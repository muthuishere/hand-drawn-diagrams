# Page Mockup Diagrams

Use this when the user wants a hand-drawn page mockup, landing page sketch, dashboard sketch, or webpage-like composition rather than a pure systems diagram.

Output should look like a rough webpage, not a flowchart: visible sections, UI hierarchy, and realistic component placement.

Shape vocabulary: start from `references/fundamental-shapes.md`, then adapt those shapes into UI blocks.

## Special Rule

Default skill behavior is monochrome.

For page mockup diagrams only, color is allowed when the user explicitly wants webpage-like fidelity, stronger UX communication, or visual emphasis.

Keep these constraints even when using color:
- same hand-drawn font family
- same rough/sketch feeling
- limited palette
- color supports hierarchy, not decoration

Wireframe note:
- If the user says `wireframe`, default to monochrome or near-monochrome first.
- If the user says `page mockup`, `landing page`, or explicitly asks for richer webpage fidelity, restrained color is allowed.

## One Big Idea

One mockup diagram should explain one page only.

Examples:
- landing page
- dashboard home
- pricing page
- onboarding page
- checkout page

## Best Default Layout

Default flow: top-to-bottom page structure

```text
[Header / Nav]
[Hero]
[Primary content]
[Secondary section]
[CTA / Footer]
```

Reveal order:
1. Hero section
2. Primary action
3. Supporting sections
4. Footer or closing CTA

## Must Show

- one dominant page purpose
- one hero section
- one primary CTA
- 3-6 page sections max
- clear hierarchy between headline, content, and action

## Never Draw

- every section with the same size and weight
- too many small labels floating everywhere
- generic wireframe boxes with no page rhythm

## Fundamental Shape Mapping For UI

- `rectangle`: card, hero block, panel, section, form area
- `ellipse`: badge, avatar, icon spot, accent chip
- `line`: dividers, navbar separators, chart axes, layout rhythm
- `diamond`: use rarely, only if a page includes explicit decision logic
- `arrow`: only for interaction explanation or page flow overlays
- `frame`: use for major page zones or alternative screen states
- `text`: headings, labels, short content, CTA text

## Color Rules

Use color only if explicitly requested.

When color is used:
- keep one base background
- one primary accent color
- one secondary support color max
- keep text readable
- avoid rainbow UI

Recommended page-mockup palette pattern:
- Base background: white or very light neutral
- Primary text: near-black
- Primary accent: one saturated button/action color
- Secondary accent: one support color for chips, charts, or active states

Recommended wireframe palette pattern:
- White background
- Near-black text and strokes
- Light gray surfaces
- Optional one muted accent for CTA or active tab only

Good uses of color:
- CTA emphasis
- active nav state
- chart bars or stats
- hero highlight
- status chips
- selected plan card
- active step in onboarding or checkout

Bad uses of color:
- every card different
- multicolor text
- decorative gradients with no communicative value
- full marketing-art direction inside a rough wireframe

## Canonical Recipes

### 1. Landing page mockup
Structure: `Header -> Hero -> Proof -> Features -> CTA -> Footer`

### 2. Dashboard mockup
Structure: `Top bar -> KPI row -> main chart/content -> side panel or recent activity`

### 3. Pricing page mockup
Structure: `Header -> Pricing hero -> plan cards -> FAQ -> CTA`

### 4. Checkout or signup page
Structure: `Header -> focused form -> reassurance/supporting detail -> submit action`

### 5. Wireframe-style page
Structure: `Header -> hero/content block -> supporting block -> CTA`, using mostly monochrome with optional one muted accent

## Hard Limits

- Sections: 3-6
- Primary CTAs: 1-2
- Accent colors: 1-2
- Major cards/panels in one viewport: 6 max
- Annotation arrows: 3 max
- Distinct button styles: 2 max

## UX Quality Rules

- one obvious primary action
- one strongest visual region
- supporting sections should reduce doubt, not compete with the hero
- spacing should communicate importance
- if comparison helps, use before/after or plan-vs-plan instead of extra explanation text

## Bad vs Better Prompt

Bad:
"Make a website mockup."

Better:
"Create a hand-drawn landing page mockup for a SaaS product with the same sketch font, one hero CTA, 5 sections, and limited accent color for the button and highlights."

Wireframe version:
"Create a hand-drawn wireframe for a pricing page using the same sketch font, 4 sections, monochrome layout blocks, and one muted accent for the main CTA."

## Cut Ruthlessly

Remove in this order:
1. extra sections
2. secondary buttons
3. decorative accents that do not improve hierarchy

## Minimum Viable Output

- header
- hero
- one supporting section
- one CTA

## Acceptance Check

- Does it read like a webpage before reading every label?
- Is the page purpose obvious in the hero?
- Is there one clear primary action?
- If color is used, does it improve hierarchy instead of decoration?
