# Website verification

## Current integrated Highway 63 treatment

The centered welcome sits in a single rounded frame. Its address link interrupts the bottom border, while the original highway SVG appears at 8% opacity in the empty lower-right corner. The marker remains square, unfiltered, and clipped within the frame; it hides at 1040px and below where the side space is needed for content. The Wednesday note and church-photo caption use matching rules and address typography without added icons.

Targeted browser checks at 1440, 1100, 1040, 768, 520, 375, and 320 pixels found no horizontal overflow, broken loaded images, or numeric service times in the opening viewport. The marker stays clear of text and buttons. The address link reaches Contact, and its keyboard focus outline is visible on desktop and narrow phones. The Wednesday rule and photo caption fit at 320px. Desktop, phone, tablet, and detail screenshots were reviewed, and homepage PR previews were refreshed. Static build and diff checks pass; the original marker asset is unchanged.

## Homestead restoration baseline

The homepage and Plan a Visit page now introduce the church and welcome visitors before showing numeric service times. Browser verification at 1440, 520, and 320 pixels confirms no numeric service times in either opening viewport, no horizontal overflow, Bitter/Nunito Sans, the original ivory/pine/gold palette, and a rounded gold primary action. About and Ministries were checked for consistent typography and color at phone width.

The homepage Sunday strip now follows the church introduction, ministries, calendar, and worship content. Plan a Visit keeps a service-times jump link near the introduction and places the time cards below its FAQs. All 26 generated documents have valid local references and anchors; the welcome/service ordering checks and 19 Python + 7 Node tests pass. The homepage share card and review screenshots were refreshed.

## Earlier performance baseline

Historical comparison of `origin/main` at `bc7513c` and the first implementation of the image/performance improvements, before the final Homestead restoration. These Lighthouse figures are retained as development evidence and are not a fresh measurement of the current layout. Both runs used the same local browser/tool configuration; these are laboratory measurements, not production field data.

| Measure | Before | After |
| --- | ---: | ---: |
| Mobile Performance | 69 | 99 |
| Mobile Accessibility | 100 | 100 |
| Mobile SEO | 100 | 100 |
| Mobile LCP | 5.6s | 1.9s |
| Mobile initial transfer | 1824 KiB | 233 KiB |
| Desktop Performance | 99 | 100 |
| Desktop Accessibility | 100 | 100 |
| Desktop SEO | 100 | 100 |
| Desktop LCP | 0.9s | 0.6s |
| Desktop initial transfer | 1824 KiB | 297 KiB |

## Earlier full-site functional and visual checks

- All 12 pages checked at 320, 375, 520, and 1440 pixels: no horizontal overflow, broken loaded images, or console/page errors. Additional homepage check at 800 pixels.
- Mobile menu: Enter to open, Tab into links, Escape to close and return focus, and link navigation.
- FAQ keyboard open/close; contact status hidden initially and native required-field validation. No message sent.
- Without JavaScript: navigation and content remain visible, and the calendar shows verified weekly meeting times.
- All 14 legacy paths navigate to their expected page or fragment.
- All 26 generated HTML documents have one h1 and valid local links, image/script references, and anchors.
- Responsive photos limited to the existing church sign and four existing staff portraits. No source photographs changed.
- 11 share graphics exported at exactly 1200 × 630; the homepage and longest title were visually checked for fit.
- 19 Python tests and 7 Node tests pass; generator and `git diff --check` pass.

## Review boundaries

No merge, deployment, main push, DNS, account, giving-destination, or private-data changes. Google CSV calendar integration and activation of the separate Creek Office portal remain separate work. Calendar dates are not automatically invented or rolled forward.
