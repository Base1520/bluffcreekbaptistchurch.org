# Bluff Creek Baptist Church — Homestead

This guide applies the original **BCBC — Brand Kit (Homestead) · v1.0**, selected on September 3, 2026. That canonical kit remains the source of truth for the website, Home @ the Creek, ministry materials, and church documents.

## The welcome

**Welcome home to the Creek.**

Lead the homepage with the church’s familiar identity and a plain, warm welcome. Keep service times, upcoming events, and first-visit details easy to find farther down the homepage and on Plan a Visit. Use the church’s approved beliefs and ministry descriptions. Do not introduce a new tagline, wordmark, or font family.

The homepage opens with an atmospheric chapel photograph and one primary visit action, followed by a concise heading and prose section on ivory, compact ministry rows, and a contrasting worship feature. [Design rationale and research](homepage-design-rationale.md) records the sources, limits, and reasons for these choices.

[Desktop homepage preview](previews/home-desktop.png) · [Phone homepage preview](previews/home-phone.png)

## Color

| Role | Name | Hex |
| --- | --- | --- |
| Main ground | Ivory | `#F5EFE3` |
| Cards and surfaces | White | `#FFFFFF` |
| Primary brand color; headings and secondary buttons | Pine | `#3C5A45` |
| Original creek; one primary action per screen; accents | Wheat / Gold | `#B08636` |
| Rare emphasis; Missions accent | Clay | `#A8573E` |
| Text and wordmark | Ink | `#221F1A` |
| Chips and icon wells | Pine tint | `#EAF0EA` |
| Official Louisiana 63 marker only | Sign green | `#006B54` |

Supporting colors: soft text `#5E574C`, faint text `#938A79`, border `#E4DAC8`, wheat tint `#F6EED9`, and pine deep `#2E4636`. Ministry accents also include moss `#6B8F5E` and creek blue `#557A82`.

Aim for roughly **62% ivory, 16% white, 12% pine, 7% gold, and 3% clay**. Light colors lead. Sign green belongs to the official highway marker alone.

**Accessibility implementation note:** darker gold `#826021` may be used for readable small text on ivory or white. It is a contrast adjustment, separate from the canonical palette. The real gold creek and wheat primary button stay `#B08636`.

## Typography

**Bitter 600** is the display and heading face; use 700 sparingly. **Nunito Sans 400–800** is the body and interface face. The script in the existing wordmark is never used as a separate font.

The exact Bitter and Nunito Sans faces are hosted locally through `css/fonts.css`. Their original files and official SIL Open Font Licenses are included in `assets/fonts/`; see the [font provenance](../assets/fonts/README.md). This removes external font stylesheet requests while preserving the typography.

| Level | Canonical scale |
| --- | --- |
| Display | 44px / 1.02 |
| Title | 30px / 1.06 |
| Heading | 22px |
| Subhead | 17px |
| Body | 16px / 1.6 |
| Small | 14px |
| Label | 11px, uppercase, 0.14em tracking |

The website welcome adapts the display size from 38px on the narrowest phones to 76px on wide screens to maintain a clear headline/body hierarchy. This is a responsive application of the original type family, not a new font system. Keep headlines in sentence case, balance their wrapping, and keep body copy to about 65 characters per line. Labels are short; times and tables use tabular figures.

## Wordmark, creek, and highway marker

The existing wordmark never changes. Use it black on ivory or white, or reversed on pine, at its natural proportions. Minimum width is 120px or 1.25 inches; leave clear space equal to the capital B’s height. Do not recolor, shadow, outline, stretch, rotate, or separate its parts.

Use the actual creek brushstroke lifted from the logo. The supplied gold asset is the default for about 90% of uses. Pine is secondary on white; ivory can be used quietly on pine or ink. Never redraw the creek or replace it with a generic wave. It points right, is at least 48px wide, and appears once per screen at full strength. It can underline a ministry lockup, divide a section, or appear as a quiet hero texture.

Use the official Louisiana 63 marker in its original green, small and near an address. Typical sizes are 20–24px by an address, 28–34px in the app header, or 0.75–1.25 inches in print. It is never another logo. The consistent byline is **1706 · LA 63 · Clinton**. A Bitter “63” watermark may be used at 5–8% opacity, below about 9%, away from body text; allow only one quiet highway reference per surface.

On the homepage, the LA 63 marker anchors the full-width wayfinding bar immediately after the photographic welcome. The unchanged 32px marker, address, and directions form one useful group. The bar also points toward the church introduction; it separates the opening from the story without turning service times into the first impression.

“6 on the 63” continues in the weekly introduction. Keep the highway thread tied to location and church life. Do not tint, filter, redraw, or outline the official marker, or scatter it through ministry links as decoration.

## Surfaces and buttons

Use an 8-point spacing grid, with 4-point adjustments where needed. Ivory grounds and white cards are the default.

- Inputs and chips: **12px radius**.
- Cards: **16–18px radius**.
- Hero surfaces: **22px radius**.
- Phone frames: **30–44px radius**.
- Buttons: **13px radius**, Nunito Sans 800.
- Border: **1px `#E4DAC8`**.
- Warm shadow: **`0 8px 24px rgba(40,33,20,.06)`**.

Use **one wheat primary button per screen**, pine secondary buttons, and ghost tertiary buttons. Use readable text on each surface. Icons, when needed, are 2px line icons in pine within pine-tint wells.

## One ministry family

The single construction is **`[Ministry] @ the Creek`**. Set the lockup in Bitter 600, with the `@` in wheat italic and the original gold creek beneath it, left-aligned at about 60% of the text width. Ministries differ by accent color only.

| Lockup | Accent |
| --- | --- |
| Church @ the Creek | Pine `#3C5A45` |
| Worship @ the Creek | Wheat `#B08636` |
| Kidz @ the Creek | Moss `#6B8F5E` |
| Youth @ the Creek | Creek blue `#557A82` |
| Missions @ the Creek | Clay `#A8573E` |
| Home @ the Creek | Ink `#221F1A` |

**Kidz** always keeps the z. Do not create new ministry logos, icons, or mascots, and do not use `@` outside a ministry lockup.

## Voice and photography

The voice is warm, plain, and invitational: a neighbor holding the door. Use the approved welcome, **“Welcome home to the Creek.”** Keep useful details specific. Use *students*, *give*, and the established ministry names. Avoid hype and formal invitation language.

Photographs support the welcome when they help someone recognize a place or person. The homepage uses the existing graded chapel photograph for its opening. The shorter church story pairs a heading with prose in two columns; the existing sign photograph is a faint decorative background beneath an ivory wash, with no figure or caption. The texture occupies the left 62% at 14% opacity on desktop and the top half at 12% opacity on phones. It carries no essential information and is hidden from assistive technology.

About uses existing staff portraits. Photography stays visually subdued. No new identifiable people, minors, or field-ministry photographs are introduced. Original files remain untouched; responsive derivatives strip metadata and never enlarge small originals.

## Applying the kit elsewhere

- **Weekly update:** the original wordmark, a Bitter title, a short opening paragraph, useful dates, and one wheat primary action.
- **Social graphics:** an ivory or pine ground, a clear headline, the original creek, and readable date/location information where relevant.
- **Sunday slides and stream:** the same wordmark, Bitter headings, Nunito Sans supporting text, and gold creek. Use approved service titles and imagery.
- **Policies and forms:** the wordmark, pine headings, white body pages, and clear owner, version, and date fields. Use approved church information only.
- **Staff signatures:** church name, role, approved church contact, and website; keep the mark small and text readable without images.
- **Creek Office:** use the same original kit when the separate admin portal is reviewed. This website work does not activate its authentication or storage.

These are application guidelines. Creating or changing live templates, accounts, or church records remains separate work.

## Maintaining the website

Edit page content in `build.py`, shared structure in `css/site.css`, and refinements in `css/polish.css`. Run `python3 build.py`; do not hand-edit the generated HTML. The normal build uses Python’s standard library.

The calendar reads the app-owned `events.json`. Keep verified dated occurrences current; this work does not invent future dates or connect the Google approvals CSV. Build and browser validation use America/Chicago. Expired dates are removed, empty calendars link to the weekly schedule, and the no-JavaScript fallback shows verified weekly gathering times.

When an approved source photo changes, install Pillow in a local development environment and run `python3 tools/image_pipeline.py`. Commit the generated manifest and derivatives with the approved source change. `image_helpers.py` emits responsive WebP sources, a JPEG fallback, lazy loading, and image dimensions.

Share graphics live in `assets/social/`. Run `python3 tools/social_cards.py --output /tmp/bcbc-share-cards` to create their self-contained HTML sources, then capture each in a browser at exactly 1200 × 630 after fonts load. These occasional exports are separate from the normal build.

Run `python3 -m unittest discover -s tests` and `node --test tests/events.test.cjs`. Review desktop and phone layouts before opening a PR. Follow the existing branch and PR workflow; deploying, changing DNS, or activating accounts requires the user’s authorization.
