# FlyCure — UI Design Requirements

**Purpose:** Implementation reference for the FlyCure visual system.  
**Scope:** Colour codes, gradients, typography tokens, surfaces, borders, shadows, and reusable CSS.  
**Out of scope:** Product requirements, user journeys, feature descriptions, screen specifications, and PRD content.

## 1. Colour palette

| CSS token | Hex | Use |
|---|---|---|
| `--fc-emerald-900` | `#0B3D33` | Deep header/footer, high-emphasis brand surface |
| `--fc-emerald-800` | `#0F5145` | Dark brand interactions |
| `--fc-emerald-700` | `#0F5D4E` | Primary brand colour and primary buttons |
| `--fc-emerald-600` | `#167461` | Hover/active brand states |
| `--fc-emerald-100` | `#E8F1ED` | Soft brand background |
| `--fc-emerald-050` | `#F3F7F4` | Very light brand-tinted surface |
| `--fc-champagne-500` | `#C6A879` | Premium accent, small highlights |
| `--fc-champagne-100` | `#F2EBDD` | Warm accent background |
| `--fc-ivory-100` | `#F7F5EF` | Main application background |
| `--fc-ivory-200` | `#F1EFE8` | Muted surface |
| `--fc-white` | `#FFFFFF` | Cards, forms, dialogs |
| `--fc-text-primary` | `#1F2927` | Main text |
| `--fc-text-secondary` | `#68736F` | Supporting text |
| `--fc-border` | `#E4E4DC` | Standard borders/dividers |
| `--fc-success` | `#167A52` | Success states |
| `--fc-warning` | `#A96B16` | Warning/pending states |
| `--fc-error` | `#B93832` | Error/destructive states |
| `--fc-info` | `#28658A` | Informational states |

Use emerald for primary actions and navigation accents. Use champagne sparingly; never use it for small text on ivory or white. Status colours must be paired with text or an icon.

## 2. Gradient tokens

| CSS token | Value | Use |
|---|---|---|
| `--fc-gradient-brand` | `linear-gradient(120deg, #0B3D33 0%, #0F5D4E 55%, #167461 100%)` | Primary brand hero or feature band |
| `--fc-gradient-brand-soft` | `linear-gradient(135deg, #F3F7F4 0%, #E8F1ED 100%)` | Soft brand panels |
| `--fc-gradient-warm` | `linear-gradient(120deg, #F7F5EF 0%, #F2EBDD 100%)` | Editorial/concierge surfaces |
| `--fc-gradient-hero-overlay` | `linear-gradient(90deg, rgba(11,61,51,.88) 0%, rgba(11,61,51,.48) 54%, rgba(11,61,51,0) 100%)` | Text legibility over hero photography |
| `--fc-gradient-card-highlight` | `linear-gradient(145deg, #FFFFFF 0%, #F7F5EF 100%)` | Featured cards |

Do not apply gradients to every card. Most content surfaces should remain flat white or ivory.

## 3. Typography tokens

- UI font: **Manrope**.
- Display font: **Playfair Display**.
- Use Playfair Display for selected large editorial headings only.
- Use Manrope for body, navigation, forms, labels, buttons, and data.

| Token | Value |
|---|---|
| `--fc-font-ui` | `"Manrope", Arial, sans-serif` |
| `--fc-font-display` | `"Playfair Display", Georgia, serif` |
| `--fc-text-xs` | `0.75rem` |
| `--fc-text-sm` | `0.875rem` |
| `--fc-text-base` | `1rem` |
| `--fc-text-lg` | `1.125rem` |
| `--fc-text-xl` | `1.25rem` |
| `--fc-heading-sm` | `1.5rem` |
| `--fc-heading-md` | `2rem` |
| `--fc-heading-lg` | `2.5rem` |
| `--fc-heading-xl` | `clamp(2.5rem, 5vw, 3.5rem)` |

## 4. Layout and component tokens

| Token | Value |
|---|---|
| `--fc-container` | `1200px` |
| `--fc-radius-sm` | `8px` |
| `--fc-radius-md` | `12px` |
| `--fc-radius-lg` | `16px` |
| `--fc-radius-xl` | `24px` |
| `--fc-radius-pill` | `999px` |
| `--fc-shadow-card` | `0 4px 18px rgba(31, 41, 39, .05)` |
| `--fc-shadow-hover` | `0 12px 32px rgba(31, 41, 39, .10)` |
| `--fc-shadow-overlay` | `0 20px 60px rgba(11, 35, 30, .18)` |
| `--fc-space-1` | `4px` |
| `--fc-space-2` | `8px` |
| `--fc-space-3` | `12px` |
| `--fc-space-4` | `16px` |
| `--fc-space-6` | `24px` |
| `--fc-space-8` | `32px` |
| `--fc-space-10` | `40px` |
| `--fc-space-12` | `48px` |
| `--fc-space-16` | `64px` |
| `--fc-space-20` | `80px` |

## 5. Copy-paste CSS foundation

```css
@import url("https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap");

:root {
  color-scheme: light;

  --fc-emerald-900: #0B3D33;
  --fc-emerald-800: #0F5145;
  --fc-emerald-700: #0F5D4E;
  --fc-emerald-600: #167461;
  --fc-emerald-100: #E8F1ED;
  --fc-emerald-050: #F3F7F4;

  --fc-champagne-500: #C6A879;
  --fc-champagne-100: #F2EBDD;

  --fc-ivory-100: #F7F5EF;
  --fc-ivory-200: #F1EFE8;
  --fc-white: #FFFFFF;

  --fc-text-primary: #1F2927;
  --fc-text-secondary: #68736F;
  --fc-border: #E4E4DC;

  --fc-success: #167A52;
  --fc-warning: #A96B16;
  --fc-error: #B93832;
  --fc-info: #28658A;

  --fc-gradient-brand: linear-gradient(120deg, #0B3D33 0%, #0F5D4E 55%, #167461 100%);
  --fc-gradient-brand-soft: linear-gradient(135deg, #F3F7F4 0%, #E8F1ED 100%);
  --fc-gradient-warm: linear-gradient(120deg, #F7F5EF 0%, #F2EBDD 100%);
  --fc-gradient-hero-overlay: linear-gradient(90deg, rgba(11,61,51,.88) 0%, rgba(11,61,51,.48) 54%, rgba(11,61,51,0) 100%);
  --fc-gradient-card-highlight: linear-gradient(145deg, #FFFFFF 0%, #F7F5EF 100%);

  --fc-font-ui: "Manrope", Arial, sans-serif;
  --fc-font-display: "Playfair Display", Georgia, serif;

  --fc-container: 1200px;
  --fc-radius-sm: 8px;
  --fc-radius-md: 12px;
  --fc-radius-lg: 16px;
  --fc-radius-xl: 24px;
  --fc-radius-pill: 999px;

  --fc-shadow-card: 0 4px 18px rgba(31, 41, 39, .05);
  --fc-shadow-hover: 0 12px 32px rgba(31, 41, 39, .10);
  --fc-shadow-overlay: 0 20px 60px rgba(11, 35, 30, .18);

  --fc-space-1: 4px;
  --fc-space-2: 8px;
  --fc-space-3: 12px;
  --fc-space-4: 16px;
  --fc-space-6: 24px;
  --fc-space-8: 32px;
  --fc-space-10: 40px;
  --fc-space-12: 48px;
  --fc-space-16: 64px;
  --fc-space-20: 80px;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  background: var(--fc-ivory-100);
  color: var(--fc-text-primary);
  font-family: var(--fc-font-ui);
  font-size: 1rem;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, .fc-display {
  font-family: var(--fc-font-display);
  font-weight: 600;
  line-height: 1.15;
  color: var(--fc-emerald-900);
}

a { color: var(--fc-emerald-700); text-decoration-thickness: .08em; text-underline-offset: .18em; }

:focus-visible {
  outline: 3px solid var(--fc-champagne-500);
  outline-offset: 3px;
}

.fc-container {
  width: min(calc(100% - 2rem), var(--fc-container));
  margin-inline: auto;
}

.fc-surface {
  background: var(--fc-white);
  border: 1px solid var(--fc-border);
  border-radius: var(--fc-radius-lg);
  box-shadow: var(--fc-shadow-card);
}

.fc-surface--warm { background: var(--fc-gradient-warm); }
.fc-surface--brand { background: var(--fc-gradient-brand); color: var(--fc-white); }

.fc-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  min-height: 44px;
  padding: .7rem 1.1rem;
  border: 1px solid transparent;
  border-radius: var(--fc-radius-md);
  font: 700 .9rem/1.2 var(--fc-font-ui);
  cursor: pointer;
  transition: background-color .18s ease, box-shadow .18s ease, transform .18s ease;
}

.fc-button--primary {
  background: var(--fc-emerald-700);
  color: var(--fc-white);
}
.fc-button--primary:hover {
  background: var(--fc-emerald-800);
  box-shadow: var(--fc-shadow-card);
}
.fc-button--secondary {
  background: var(--fc-white);
  color: var(--fc-emerald-800);
  border-color: var(--fc-emerald-700);
}
.fc-button--secondary:hover { background: var(--fc-emerald-050); }

.fc-input {
  width: 100%;
  min-height: 46px;
  padding: .7rem .9rem;
  border: 1px solid var(--fc-border);
  border-radius: var(--fc-radius-md);
  background: var(--fc-white);
  color: var(--fc-text-primary);
  font: 500 .95rem var(--fc-font-ui);
}
.fc-input:focus {
  outline: 2px solid var(--fc-emerald-600);
  outline-offset: 1px;
  border-color: var(--fc-emerald-600);
}

.fc-muted { color: var(--fc-text-secondary); }
.fc-tag {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: .25rem .65rem;
  border-radius: var(--fc-radius-pill);
  background: var(--fc-emerald-100);
  color: var(--fc-emerald-900);
  font-size: .75rem;
  font-weight: 700;
}

@media (max-width: 767px) {
  .fc-container { width: min(calc(100% - 1.25rem), var(--fc-container)); }
  .fc-hide-mobile { display: none !important; }
}
```

**Font hosting note:** The `@import` is convenient for local prototyping. For production, consider self-hosting licensed font files and defining `@font-face` to improve privacy, reliability, and performance.

## 6. Component styling rules

- **Header:** deep emerald surface, white wordmark/navigation, restrained active underline or text colour.
- **Page background:** warm ivory; use white for content cards and form surfaces.
- **Primary CTA:** emerald fill; one dominant primary action per visual region.
- **Secondary CTA:** white surface with emerald border.
- **WhatsApp CTA:** use the official WhatsApp brand treatment only for the WhatsApp action; retain a text label.
- **Cards:** 1 px neutral border, 12–16 px radius, minimal shadow; increase elevation only on hover when clickable.
- **Filters:** quiet neutral controls; active filter uses soft emerald background and a clear selected state.
- **Badges:** compact and restrained; use only for meaningful metadata/status.
- **Forms:** persistent labels, clear help/error text, 44 px minimum control height.
- **Tables/lists:** generous row spacing, subtle dividers, avoid dense dashboard grids.
- **Photography:** consistent aspect ratios and intentional crops; never overlay text without a tested contrast layer.

## 7. Responsive breakpoints

```css
/* Mobile first */
@media (min-width: 768px) { /* tablet and up */ }
@media (min-width: 1024px) { /* desktop and up */ }
@media (min-width: 1280px) { /* wide desktop */ }
```

Use responsive layout behaviour rather than designing fixed-width pages. The breakpoints above are starting points; validate them against actual content.

## 8. Iconography

Use **Lucide** consistently. Standard sizes: 16 px for inline metadata, 18–20 px for controls, 22–24 px for feature icons. Use one stroke weight consistently. Icons should support labels, not replace them.

## 9. Implementation notes

- Keep these tokens in one shared stylesheet, e.g. `static/css/design-tokens.css`.
- Keep component rules in a shared stylesheet, e.g. `static/css/components.css`.
- Reuse Django template partials for buttons, cards, form fields, tags, navigation, and alerts.
- Avoid inline colour values in templates; use the CSS variables.
- Keep interaction states visible and keyboard accessible.
- Use reduced-motion-aware transitions and avoid animation that blocks task completion.
