# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** FlyCure
**Updated:** 2026-08-11
**Category:** Futuristic Med-Tech / Hospital Marketplace
**Direction:** Clinical HUD × Soft UI Evolution (hospital imaging suite aesthetic)

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#22D3EE` | `--color-primary` |
| On Primary | `#041016` | `--color-on-primary` |
| Secondary | `#38BDF8` | `--color-secondary` |
| Accent/CTA | `#2DD4BF` | `--color-accent` |
| Background | `#070B14` | `--color-background` |
| Foreground | `#E8F4F8` | `--color-foreground` |
| Muted | `#121A28` | `--color-muted` |
| Muted FG | `#8BA3B5` | `--color-muted-fg` |
| Border | `rgba(56, 189, 248, 0.28)` | `--color-border` |
| Surface / Glass | `rgba(14, 22, 36, 0.78)` | `--color-surface` |
| Destructive | `#F87171` | `--color-destructive` |
| Ring | `#22D3EE` | `--color-ring` |
| Success | `#34D399` | `--color-success` |

**Color Notes:** Deep hospital night + diagnostic cyan (MRI/OR monitor vibe). No purple. Soft teal CTAs keep it clinical, not cyberpunk.

### Typography

- **Heading Font:** Space Grotesk
- **Body Font:** DM Sans
- **Meta / Data:** JetBrains Mono
- **Mood:** futuristic med-tech, precise, hospital-grade, innovative
- **Google Fonts:** https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap

### Style

**Hybrid:** Soft UI Evolution depth + restrained clinical HUD cues

- Glass panels with hairline cyan borders
- Subtle grid / radial glow atmosphere (not neon overload)
- Corner tech markers on featured cards
- Soft shadows with cyan tint
- 44×44 touch targets, visible focus rings, reduced-motion support

### Avoid

- Purple / pink AI gradients
- Matrix green cyberpunk / glitch overload
- Emoji icons
- Harsh neon text glow on body copy

### Motion

- Reveal-up 350–500ms on listings
- Soft hover lift 180–240ms
- Optional slow pulse on status dots only
