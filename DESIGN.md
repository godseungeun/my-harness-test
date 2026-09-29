# The Pinkfong Company Reference Design System

<!-- design-md:section experience -->
## 1. Experience

### Visual Theme & Atmosphere

The Pinkfong Company is a global family-entertainment company whose official corporate pages describe a portfolio led by Pinkfong, Baby Shark, and Bebefinn. Its public materials pair memorable music, stories, technology, character worlds, and experiences for children and families; the company page explicitly frames the work as content that connects people through joy. The current reference is intentionally narrower than that portfolio: its supplied collector evidence covers only the public corporate home, company, and business pages. Those pages use a mostly white, black, and gray corporate shell with Pinkfong pink (`#ff66af`) for a prominent action, rather than proving a universal consumer-product interface. [Company](https://www.thepinkfongcompany.com/en/company) · [Business](https://www.thepinkfongcompany.com/en/business)

The company’s identity page supplies CI and BI downloads for The Pinkfong Company, Pinkfong, Baby Shark, and Bebefinn. It also links to an official Pinkfong Baby Shark Font release. That official asset expresses the character side of the brand, while the captured corporate shell uses a loaded Spoqa Han Sans Neo body family plus system-stack controls. The distinction is important: identity assets and one loaded display heading are not a general app type scale or a license to substitute a system font for the named family.

**Key Characteristics:**

- Public corporate pages use white `#ffffff`, black `#000000`, muted gray `#5a5a5a`, and a measured Pinkfong-pink `#ff66af` action.
- `#ff66af` is a selector-backed corporate-action value, not a blanket claim for consumer, app, or franchise controls.
- Spoqa Han Sans Neo is loaded on the corporate capture; the generic system stack is separately observed on many public controls.
- Pinkfong Baby Shark Font is an official distributed brand asset and one loaded corporate-business display use; it is not promoted to the corporate UI family.
- Only corporate-page defaults and their exact selector/surface provenance are documented. Product flows, consumer-site UI, and generic family-site components are omitted.

<!-- design-md:claim primary-tasks kind=user-outcomes count=3 lang=en -->
### Primary tasks

- Find out what the company makes across music, apps, and events
- Download the identity assets for the company or a franchise
- Download the official Baby Shark font for a document
<!-- design-md:claim-end -->

### Do's and Don'ts

### Do

- Preserve the corporate/public source boundary when using the documented controls.
- Use `#ff66af` only where a Pinkfong corporate-action treatment is intended and evidenced.
- Load Spoqa Han Sans Neo before naming a corporate public-text treatment after it.
- Treat Pinkfong Baby Shark Font as a distinct display asset with its own official release and stated-use boundary.
- Keep the recorded selector and route with every component reuse claim.

### Don't

- Do not turn the public corporate CTA into a general consumer-product, checkout, or authenticated-app button.
- Do not infer interaction styling from collector state labels while `interactionCount` is zero.
- Do not call a system-stack heading a Pinkfong font.
- Do not promote the company’s BI downloads or font release into a public component library.
- Do not invent mobile, error, success, loading, or responsive variants from this desktop artifact.

### Brand Narrative

The Pinkfong Company describes itself as a global family-entertainment company working across music, stories, technology, video and audio content, live events, mobile apps, partnerships, and merchandise. Its official identity page groups the company CI with Pinkfong, Baby Shark, and Bebefinn BI assets, showing a portfolio structure rather than a single product surface. [Company](https://www.thepinkfongcompany.com/en/company) · [Business](https://www.thepinkfongcompany.com/en/business)

In 2025, the company released Pinkfong Baby Shark Font for Baby Shark’s tenth anniversary. The release describes a 9-language family with 13,200 characters, fin-inspired triangular details, and a rhythmic visual idea based on the song; it offers the font through the identity page for everyday documents, fan art, and card news. That is an official asset and brand-expression evolution, not evidence that every corporate or consumer control uses the font. [Official font release](https://www.thepinkfongcompany.com/news/pr/207)

### Principles

1. **Connect through joyful content.** The official mission explicitly centers joyful content and entertaining experiences. *UI implication:* corporate public copy should state the content or experience clearly before adding promotional flourish.
2. **Keep portfolio identities distinct.** The company page distributes separate CI/BI assets for the company, Pinkfong, Baby Shark, and Bebefinn. *UI implication:* do not collapse corporate identity assets into a single universal franchise UI palette.
3. **Treat type as an asset with a boundary.** The official font release gives purpose and permitted creative examples, while the corporate capture separately proves a loaded body family. *UI implication:* use a named font only with the evidence class and load/distribution condition that supports it.

### Personas

Official public materials identify **kids and families worldwide** as the audience for joyful content, and enumerate business contexts including content, partnerships, merchandise, live events, and mobile apps. These are public audience and stakeholder cues, not validated individual personas. No fictional personas are added. [Company](https://www.thepinkfongcompany.com/en/company) · [Business](https://www.thepinkfongcompany.com/en/business)

<!-- design-md:section foundations -->
## 2. Foundations

<!-- design-md:claim foundations kind=rules-or-constraints lang=en -->
### Color Palette & Roles

### Observed corporate surfaces

- **Pink action** (`#ff66af`): observed on the public corporate-home primary CTA and on a business-page primary action.
- **Canvas** (`#ffffff`): observed on the family-site pill, business-page outlined action, and mobile-menu dialog.
- **Corporate foreground** (`#000000`): recurrent public corporate text value and the mobile-menu dialog foreground.
- **Muted corporate text** (`#5a5a5a`): recurrent public corporate text value.

### Boundary

The capture does not include Pinkfong consumer pages, an authenticated product, or an official color-specification document that maps these values to semantic states. `#08c7ff` occurs only as the selector-backed corporate-company outline-action foreground; it is retained inside that component record, not elevated to a global color token. The identity-page BI downloads establish asset availability, not a UI palette.
<!-- design-md:claim-end -->

### Depth & Elevation

Most representative corporate controls and the dialog have `box-shadow: none`. Two observed button treatments carry small shadows: the Pinkfong action uses `rgba(255, 5, 88, 0.06) 0px 2px 0px 0px`, while the family-site pill uses `rgba(0, 0, 0, 0.02) 0px 2px 0px 0px`. These are component-local observations, not an elevation scale.

### Motion & Easing

No duration, easing curve, reduced-motion rule, or captured animated state is available in the supplied artifact. Motion tokens are intentionally absent.

<!-- design-md:section typography-assets -->
## 3. Typography & Assets

### Typography Rules

### Evidence classes

- **Live computed surface-use:** the supplied artifact records **Spoqa Han Sans Neo** as `loaded` with high confidence on three corporate-route text elements and corroborates it with 15 Spoqa CDN source URLs. It is the verified corporate-public text family only.
- **Live computed display use:** one corporate-business h1 computes to `BabyShark`, 48px/700/48px, with a loaded `pbs-light.otf` source on the company domain. The official release calls the distributed family **Pinkfong Baby Shark Font**; the naming difference is retained as a source boundary rather than silently normalized.
- **Official distributed asset:** the company announced Pinkfong Baby Shark Font in 2025, describes its fin-inspired triangular form and rhythmic character, and says it is freely downloadable from the company identity page for documents, fan art, and card-news-style work. This is a font-asset and stated-use fact, not a source for uncaptured UI metrics or components. [Official release](https://www.thepinkfongcompany.com/news/pr/207)
- **License boundary:** the current official release describes free download and the listed creative uses but does not establish a broader webfont license in this reference. Separately, the loaded corporate Spoqa Han Sans Neo is distributed by Spoqa under the SIL Open Font License. [Spoqa source and license](https://github.com/spoqa/spoqa-han-sans)
- **Declared/system families:** `-apple-system`, `system-ui`, Segoe UI, Roboto, Helvetica Neue, Noto Sans, emoji families, and Arial appear in computed stacks. They remain system context; do not label a substituted system font as Spoqa Han Sans Neo or Pinkfong Baby Shark Font.

### Observed hierarchy

| Role | Size | Weight | Line height | Source boundary |
|------|------|--------|-------------|-----------------|
| Corporate body | 16px | 400 | 25.144px | Loaded Spoqa Han Sans Neo text on supplied corporate routes |
| Corporate heading | 38px | 700 | 59.717px | Corporate-company h1; computed system stack, not a brand-font token |
| Brand display | 48px | 700 | 48px | One corporate-business h1 computes to loaded `BabyShark`; official distribution is Pinkfong Baby Shark Font |

<!-- design-md:section components-states -->
## 4. Components & States

### Component Stylings

### Public corporate home

**Corporate primary action — observed default**
- Background: #ff66af
- Text: #ffffff
- Radius: 32px
- Padding: 32px 15px
- Font: 24px / 400 / system stack
- Shadow: rgba(255, 5, 88, 0.06) 0px 2px 0px 0px
- States: Observed default only; interactionCount is 0.
- Use: `corporate-home` / `home::[captured element]`; one public corporate CTA with 64px rendered height.

**Family-site pill — observed default**
- Background: #ffffff
- Text: #8c8c8c
- Radius: 32px
- Padding: 4px 20px
- Font: 14px / 400 / system stack
- Shadow: rgba(0, 0, 0, 0.02) 0px 2px 0px 0px
- States: Observed default only; interactionCount is 0.
- Use: `home::[captured element]`, repeated on corporate-home, corporate-company, and corporate-business; 35px rendered height.

### Public corporate-company page

**Business outline action — observed default**
- Background: #ffffff
- Text: #08c7ff
- Radius: 32px
- Padding: 30px 15px
- Font: 18px / 400 / system stack
- States: Collector labels focus, hover, and pressed on `corporate-company` / `surface-2::[captured element]`; interactionCount is 0, so no state value is specified.
- Use: One public corporate-company action with 60px rendered height.

### Shared corporate mobile structure

**Mobile menu dialog — captured structure**
- Background: #ffffff
- Text: #000000
- Padding: 30px
- Font: 14px / 400 / system stack
- Use: `home::div.DefaultMenu_mobile-menu-modal__SEaJA`, a hidden dialog structure captured on all three corporate routes; no opened dialog interaction was captured.

No public consumer-product button, form, card, badge, navigation state, toast, authenticated flow, or general component variant had the required selector plus surface provenance in this update.

The prior reference mixed a historical consumer capture into this corporate-only artifact. This update preserves official brand and font context but retains machine tokens and components only where the 2026-07-13 supplied evidence provides a current selector and surface.

### States

The supplied artifact contains default corporate controls, a hidden mobile-menu dialog structure, one disabled menu-label sample, and collector-labelled focus/hover/pressed entries with `interactionCount: 0`. It does not provide opened-dialog, empty, loading, error, success, toast, form-validation, or product-state evidence. Those specifications are intentionally absent.

<!-- design-md:section layout-platforms -->
## 5. Layout & Platforms

### Layout Principles

The supplied evidence is a single desktop corporate capture. It records spacing clusters at 8px, 20px, and 32px, but does not establish a reusable product grid, consumer-content layout, or mobile breakpoint system. The measured controls above preserve their own padding; no generic card or page-spacing rule is inferred.

### Responsive Behavior

Only a 1440×900 collector viewport was supplied. The artifact includes a hidden mobile-menu dialog structure, but no open-dialog or mobile viewport observation. Breakpoints, touch-target rules, safe-area behavior, and responsive layout changes are intentionally absent.

<!-- design-md:section content-locales -->
## 6. Content & Locales

### Voice & Tone

The official company description ties vivid characters, memorable music, and easy-to-follow movement to family-entertainment content IP. Its English company page says the mission is to connect people through joyful content and entertaining experiences, while the business page presents content, partnership, merchandise, live events, and mobile apps as separate offerings. This supports an optimistic, clear corporate voice that speaks about family enjoyment and content capability without treating all corporate copy as child-facing UI guidance. [Company](https://www.thepinkfongcompany.com/en/company) · [Business](https://www.thepinkfongcompany.com/en/business)

<!-- design-md:section governance -->
## 7. Governance

### Agent Prompt Guide

For a public corporate Pinkfong concept, start from the evidence boundary: white `#ffffff`, black `#000000`, muted `#5a5a5a`, and a selector-backed Pinkfong-pink `#ff66af` action. Use the specific corporate CTA, family-site pill, or business outline action only with its recorded route and default-state limitation. Load Spoqa Han Sans Neo only when the verified source can be loaded; use Pinkfong Baby Shark Font as an official display asset only within its stated distribution boundary. Do not generate a Pinkfong consumer site, child-facing app, purchase flow, status system, or generic character-card library from this reference.

<!-- design-md:claim authority kind=evidence-backed-reconstruction lang=en -->

### Authority



This document is an evidence-backed reconstruction, not authority for an unrelated target project.

<!-- design-md:claim-end -->

<!-- design-md:claim application-priority order=prompt-fact,repository-fact,system-contract,reference-inspiration lang=en -->

### Application priority



1. Direct user instructions for the requested scope.

2. Repository facts.

3. This system contract.

4. Reference inspiration.

<!-- design-md:claim-end -->

<!-- design-md:claim unknowns policy=absent-at-smallest-unresolved-boundary lang=en -->

### Unknowns



Omit only the smallest unresolved value or group. Do not replace it with a plausible default.

<!-- design-md:claim-end -->

<!-- design-md:claim changes policy=review-record-validate-before-adoption lang=en -->

### Changes



Record, review, and validate changes before adoption.

<!-- design-md:claim-end -->
