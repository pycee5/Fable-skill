---
name: fable-ui-design
description: How to design and build user interfaces that are clear, usable, accessible and deliberate rather than generic. Use for any work a person will look at or interact with - web pages, components, forms, dashboards, landing pages, mobile screens, emails, design systems, CSS and styling fixes, responsive layout, dark mode, accessibility - and for any request to make something look better, cleaner, more modern or more professional. Also use when reviewing or critiquing an interface. Covers hierarchy, layout, spacing, typography, color, component states and how to verify by rendering and looking. Bundles a contrast checker, a multi-viewport screenshot script and starter design tokens.
---

# UI Design

An interface is good when a person can see what matters, understand what they can do, and do it without friction - on their device, in their conditions. That comes from a small number of decisions made deliberately and applied consistently, not from decoration.

You cannot judge an interface from its code. The last step of every UI task is to render it and look.

## 1. Before any pixels

- **Who, what, where**: who uses this, to do what, on which device, how often? A dashboard used all day wants density; a checkout used once wants guidance.
- **The one thing**: what is the most important thing on this screen, and what is the primary action? If you can't say, the design won't be able to either.
- **Real content**: design with realistic data - the long name, the empty list, the seven-digit number, the error. A layout that only works with tidy placeholder text isn't finished.
- **What exists**: if the project has a design system, component library, tokens or brand, use them. Look at two or three existing screens and match their spacing, type and components. Never invent a color, radius or spacing value where a token exists. Only when there is nothing, start from `assets/tokens.css` (in this skill's directory) and adapt it.

## 2. Hierarchy

This is the core skill. Everything on a screen has a rank, and the eye should find the ranks in order.

- One focal point per view. One primary button per view; other actions are styled as secondary or tertiary.
- Rank with size, weight, contrast and space - usually two of these, not all at once.
- De-emphasise the secondary rather than shouting the primary. Muted color and smaller size for metadata and helper text make the main content stand out by itself.
- Squint at it, or blur a screenshot: what stays visible should be what matters, in order of importance.
- A label is less important than its value. Don't give "Email" the same weight as the address.

## 3. Layout and spacing

- **Use a spacing scale and only the scale**: 4, 8, 12, 16, 24, 32, 48, 64. Arbitrary values (13px, 22px) are what makes a layout look slightly off.
- **Proximity means relationship.** Space inside a group is smaller than space between groups. A label sits closer to its own field than to the one above.
- **Align to few lines.** Shared left edges, a consistent grid, consistent widths for repeated things.
- **Whitespace before borders.** Separate with space first, then a subtle background change, then a border. Boxes inside boxes inside boxes is noise.
- **Constrain text** to 60-75 characters a line for reading, and constrain content width on large screens rather than stretching it.
- **Left-align by default.** Centre only short, standalone things: a hero line, an empty state.
- Lay out with flexbox and grid, `gap` for spacing, and intrinsic sizing (`minmax`, `clamp`, `auto-fit`) rather than fixed pixel widths.

## 4. Typography

- One typeface is enough; two at most. A system font stack is a perfectly good choice.
- A type scale with few steps, such as 12 / 14 / 16 / 20 / 24 / 32 / 48. Body text 16px on the web; rarely below 14 for anything meant to be read.
- Line height around 1.5 for body text and 1.1-1.3 for headings: tighter as the text gets larger.
- Two or three weights. Build hierarchy with weight and color before reaching for size.
- Tabular numerals for columns of numbers; right-align numbers that will be compared.
- Avoid long passages that are all caps, centred, justified or light gray.

## 5. Color

- **Neutrals do most of the work**: a ramp of grays for backgrounds, borders and text. One accent, used sparingly, for the primary action, links and focus. Semantic colors for success, warning and danger, used only with those meanings.
- **Name by role, not hue**: `--surface`, `--text`, `--text-muted`, `--border`, `--accent`, `--danger`. That is what makes theming and dark mode possible.
- **Measure contrast; don't eyeball it.** 4.5:1 for body text; 3:1 for large text (24px, or 19px bold) and for control boundaries and meaningful icons. Check a pair with `python3 scripts/contrast.py "#6b7280" "#ffffff"`.
- **Never color alone.** Pair it with text, an icon or a shape - for errors, status, chart series, required fields.
- **Dark mode is a second design, not an inversion.** Dark gray rather than pure black; off-white text; raise a surface by making it lighter, not by adding shadow; desaturate accents a little; re-check every contrast pair.

## 6. Components and their states

A component is designed when all its states are. Before calling UI done, account for:

- **Interactive elements**: default, hover, focus-visible, active, disabled, loading.
- **Data views**: loading (a skeleton or spinner in the layout's final shape), empty (say what belongs here and how to add it), error (what happened and how to retry), partial, and overflowing (long text, hundreds of items).
- **Forms**: a visible label for every field (placeholder text is not a label); help text before the error, not only after it; validation on blur or submit rather than on every keystroke; the message beside the field, saying how to fix it; input preserved after an error; the right input type and autocomplete attributes.
- **Feedback**: every action gets a visible response within about a tenth of a second - a pressed state, a spinner, an optimistic update. Destructive actions get a confirmation or, better, an undo.
- **Consistency**: the same thing looks and behaves the same everywhere. Things that look clickable are, and things that are clickable look it.

## 7. Accessibility is part of the design

- **Semantic HTML first**: `button` for actions, `a` for navigation, `label` tied to its input, headings in order, `nav` and `main` landmarks, real lists and tables. ARIA only where semantics don't reach.
- **Keyboard**: everything reachable and operable; a logical tab order; a clearly visible focus ring (never remove the outline without replacing it); Escape closes overlays; focus moves into a dialog and returns afterwards.
- **Names**: alt text on meaningful images; an accessible name on every icon-only button.
- **Targets**: at least 44 by 44 px for touch.
- **Motion**: short (150-250 ms) and purposeful; honor `prefers-reduced-motion`.
- **Zoom**: usable at 200% and with larger system text. Sizes in `rem`; no fixed pixel heights around text.

## 8. Responsive

Design the narrow layout as seriously as the wide one. Check at about 375, 768 and 1280 or more wide. The page must not scroll sideways; text must not clip or overlap; touch targets must be large enough; tables need a narrow-screen answer (scroll inside their container, stack, or drop columns); images need dimensions so the layout doesn't jump.

## 9. Avoiding the generic look

Interfaces made on autopilot share a look: a purple-to-blue gradient, everything centred, every item in a rounded card with a shadow, emoji as icons, three equal feature boxes, heavy drop shadows, a dozen font sizes. None of that is a decision.

Make decisions instead. Pick a direction that suits the product - dense and utilitarian, calm and editorial, warm and friendly - and carry it through type, spacing, color and shape. Use restraint: fewer colors, fewer sizes, fewer boxes; more alignment and space. When the user gives a reference or a brand, follow it closely. When they give none, a quiet, well-ordered design beats an ornate one.

## 10. Verify by looking

1. **Render it** in a real browser. Use whatever browser or screenshot tool the session offers. This skill ships one: `node scripts/screenshot.cjs <url-or-html-file> [out-dir]` captures phone, tablet and desktop widths in light and dark, and reports horizontal overflow and console errors. It needs Playwright to be installed.
2. **Look at every screenshot** - actually examine it. Alignment, spacing rhythm, hierarchy, clipped or overflowing text, contrast, anything touching an edge.
3. **Use it.** Click through each state. Tab through with the keyboard. Try the empty, loading and error cases. Put in the long name and the huge number.
4. **Fix and shoot again.** The first render nearly always shows something the code didn't.

If you can't render it in this environment, say so plainly in your report. Don't describe the UI as though you had seen it.

Script paths above are relative to this skill's directory.

## Review checklist

- The most important thing is the most prominent; there is one primary action
- Spacing and type sizes come from the scale; edges align
- It follows the existing design system or tokens
- Text and control contrast meets the ratios, in every theme
- Every state exists: hover, focus, disabled, loading, empty, error, overflow
- It works by keyboard; focus is visible; elements are semantic; icon buttons have names
- It holds at phone, tablet and desktop widths with no sideways scroll
- It works with real, long, missing and extreme content
- It was rendered and looked at, not just written
