# Website verification

## Current research-informed homepage — September 5, 2026

The worship feature includes a generated open-Bible illustration with real alpha transparency, positioned on the right at 10% opacity. The service-time label uses ivory for contrast over the image. Its 1200×800 WebP is 105,266 bytes, has empty alt text inside an `aria-hidden` wrapper, preserves its aspect ratio, loads lazily, and cannot intercept pointers. At 1440/768/375/320 pixels there is no horizontal overflow. Actual rendered-background contrast for the final right-hand placement passes: body 4.869:1 minimum, small label 4.924:1, time 5.338:1, beliefs link 5.197:1, and Watch button 5.164:1. The large heading also passes its 3:1 threshold. Keyboard activation reaches Watch and Beliefs. The exact generation prompt, asset provenance, and alpha-preserving optimization are recorded in `assets/illustrations/README.md`; this is a generic decorative illustration.

The floating navigation was checked at 1440, 768, 375, and 320 pixels. No horizontal overflow, logo/menu collision, or numeric opening service times were found. The hero text passes actual background contrast sampling: minimum small-eyebrow contrast 4.525:1 and large-heading contrast 3.625:1. On a narrow phone, the header remains at the top while scrolling; Enter opens the menu, Tab reaches the navigation, Escape closes it and restores focus, and the Visit link navigates and closes the menu. A fresh phone load with JavaScript disabled shows all six navigation links, hides the menu button, and puts the header in normal flow with 14px panel padding; the hero starts immediately after the header without overlap or overflow.

The family section also includes the original LA 63 sign as a faint, clipped background: 6% opacity at the lower left on desktop, and 5% at the upper right on phones. Targeted checks at 1440, 768, 375, and 320 pixels confirm no horizontal overflow, intact text and links, natural sign proportions, no image filter, and no pointer interception. The image has empty alt text inside an `aria-hidden` container; its original SVG is unchanged. The background now scales to 48vw (maximum 640px) on desktop and 68% of section width (maximum 400px) on phones. Actual rendered-background contrast checks for the overlaid introduction pass at all four widths; the lowest normal-text reading is 4.626:1. The approved welcome copy and brick-sign background remain intact. Build, diff, and all 26 generated documents’ reference/anchor checks pass.

The opening uses a floating, rounded ivory navigation panel over the existing graded chapel photograph, the original Homestead identity, one gold visit action, and a quiet introduction link. The unchanged LA 63 marker anchors the address in a wayfinding bar. The church story is a shorter, typography-led section with the existing brick-sign photograph only as a faint decorative background under an ivory wash. Compact ministry rows, a pine worship feature, the calendar, and first-visit details follow. Numeric service times stay out of the opening viewport.

The homepage was checked at 1440, 1100, 768, 520, 375, and 320 pixels before the final sign-background refinement. Those checks found no horizontal overflow, broken loaded images, console/page errors, or numeric opening service times. Visit, introduction-anchor, address, ministry, and worship links worked. Mobile navigation responds to Enter/Tab/Escape and restores focus; all four FAQs open with Enter and close with Space. A visible ivory outline identifies keyboard focus in the hero.

Before the floating navigation refinement, text over the rendered hero photograph was sampled at each width. The weakest large-heading contrast was 4.097:1, above the 3:1 large-text threshold. The corrected small eyebrow measured 5.623:1 at its weakest viewport; the gold primary action measured 5.164:1. These pixel checks complement the automated accessibility audit.

The exact existing Bitter and Nunito Sans font files are now served locally with `font-display: swap`, normal-face preloads, and their original official licenses. The chapel photo has responsive, metadata-free WebP/JPEG derivatives; no original photographs changed. Decorative photos have empty alt text and are hidden from assistive technology.

The final story/background refinement was checked at 1440, 768, 375, and 320 pixels. Every story text sample passes its contrast threshold; the pine eyebrow’s minimum is 5.877:1. No overflow or broken loaded images occurred. Home and Plan a Visit load local Bitter and Nunito Sans without any Google font requests. Desktop and phone review images were refreshed.

The mobile Lighthouse run before the decorative family-section sign, floating navigation, and worship illustration reports **91 Performance / 100 Accessibility / 100 SEO**, FCP 1.7s, LCP 3.5s, Speed Index 1.7s, TBT 0ms, CLS 0, and 399 KiB transferred. Before local-font integration and the final story refinement, the same local audit reported 85/100/100, FCP 3.0s, LCP 3.2s, and Speed Index 4.4s. Initial rendering improved while the measured LCP increased; this is not a claim that every metric improved. Both are local laboratory runs, not production field data. Original reports are retained as the pre-optimization comparison.

Build and diff checks pass. All 26 generated HTML documents have one h1 and valid local links, assets, and anchors; CSS asset references also resolve. The 19 Python and 7 Node tests pass. Design sources, evidence limits, and proposed visitor tests are documented in `docs/homepage-design-rationale.md`. Visitor recognition, engagement, and scrolling have not been measured.

## Earlier Homestead restoration baseline

At this earlier checkpoint, the homepage and Plan a Visit page introduced the church and welcome visitors before showing numeric service times. Browser verification at 1440, 520, and 320 pixels confirms no numeric service times in either opening viewport, no horizontal overflow, Bitter/Nunito Sans, the original ivory/pine/gold palette, and a rounded gold primary action. About and Ministries were checked for consistent typography and color at phone width.

At this earlier checkpoint, the homepage Sunday strip followed the church introduction, ministries, calendar, and worship content. Plan a Visit keeps a service-times jump link near the introduction and places the time cards below its FAQs. All 26 generated documents have valid local references and anchors; the welcome/service ordering checks and 19 Python + 7 Node tests pass. The homepage share card and review screenshots were refreshed.

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
