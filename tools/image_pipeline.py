#!/usr/bin/env python3
"""Make responsive derivatives of approved, existing BCBC website photographs.

Run from any directory: python3 tools/image_pipeline.py
Requires Pillow. Normal HTML builds use the committed outputs, not Pillow.

This only resizes and encodes existing photos. It never crops, recolors, sharpens,
upscales, or changes their content. Metadata is omitted from public derivatives.
The explicit source list prevents publishing new photography accidentally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = (
    "sign.jpg",
    "hero-church.jpg",
    "cole-headshot.jpg",
    "ashleigh-pierce.jpg",
    "janice-mcnabb.jpg",
    "jackie-brian.jpg",
)
WIDTHS = (320, 640, 960, 1440, 1920)


def source_name(filename: str) -> str:
    """Require a local JPEG basename; never read paths outside assets/photos."""
    if Path(filename).name != filename or Path(filename).suffix.lower() not in {".jpg", ".jpeg"}:
        raise ValueError(f"Expected a JPEG filename, received {filename!r}")
    return filename


def resize(image: Image.Image, width: int) -> Image.Image:
    if width >= image.width:
        return image.copy()
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def generate(source_directory: Path, output_directory: Path, sources=DEFAULT_SOURCES) -> dict:
    """Write a deterministic manifest and files, given identical Pillow/libwebp versions."""
    names = sorted({source_name(name) for name in sources})
    if not names:
        raise ValueError("At least one approved source is required")
    stems = [Path(name).stem for name in names]
    if len(stems) != len(set(stems)):
        raise ValueError("Source basenames must have unique stems")
    for name in names:
        if not (source_directory / name).is_file():
            raise FileNotFoundError(source_directory / name)

    output_directory.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": 1,
        "encoder": {"pillow": PILLOW_VERSION, "webp_quality": 78, "jpeg_quality": 82},
        "images": {},
    }
    for name in names:
        path = source_directory / name
        with Image.open(path) as source:
            # Transpose camera orientation before recording intrinsic dimensions.
            original = ImageOps.exif_transpose(source).convert("RGB")
        widths = sorted({width for width in WIDTHS if width < original.width} | {min(original.width, WIDTHS[-1])})
        entry = {
            "source": f"assets/photos/{name}",
            "source_bytes": path.stat().st_size,
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "width": original.width,
            "height": original.height,
            "webp": [],
        }
        for width in widths:
            derivative = resize(original, width)
            output = output_directory / f"{Path(name).stem}-{width}.webp"
            derivative.save(output, format="WEBP", quality=78, method=6, exif=b"")
            entry["webp"].append({
                "src": f"assets/optimized/{output.name}",
                "width": derivative.width,
                "height": derivative.height,
                "bytes": output.stat().st_size,
            })

        fallback = resize(original, min(original.width, 960))
        output = output_directory / f"{Path(name).stem}-fallback.jpg"
        fallback.save(output, format="JPEG", quality=82, optimize=True, progressive=True, exif=b"")
        entry["fallback"] = {
            "src": f"assets/optimized/{output.name}",
            "width": fallback.width,
            "height": fallback.height,
            "bytes": output.stat().st_size,
        }
        manifest["images"][name] = entry

    manifest["totals"] = {
        "source_bytes": sum(entry["source_bytes"] for entry in manifest["images"].values()),
        "mobile_640_webp_bytes": sum(
            next((variant for variant in entry["webp"] if variant["width"] >= 640), entry["webp"][-1])["bytes"]
            for entry in manifest["images"].values()
        ),
        "all_generated_bytes": sum(
            entry["fallback"]["bytes"] + sum(variant["bytes"] for variant in entry["webp"])
            for entry in manifest["images"].values()
        ),
    }
    (output_directory / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", nargs="+", default=list(DEFAULT_SOURCES), help="Approved JPEG basenames already in assets/photos")
    args = parser.parse_args()
    manifest = generate(ROOT / "assets/photos", ROOT / "assets/optimized", args.sources)
    for name, entry in manifest["images"].items():
        mobile = next((v for v in entry["webp"] if v["width"] >= 640), entry["webp"][-1])
        print(f"{name}: {entry['source_bytes']:,} source bytes → {mobile['bytes']:,} bytes at {mobile['width']}px WebP")
    print(json.dumps(manifest["totals"], indent=2))


if __name__ == "__main__":
    main()
