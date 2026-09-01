# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** FlyCure
**Updated:** 2026-09-01
**Category:** Luxury medical travel / hospital marketplace
**Direction:** Editorial Clinic (hospital annual report × travel magazine)

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#0F5C5A` | `--color-primary` |
| On Primary | `#F6F1E8` | `--color-on-primary` |
| Secondary | `#134E4A` | `--color-secondary` |
| Accent / brass | `#C4A574` | `--color-accent` |
| Background | `#F6F1E8` | `--color-background` |
| Foreground | `#1C1917` | `--color-foreground` |
| Muted | `#EDE6D9` | `--color-muted` |
| Muted FG | `#6B645C` | `--color-muted-fg` |
| Border | `#E0D6C6` | `--color-border` |
| Surface / paper | `#FFFbf5` | `--color-surface` |
| Destructive | `#B42318` | `--color-destructive` |
| Ring | `#0F5C5A` | `--color-ring` |
| Success | `#3F6F4A` | `--color-success` |

**Color Notes:** Warm ivory paper, near-black ink, deep teal CTAs, thin brass rules. No cyan HUD glow, no purple AI gradients.

### Typography

- **Heading Font:** Fraunces
- **Body / UI Font:** DM Sans
- **Mood:** editorial, calm, hospital-grade, travel-luxury
- **Google Fonts:** https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400&display=swap

### Style

- Full-bleed photography with soft scrims
- Photo-led cards with caption overlays
- Generous whitespace and thin brass dividers
- 44×44 touch targets, visible focus rings, reduced-motion support
- Rounded corners stay modest (`10–16px`)

### Avoid

- Dark HUD grids, neon glow, glass-cyber panels
- Purple / pink AI gradients
- Emoji icons
- Jargon like “care console”, “specialty matrix”, “transmit needs”

### Motion

- Reveal-up 400–500ms on listings
- Soft hover lift 180–240ms
- No status-dot pulse
