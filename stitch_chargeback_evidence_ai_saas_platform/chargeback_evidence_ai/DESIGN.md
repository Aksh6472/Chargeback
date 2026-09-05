---
name: Chargeback Evidence AI
colors:
  surface: '#f8f9fb'
  surface-dim: '#d9dadc'
  surface-bright: '#f8f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#edeef0'
  surface-container-high: '#e7e8ea'
  surface-container-highest: '#e1e2e4'
  on-surface: '#191c1e'
  on-surface-variant: '#43474b'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f3'
  outline: '#74777b'
  outline-variant: '#c4c7cb'
  surface-tint: '#556069'
  primary: '#1a242c'
  on-primary: '#ffffff'
  primary-container: '#2f3a42'
  on-primary-container: '#98a4ad'
  inverse-primary: '#bcc8d2'
  secondary: '#535f70'
  on-secondary: '#ffffff'
  secondary-container: '#d7e3f7'
  on-secondary-container: '#596576'
  tertiary: '#002a1a'
  on-tertiary: '#ffffff'
  tertiary-container: '#00422b'
  on-tertiary-container: '#10b981'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e4ee'
  primary-fixed-dim: '#bcc8d2'
  on-primary-fixed: '#121d24'
  on-primary-fixed-variant: '#3d4850'
  secondary-fixed: '#d7e3f7'
  secondary-fixed-dim: '#bbc7da'
  on-secondary-fixed: '#101c2a'
  on-secondary-fixed-variant: '#3c4857'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9fb'
  on-background: '#191c1e'
  surface-variant: '#e1e2e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-xs-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.06em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  space-2xs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 2.5rem
  space-3xl: 3rem
  gutter-desktop: 1.5rem
  margin-desktop: 2rem
  sidebar-width: 260px
---

## Brand & Style

This design system embodies quiet confidence, precision, and enterprise-grade security. Designed specifically for automated dispute mitigation and chargeback evidence generation, the visual language avoids flashy or decorative trends in favor of an institutional, highly structured aesthetic. It communicates stability, compliance, and effortless power.

Key characteristics:
- **Design Philosophy:** Minimalist Corporate with subtle tactile depth. Interfaces favor breathing room, crystalline typography, and razor-sharp alignment.
- **Atmosphere:** High-trust, analytical, calm, and rigorous. There are no distracting bright accents or noisy gradients; visual momentum is guided solely by content priority and deliberate spatial cadence.
- **Emotional Intent:** Reduces the operational stress of financial disputes. Teams should feel immediate clarity, control, and audit-ready certainty.

## Colors

The palette employs a restrained, tonal hierarchy that centers around deep blue-grays, crisp whites, and clinical status accents.

- **Primary Canvas & Surfaces:**
  - Application Canvas (`#F7F8FA`): A calibrated, neutral off-white providing balanced contrast without stark eye fatigue.
  - Card & Container Surface (`#FFFFFF`): Crisp white applied to panels, cards, and modal views to cleanly separate data surfaces from the canvas.
  - Shell / Sidebar (`#2D3948`): A dark, desaturated navy-gray anchoring persistent navigation with institutional gravity.

- **Brand & Structural Neutrals:**
  - Primary Slate (`#2F3A42`): The primary ink tone for headings, critical actions, and key focal points.
  - Secondary Slate (`#64748B`): Muted mid-tone for body secondary copy, inactive icons, metadata, and structural micro-copy.
  - Structural Border (`#E5E7EB`): A whisper-thin, neutral hairline dividing cards, rows, and functional compartments.

- **Functional Status Indicators:**
  - Success / Win Rate (`#10B981`): Subtle, desaturated emerald used for positive win-rate differentials, recovered funds, and confirmed submissions.
  - Warning / Under Review (`#F59E0B`): Muted amber indicating impending submission deadlines and pending merchant actions.
  - Risk / Dispute Loss (`#EF4444`): Controlled, muted red signaling high chargeback liability, missing evidence fragments, or lost arbitration.

## Typography

Inter serves as the sole workhorse typeface across the system, complemented by JetBrains Mono for ARN numbers, transaction hashes, and evidence timestamps.

- **Weight Discipline:** Headings employ bold (`700`) and semi-bold (`600`) weights with tightened letter tracking (`-0.015em` to `-0.025em`) to evoke technical discipline and executive authority.
- **Data Scannability:** Financial figures and table data utilize tabular figures (`tnum`) to ensure perfect vertical alignment across ledger and audit logs.
- **Labels & Categorization:** Overlines, status indicators, and dispute lifecycle tags use `label-xs-caps` with uppercase transformations and generous letter tracking (`0.06em`) for crystalline readability at small viewports.

## Layout & Spacing

The layout is grounded in a 12-column responsive fluid grid pinned within a structured shell layout. Enterprise density is prioritized without sacrificing whitespace.

- **Shell Architecture:**
  - Persistent left-hand sidebar fixed at 260px (`#2D3948`) containing core system modules (Disputes, Packet Builder, Analytics, Integrations).
  - Main workspace with dynamic padding: 32px on desktop monitors, reducing to 20px on tablet layouts.
- **Grid & Alignment:**
  - Content containers use a maximum width of `1600px` for ultra-wide monitors to maintain optimal line lengths.
  - Multi-panel workspaces (e.g., dispute feed alongside live PDF evidence preview) operate on balanced split-column ratios (e.g., 5-column list / 7-column evidence dossier).
- **Responsive Adaptations:**
  - Below 1024px, the sidebar collapses to a condensed 64px icon dock or overlay drawer. Split panels transition into stacked tabs.

## Elevation & Depth

This design system avoids heavy shadows, saturated glows, and blur effects. Depth is expressed through structural layering:

- **Level 0 (Base Canvas):** `#F7F8FA` background fill. Completely flat.
- **Level 1 (Card & Module Layer):** `#FFFFFF` fill bounded by a 1px micro-border (`#E5E7EB`). A subtle ambient drop shadow (`0 1px 3px 0 rgba(47, 58, 66, 0.04), 0 1px 2px -1px rgba(47, 58, 66, 0.02)`) provides clean separation.
- **Level 2 (Hover & Contextual Popovers):** Elevates interactive cards and action menus using `0 4px 12px -2px rgba(47, 58, 66, 0.08), 0 2px 6px -1px rgba(47, 58, 66, 0.04)` with an identical micro-border.
- **Level 3 (Modals & Slide-out Dossiers):** Deep overlay layer with `0 20px 25px -5px rgba(47, 58, 66, 0.1), 0 8px 10px -6px rgba(47, 58, 66, 0.04)` backed by a muted backdrop (`rgba(45, 57, 72, 0.4)`).

## Shapes

The shape system balances modern approachability with enterprise restraint through moderate corner radii:

- **Cards & Data Modules:** 12px to 16px corner radius (`rounded-md` to `rounded-lg`).
- **Interactive Controls (Buttons, Inputs, Selects):** Standardized at 8px to 10px to retain precision and visual discipline.
- **Status Pills & Micro Badges:** Standardized at 6px or full pill (9999px) strictly for concise category tags.
- **Micro-borders:** All containers, cards, and input boundaries feature a consistent 1px hairline stroke, anchoring elements cleanly against the soft off-white background.

## Components

### Buttons
- **Primary:** Solid `#2F3A42` fill, `#FFFFFF` text, subtle hover shift to `#242E35`. Focus ring uses a 2px offset in `#64748B`.
- **Secondary:** `#FFFFFF` background, `#2F3A42` text, 1px `#E5E7EB` border. Subtle hover to `#F7F8FA`.
- **Destructive / Dispute Abandon:** Muted red surface (`#FEF2F2`), `#EF4444` text, 1px border (`#FCA5A5`).
- **Dimensions:** 36px default height for dense enterprise views; 44px for primary page actions.

### Data Chips & Status Badges
- **Status Indicator Badges:** Minimalist, low-saturation pill styles:
  - *Won / Evidence Accepted:* `#ECFDF5` fill, `#065F46` text, `#A7F3D0` micro-border.
  - *Pending Evidence / Warning:* `#FFFBEB` fill, `#92400E` text, `#FDE68A` micro-border.
  - *Lost / Escalated:* `#FEF2F2` fill, `#991B1B` text, `#FECACA` micro-border.
- Badges feature a trailing or leading 6px status dot for accessibility across monochrome modes.

### Form Inputs & Selects
- Background `#FFFFFF`, border 1px `#E5E7EB`, text `#2F3A42`, placeholder `#94A3B8`.
- Focus state activates a crisp `#2F3A42` border with an ambient outer ring: `box-shadow: 0 0 0 3px rgba(47, 58, 66, 0.08)`.
- Label placed directly above in `label-md` weight, rendered in `#2F3A42`.

### Evidence Cards & Data Dossiers
- Structured with a distinct header containing claim ID, cardholder identifier, and countdown timer.
- Separated internally via 1px `#E5E7EB` dividers instead of heavy visual blocks.
- Card padding set to a generous 24px (`space-lg`) to maintain clear operational focus.

### Data Tables & Audit Ledgers
- Row height: 48px for standard density; row border: 1px `#E5E7EB`.
- Row hover: Subtle transition to `#F7F8FA`.
- Headers: `label-xs-caps` uppercase text in `#64748B` with ascending/descending sort triggers.

### Evidence Packet Timeline / Tree
- Vertical connecting line in 1.5px `#E5E7EB`.
- Milestone nodes highlighted with deep slate circles or contextual status greens, tracking webhook reception, automated OCR extraction, and gateway submission.