# Website redesign verification

Comparison of the previous `origin/main` at `bc7513c` and the proposed Homestead editorial design. Lighthouse measured locally with the same browser/tool configuration. These are laboratory measurements, not production field data.

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

## Functional and visual checks

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
