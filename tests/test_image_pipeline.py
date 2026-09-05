"""Validate image output rather than the mechanics of the encoder."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("image_pipeline", ROOT / "tools/image_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)
helper_spec = importlib.util.spec_from_file_location("image_helpers", ROOT / "image_helpers.py")
helpers = importlib.util.module_from_spec(helper_spec)
helper_spec.loader.exec_module(helpers)


class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class ImagePipelineTests(unittest.TestCase):
    def test_committed_outputs_are_current_and_preserve_aspect_ratio(self):
        import hashlib
        manifest = json.loads((ROOT / "assets/optimized/manifest.json").read_text())
        for name, entry in manifest["images"].items():
            self.assertEqual(hashlib.sha256((ROOT / entry["source"]).read_bytes()).hexdigest(), entry["source_sha256"], name)
            for variant in [*entry["webp"], entry["fallback"]]:
                with Image.open(ROOT / variant["src"]) as image:
                    self.assertEqual(image.size, (variant["width"], variant["height"]))
                    self.assertLessEqual(image.width, entry["width"])
                    self.assertAlmostEqual(image.height, entry["height"] * image.width / entry["width"], delta=1)
                    self.assertFalse(image.getexif())
                    self.assertEqual((ROOT / variant["src"]).stat().st_size, variant["bytes"])

    def test_small_oriented_source_is_not_upscaled_and_outputs_repeat(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            exif = Image.Exif()
            exif[274] = 6
            Image.new("RGB", (120, 80), "#3c5a45").save(source / "example.jpg", exif=exif)
            manifest = pipeline.generate(source, root / "one", ["example.jpg"])
            pipeline.generate(source, root / "two", ["example.jpg"])
            entry = manifest["images"]["example.jpg"]
            self.assertEqual((entry["width"], entry["height"]), (80, 120))
            for path in (root / "one").iterdir():
                self.assertEqual(path.read_bytes(), (root / "two" / path.name).read_bytes())

    def test_markup_escapes_attributes_and_reserves_space(self):
        markup = helpers.responsive_image("sign.jpg", 'Road sign " & <welcome>', '(max-width: 800px) 100vw, 45vw', 'place-photo')
        elements = Elements(markup).elements
        source = next(attrs for tag, attrs in elements if tag == "source")
        image = next(attrs for tag, attrs in elements if tag == "img")
        self.assertEqual(image["alt"], 'Road sign " & <welcome>')
        self.assertEqual(image["loading"], "lazy")
        self.assertEqual(image["decoding"], "async")
        self.assertIn("width", image)
        self.assertIn("height", image)
        self.assertNotIn("fetchpriority", image)
        self.assertEqual(source["type"], "image/webp")
        self.assertIn("sizes", source)
        self.assertTrue(image["src"].endswith(".jpg"))
        self.assertEqual([tag for tag, _ in elements], ["picture", "source", "img"])

    def test_unapproved_sources_and_invalid_loading_fail(self):
        with self.assertRaises(ValueError):
            helpers.responsive_image("not-approved.jpg", "", "100vw")
        with self.assertRaises(ValueError):
            helpers.responsive_image("sign.jpg", "", "100vw", loading="invalid")
        with self.assertRaises(ValueError):
            pipeline.source_name("../../private.jpg")


if __name__ == "__main__":
    unittest.main()
