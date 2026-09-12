"""Responsive HTML for approved photos. Uses checked-in assets; no Pillow at build time."""

import html
import json
from functools import lru_cache
from pathlib import Path

MANIFEST_PATH = Path(__file__).resolve().parent / "assets/optimized/manifest.json"


@lru_cache(maxsize=1)
def image_manifest():
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["images"]
    except FileNotFoundError as error:
        raise RuntimeError("Missing responsive assets. Run python3 tools/image_pipeline.py first.") from error


def responsive_image(filename, alt, sizes, class_name="", loading="lazy"):
    """Return picture markup with WebP choices, JPEG fallback and stable dimensions.

    Example: responsive_image('sign.jpg', 'The church entrance',
                              '(min-width: 900px) 45vw, 100vw', 'place-photo')
    Only use loading='eager' for a photograph visible in the opening viewport.
    Style the img or its existing container; the picture wrapper has no class.
    """
    if loading not in {"lazy", "eager"}:
        raise ValueError("Image loading must be 'lazy' or 'eager'")
    try:
        entry = image_manifest()[filename]
    except KeyError as error:
        raise ValueError(f"No approved responsive image for {filename!r}") from error
    escape = lambda value: html.escape(str(value), quote=True)
    srcset = ", ".join(f"{escape(variant['src'])} {variant['width']}w" for variant in entry["webp"])
    class_attribute = f' class="{escape(class_name)}"' if class_name else ""
    priority = ' fetchpriority="high"' if loading == "eager" else ""
    return (
        f'<picture><source type="image/webp" srcset="{srcset}" sizes="{escape(sizes)}">'
        f'<img{class_attribute} src="{escape(entry["fallback"]["src"])}" '
        f'width="{entry["width"]}" height="{entry["height"]}" alt="{escape(alt)}" '
        f'loading="{loading}" decoding="async"{priority}></picture>'
    )
