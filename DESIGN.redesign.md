# The Pinkfong Company — Design System

> **Legend** — Values without a mark were observed on the live corporate site (home, company, business; 1440×900 capture). Values marked **†** are proposed defaults that complete the system; they are consistent with the observed values but are not taken from the site.

## Overview

The Pinkfong Company is a global family-entertainment company whose portfolio is led by Pinkfong, Baby Shark, and Bebefinn, spanning music, stories, video and audio content, live events, mobile apps, partnerships, and merchandise. Its stated mission is to connect people through joyful content and entertaining experiences. The corporate interface is deliberately restrained: black ink (`{colors.ink}` — #000000) and muted gray (`{colors.text-muted}` — #5a5a5a) on a pure white canvas (`{colors.canvas}`), so that the character worlds (artwork, BI logos, video thumbnails) supply the color and the chrome stays out of their way.

The geometry is soft and friendly. Every interactive element is a rounded pill at `{rounded.pill}` (32px): the pink corporate CTA, the family-site pill, the outline actions, badges, and tabs. Containers sit at `{rounded.lg}` (24px)†, media at `{rounded.md}` (20px)†. Pills carry a signature detail: a flat 2px "ledge" shadow with no blur, which makes buttons feel like physical, pressable toy blocks. Body text is set in Spoqa Han Sans Neo; large display moments use the official Pinkfong Baby Shark Font, whose fin-inspired triangular details carry the character voice.

One color is allowed to interrupt: Pinkfong pink (`{colors.primary}` — #ff66af), used for the primary action. A secondary sky blue (`{colors.accent}` — #08c7ff) handles outline and informational actions. Pink appears at most once or twice per view; when it does, it is the one thing asking to be clicked.

**Primary tasks** the corporate site serves:

- Find out what the company makes across music, apps, and events
- Download the identity assets (CI/BI) for the company or a franchise
- Download the official Baby Shark font for a document

**Key Characteristics:**

- White corporate shell — `{colors.ink}` and `{colors.text-muted}` on `{colors.canvas}`, with `{colors.primary}` pink as the single brand-action color
- Pill interaction language: buttons, badges, tabs, and chips all at `{rounded.pill}`
- The 2px ledge — a blur-free bottom shadow under pills that collapses on press
- Near-flat elevation elsewhere; only overlays (modal, toast, dropdown) float
- Spoqa Han Sans Neo for running text; Pinkfong Baby Shark Font for display headlines only
- Portfolio identities stay distinct — company CI and the Pinkfong, Baby Shark, and Bebefinn BIs are shown as separate assets, never merged into one palette
- Content supplies the color: character art, franchise logos, and thumbnails carry all visual richness

## Colors

Source pages: corporate home, company, business.

### Brand & Accent

- **Pinkfong Pink** (`{colors.primary}` — #ff66af): The brand-action color. Fills the primary CTA on every page. Used for the single most important action per view, never decoratively.
- **Pink Hover** (`{colors.primary-hover}` — #f5519f)†: Hover fill for primary pills.
- **Pink Pressed** (`{colors.primary-pressed}` — #e63d8b)†: Pressed fill for primary pills.
- **Pink Tint** (`{colors.primary-soft}` — #fff0f7)†: Soft pink wash for selected tabs, highlighted rows, and the featured card.
- **Sky Blue** (`{colors.accent}` — #08c7ff): Secondary accent. Label and border of outline actions, text links, and informational highlights.
- **Sky Tint** (`{colors.accent-soft}` — #e8f9ff)†: Background for info banners and accent badges.

### Surface

- **Canvas** (`{colors.canvas}` — #ffffff): Default page, card, pill, and dialog background.
- **Soft Canvas** (`{colors.canvas-soft}` — #f7f7f7)†: Alternate section bands, table header rows, and the segmented-control track.
- **Field** (`{colors.field}` — #f2f2f2)†: Fill for form inputs at rest.
- **Soft Hairline** (`{colors.hairline-soft}` — #eeeeee)†: 1px outlines on resting cards and table row dividers.
- **Hairline** (`{colors.hairline}` — #dcdcdc)†: Stronger 1px border for neutral outline buttons and dropdowns.
- **Inverse** (`{colors.inverse}` — #111111)†: Footer band background.

### Text

- **Ink** (`{colors.ink}` — #000000): Headings, body copy, and nav links.
- **Muted** (`{colors.text-muted}` — #5a5a5a): Secondary copy — descriptions, metadata, supporting paragraphs.
- **Subtle** (`{colors.text-subtle}` — #8c8c8c): Tertiary labels, such as the family-site pill label and captions.
- **Faint** (`{colors.text-faint}` — #b3b3b3)†: Placeholders, disabled labels, and fine print.
- **On Primary** (`{colors.on-primary}` — #ffffff): Text on `{colors.primary}`, `{colors.accent}`, and `{colors.inverse}` fills.

### Semantic†

| Token                     | Value   | Use                                  |
| ------------------------- | ------- | ------------------------------------ |
| `{colors.success}`        | #1fb86b | Download complete, form sent         |
| `{colors.warning}`        | #ffae00 | Usage-limit and license notices      |
| `{colors.error}`          | #e5302f | Validation errors, failed downloads  |
| `{colors.info}`           | #08c7ff | Same as `{colors.accent}`            |

Error red is deliberately cooler and darker than Pinkfong pink so the two never read as the same signal.

## Typography

### Font Family

**Spoqa Han Sans Neo** — the corporate text family, loaded on every corporate page and distributed under the SIL Open Font License. Use it for all body text, labels, buttons, and UI headings. Weights: Light 300† · Regular 400 · Medium 500† · Bold 700.

**Pinkfong Baby Shark Font** — the official display face, released in 2025 for Baby Shark's tenth anniversary: 9 languages, 13,200 characters, fin-inspired triangular details, and a rhythm drawn from the song. On the site it appears as the business-page h1 (font file `BabyShark`). Use it only for `{typography.display}` and `{typography.display-sm}`†. Freely downloadable from the company identity page; confirm webfont licensing before embedding it on new properties.

**Fallback stack:** `"Spoqa Han Sans Neo", -apple-system, system-ui, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans KR", Arial, sans-serif`.

Sizes are listed for desktop (1440 baseline) and mobile (390 baseline)†.

### Hierarchy

| Token                      | Desktop | Mobile† | Weight | Line Height | Family      | Use                                        |
| -------------------------- | ------- | ------- | ------ | ----------- | ----------- | ------------------------------------------ |
| `{typography.display}`     | 48px    | 36px†   | 700    | 1.0         | Baby Shark  | Hero headline                              |
| `{typography.display-sm}`† | 36px    | 28px    | 700    | 1.1         | Baby Shark  | Franchise section titles                   |
| `{typography.heading-1}`   | 38px    | 28px†   | 700    | 1.57        | Spoqa       | Page titles                                |
| `{typography.heading-2}`†  | 28px    | 22px    | 700    | 1.45        | Spoqa       | Section headings                           |
| `{typography.heading-3}`†  | 22px    | 18px    | 700    | 1.45        | Spoqa       | Card headlines                             |
| `{typography.cta-lg}`      | 24px    | 18px†   | 400    | 1.3†        | Spoqa       | Hero CTA label                             |
| `{typography.cta}`         | 18px    | 16px†   | 400    | 1.3†        | Spoqa       | Standard button label                      |
| `{typography.body-lg}`†    | 18px    | 17px    | 300    | 1.6         | Spoqa       | Lead paragraphs under headings             |
| `{typography.body}`        | 16px    | 15px†   | 400    | 1.57        | Spoqa       | Default body copy                          |
| `{typography.body-sm}`†    | 14px    | 13px    | 400    | 1.57        | Spoqa       | Supporting copy, table cells               |
| `{typography.label}`       | 14px    | 13px†   | 400    | 1.4†        | Spoqa       | Pills, tabs, menu items                    |
| `{typography.caption}`†    | 12px    | 12px    | 400    | 1.4         | Spoqa       | Metadata, legal text, badge labels         |

### Principles

- **Character in the headline, calm in the body.** The Baby Shark face carries brand personality in display sizes only; everything else stays in neutral Spoqa.
- **Open leading.** Body copy sits at about 1.57 line height, comfortable for Korean and Latin text alike.
- **Zero letter-spacing.**† Both families are used at their natural fit; no tracking or all-caps treatment.

## Layout

### Spacing System†

- **Base unit**: 4px, stepping mainly in 8s
- **Tokens**: `{spacing.xxs}` 4px · `{spacing.xs}` 8px · `{spacing.sm}` 12px · `{spacing.md}` 16px · `{spacing.lg}` 20px · `{spacing.xl}` 32px · `{spacing.section}` 64px · `{spacing.section-lg}` 120px
- Observed button padding is kept as recorded (for example `32px 15px` on the hero CTA). New buttons use `{spacing.md}` vertical and `{spacing.xl}` horizontal.
- Card padding is `{spacing.xl}` on desktop and `{spacing.lg}` on mobile.

### Grid & Container†

- Content column max-width 1200px, centered, on a 12-column grid with 24px gutters.
- Franchise and business tiles use a 3-up grid; news and asset lists use a 4-up card grid; the company overview uses a 2-column split (text left, media right).
- Hero art and video strips run full-bleed beyond the content column.

### Whitespace Philosophy

The white canvas and muted text leave room for the pink action and the character art to stand out. Sections are separated by `{spacing.section}` to `{spacing.section-lg}` of empty canvas, with `{colors.canvas-soft}` bands used instead of divider rules when a change of section needs marking.†

### Responsive Strategy

#### Screen Size

| Name    | Width        | Columns | Side padding | Notes                                   |
| ------- | ------------ | ------- | ------------ | --------------------------------------- |
| Desktop | ≥ 1200px     | 12      | 40px†        | Baseline frame 1440 × 900 (observed)    |
| Tablet† | 768–1199px   | 8       | 32px         |                                         |
| Mobile† | ≤ 767px      | 4       | 20px         | Baseline frame 390 × 844; minimum 360px |

#### Touch Targets

- Observed heights: hero CTA 64px, outline action 60px, family-site pill 35px.
- Every tap target has at least a 44 × 44px hit area†; the 35px family-site pill gets extra invisible padding on mobile.

#### Collapsing Strategy†

- The top navigation collapses into the observed mobile menu dialog below 1200px: logo left, hamburger right, and a full-screen `{colors.canvas}` sheet listing links at `{typography.heading-3}`.
- Multi-column grids step down 4 → 2 → 1 and 3 → 2 → 1 rather than scrolling horizontally.
- The hero CTA goes full-width on mobile.

#### Image Behavior†

- Character art and thumbnails keep fixed aspect ratios (16:9 for video, 1:1 for franchise tiles) and `{rounded.md}` corners.
- BI logos are never cropped, recolored, or placed on busy backgrounds; they sit on `{colors.canvas}` or `{colors.canvas-soft}` with clear space equal to the logo height × 0.25.
- Images below the fold are lazy-loaded.

## Elevation & Depth

| Level    | Treatment                                         | Use                                             |
| -------- | ------------------------------------------------- | ----------------------------------------------- |
| 0        | Flat, `box-shadow: none`                          | Default — most surfaces, the mobile menu dialog |
| Ledge    | `rgba(0, 0, 0, 0.02) 0px 2px 0px 0px`             | Neutral pills (family-site pill)                |
| Ledge-pink | `rgba(255, 5, 88, 0.06) 0px 2px 0px 0px`        | Primary pills                                   |
| Card†    | 1px `{colors.hairline-soft}` outline, no shadow   | Resting cards                                   |
| Float†   | `rgba(0, 0, 0, 0.08) 0px 8px 24px 0px`            | Dropdowns, toasts                               |
| Modal†   | `rgba(0, 0, 0, 0.12) 0px 16px 40px 0px` + 40% ink scrim | Modals, the opened mobile menu            |

The ledge is the signature depth cue: a blur-free 2px drop under pills. On press the ledge disappears and the pill moves down 2px, like a button being pushed in.† Nothing else on the page casts a shadow at rest.

### Motion†

| Token                | Value                            | Use                                  |
| -------------------- | -------------------------------- | ------------------------------------ |
| `{motion.fast}`      | 120ms                            | Hover and press color changes        |
| `{motion.base}`      | 200ms                            | Tabs, accordions, dropdowns          |
| `{motion.slow}`      | 320ms                            | Modals, the mobile menu sheet        |
| `{motion.ease}`      | `cubic-bezier(0.2, 0, 0, 1)`     | Default easing                       |
| `{motion.bounce}`    | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful entrances for character art only |

Under `prefers-reduced-motion: reduce`, all transitions drop to an instant change and bounce is disabled.

## Shapes

### Border Radius Scale

| Token             | Value | Use                                                    |
| ----------------- | ----- | ------------------------------------------------------ |
| `{rounded.none}`  | 0px   | Full-bleed hero art and video strips                   |
| `{rounded.sm}`†   | 12px  | Inputs, table containers, small thumbnails             |
| `{rounded.md}`†   | 20px  | Media tiles, video thumbnails                          |
| `{rounded.lg}`†   | 24px  | Cards, modals, footer top corners                      |
| `{rounded.pill}`  | 32px  | Every pill: buttons, badges, tabs, chips (observed on all captured buttons) |
| `{rounded.full}`† | 9999px | Avatars and icon buttons                              |

### Identity Geometry

- The Pinkfong Baby Shark Font's triangular, fin-shaped details are the brand's signature form. A small fin-triangle glyph may be used as a list bullet or section marker† — never as a container shape.
- Franchise tiles use `{rounded.md}` so each BI logo sits in its own calm frame.

## Components

### Buttons

**`button-primary`** — "Contact us", "Download", hero CTA

- Fill `{colors.primary}`, label `{colors.on-primary}` in `{typography.cta-lg}` (hero) or `{typography.cta}`, shape `{rounded.pill}`, hero padding `32px 15px` (observed, 64px tall), standard padding `{spacing.md} {spacing.xl}`†
- Shadow: Ledge-pink
- Hover `{colors.primary-hover}`; pressed `{colors.primary-pressed}` with the ledge removed and a 2px downward shift; disabled `{colors.field}` fill with `{colors.text-faint}` label†

**`button-outline`** — company-page business action, secondary actions

- Fill `{colors.canvas}`, label `{colors.accent}` in `{typography.cta}`, shape `{rounded.pill}`, padding `30px 15px` (observed, 60px tall)
- Border 1px `{colors.accent}`†; hover fill `{colors.accent-soft}`†

**`button-pill-neutral`** — family-site pill, filters, utility links

- Fill `{colors.canvas}`, label `{colors.text-subtle}` in `{typography.label}`, shape `{rounded.pill}`, padding `4px 20px` (observed, 35px tall)
- Shadow: Ledge; hover label `{colors.ink}`†

**Focus (all buttons)**† — 2px `{colors.ink}` ring with a 2px offset, visible only for keyboard focus.

### Cards & Containers†

**`franchise-card`** — Pinkfong / Baby Shark / Bebefinn tile

- `{colors.canvas}` fill, 1px `{colors.hairline-soft}` outline, `{rounded.lg}` corners, padding `{spacing.xl}`
- 1:1 character-art area at `{rounded.md}`, franchise name in `{typography.heading-3}`, one-line description in `{colors.text-muted}` `{typography.body}`, closed by a `button-outline`
- Laid out 3-up; each card uses only its own franchise's art and logo

**`business-tile`** — content, partnership, merchandise, live events, mobile apps

- `{colors.canvas-soft}` fill, borderless, `{rounded.lg}` corners
- Icon or photo on top, title in `{typography.heading-3}`, description in `{typography.body-sm}` `{colors.text-muted}`

**`asset-download-row`** — CI/BI and font downloads (primary task)

- Full-width row on `{colors.canvas}` with a 1px `{colors.hairline-soft}` bottom divider
- Logo preview (48px, on `{colors.canvas-soft}` at `{rounded.sm}`), asset name in `{typography.body}`, formats (AI · PNG · SVG) as `badge-neutral`, trailing `button-primary` "Download"
- After download, the button briefly shows a `{colors.success}` check†

**`news-card`** — press releases

- 16:9 thumbnail at `{rounded.md}`, date in `{typography.caption}` `{colors.text-subtle}`, headline in `{typography.heading-3}` clamped to 2 lines

### Inputs & Forms†

**`text-input`**

- `{colors.field}` fill, no border, `{colors.ink}` text with `{colors.text-faint}` placeholder, `{rounded.sm}` corners, padding `{spacing.sm} {spacing.md}`, 48px tall

**`text-input-focused`**

- Same chrome plus a 2px `{colors.accent}` ring

**`text-input-error`**

- 2px `{colors.error}` ring, helper text below in `{typography.caption}` `{colors.error}`

### Navigation

**`top-nav`**† — desktop

- Full-width `{colors.canvas}` bar, 72px tall, logo left, links in `{typography.label}` `{colors.ink}` center-right, `button-pill-neutral` family-site link and language switch at the far right
- Active link in `{colors.primary}` with a 2px underline at `{rounded.full}`
- Sticky on scroll, gaining a 1px `{colors.hairline-soft}` bottom border once scrolled

**`mobile-menu-dialog`** — mobile and tablet

- Fill `{colors.canvas}`, text `{colors.ink}` in `{typography.label}`, padding `30px` (observed)
- Opens as a full-screen sheet from the right at `{motion.slow}`†; links listed at `{typography.heading-3}`†, with the family-site pill and language switch pinned to the bottom†

**`footer`**†

- Full-width `{colors.inverse}` band with `{rounded.lg}` top corners
- Company CI in white, address and legal text in `{colors.text-faint}` `{typography.caption}`, link columns in `{colors.on-primary}` `{typography.body-sm}`, family-site pill at right

### Signature Components†

**`badge-neutral`** — `{colors.canvas-soft}` pill with `{colors.text-muted}` `{typography.caption}` label (formats, categories)

**`badge-new`** — `{colors.primary-soft}` pill with `{colors.primary}` label, for new releases; at most one per card

**`tabs`** — a row of `button-pill-neutral` pills; the selected tab fills `{colors.ink}` with `{colors.on-primary}` label

**`segmented-control`** — `{colors.canvas-soft}` pill track with a `{colors.canvas}` active pill carrying the Ledge shadow

**`stat-counter`** — large figure in `{typography.display}` over a `{typography.body}` `{colors.text-muted}` caption, for company milestones such as views and subscribers

### States†

| State    | Treatment                                                             |
| -------- | --------------------------------------------------------------------- |
| Hover    | Darker fill (primary) or `{colors.accent-soft}` fill (outline), `{motion.fast}` |
| Pressed  | Ledge shadow removed, 2px downward shift, pressed fill                |
| Focus    | 2px ring (`{colors.ink}` on buttons, `{colors.accent}` on inputs), 2px offset |
| Disabled | `{colors.field}` fill, `{colors.text-faint}` label, no shadow, `cursor: not-allowed` |
| Loading  | Label replaced by a 16px spinner in the label color; width held fixed |
| Empty    | Centered character illustration, `{typography.heading-3}` title, `{colors.text-muted}` one-line explanation, optional `button-outline` |
| Error    | `{colors.error}` ring or inline message; never pink                   |
| Success  | `{colors.success}` check icon plus confirmation text                  |

### Examples (illustrative)

> Demonstration surfaces that reuse the tokens above. Each `ex-*` entry references tokens only, so any rebuild re-skins them the same way.

**`ex-pricing-tier`** — Default tier card (partnership or license plans)

- `backgroundColor` `{colors.canvas}` · `textColor` `{colors.ink}` · `borderColor` `{colors.hairline-soft}` · `rounded` `{rounded.lg}` · `padding` `{spacing.xl}`

**`ex-pricing-tier-featured`** — Featured tier

- `backgroundColor` `{colors.primary-soft}` · `textColor` `{colors.ink}` · `rounded` `{rounded.lg}` · `padding` `{spacing.xl}` · carries `badge-new` and a `button-primary`

**`ex-product-selector`** — Franchise picker (Pinkfong / Baby Shark / Bebefinn)

- `backgroundColor` `{colors.canvas-soft}` · `rounded` `{rounded.lg}` · `padding` `{spacing.lg}`

**`ex-cart-drawer`** — Download basket for multiple CI/BI assets

- `backgroundColor` `{colors.canvas}` · `rounded` `{rounded.lg}` (left corners) · `padding` `{spacing.xl}` · `item-divider` 1px `{colors.hairline-soft}`

**`ex-app-shell-row`** — Sidebar row in a partner portal

- `backgroundColor` `{colors.canvas}` · `activeIndicator` `{colors.primary-soft}` fill + `{colors.primary}` label · `rounded` `{rounded.pill}` · `padding` `{spacing.sm} {spacing.md}`

**`ex-data-table-cell`** — Asset or license table

- `headerBackground` `{colors.canvas-soft}` · `headerTypography` `{typography.label}` in `{colors.text-muted}` · `bodyTypography` `{typography.body-sm}` · `cellPadding` `{spacing.sm} {spacing.md}` · `rowBorder` 1px `{colors.hairline-soft}`

**`ex-auth-form-card`** — Partner sign-in

- `backgroundColor` `{colors.canvas}` · `rounded` `{rounded.lg}` · `padding` `{spacing.xl}` · `text-input` fields and a full-width `button-primary`

**`ex-modal-card`** — Download license agreement

- `backgroundColor` `{colors.canvas}` · `rounded` `{rounded.lg}` · `padding` `{spacing.xl}` · Modal elevation

**`ex-empty-state-card`** — No search results

- `backgroundColor` `{colors.canvas-soft}` · `rounded` `{rounded.lg}` · `padding` `{spacing.section}` · `captionTypography` `{typography.body}` in `{colors.text-muted}`

**`ex-toast`** — "Download started"

- `backgroundColor` `{colors.inverse}` · `rounded` `{rounded.pill}` · `padding` `{spacing.sm} {spacing.lg}` · `typography` `{typography.label}` in `{colors.on-primary}` · Float elevation

## Do's and Don'ts

### Do

- Keep the canvas `{colors.canvas}` white and let character art, logos, and thumbnails supply the color.
- Use `{colors.primary}` pink for the single most important action per view.
- Use `{rounded.pill}` for every interactive element, with the 2px ledge on pills.
- Collapse the ledge on press — the push-in feel is part of the brand.
- Set body text in Spoqa Han Sans Neo and reserve Pinkfong Baby Shark Font for display headlines.
- Show company CI and the Pinkfong, Baby Shark, and Bebefinn BIs as separate identities, each with its own clear space.
- Make CI/BI and font downloads reachable in one click from the company page.
- Write copy in an optimistic, clear voice: say what the content or experience is before adding promotional flourish.

### Don't

- Don't use more than two pink elements in one view, or use pink decoratively.
- Don't use pink for errors; errors are `{colors.error}` red.
- Don't add blurred drop shadows to cards or buttons at rest; only overlays float.
- Don't set body copy or UI labels in the Baby Shark font.
- Don't recolor, crop, stretch, or merge franchise logos, or put them on busy backgrounds.
- Don't square off pills at small sizes — badges, tabs, and chips stay at `{rounded.pill}`.
- Don't apply letter-spacing or all-caps styling.
- Don't use bounce easing on UI chrome; keep it for character art entrances.
