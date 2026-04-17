---
name: excalidraw-diagram
description: Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to visualize workflows, architectures, or concepts.
---

# Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth Required
- **Simple/Conceptual**: Abstract shapes, labels, relationships
- **Comprehensive/Technical**: Concrete examples, code snippets, real data

### Step 1: Understand Deeply
- What does this concept DO? (not what IS it)
- What relationships exist between concepts?
- What's the core transformation or flow?

### Step 2: Map Concepts to Patterns

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | Fan-out (radial arrows from center) |
| Combines inputs into one | Convergence (funnel) |
| Has hierarchy/nesting | Tree (lines + free-floating text) |
| Is a sequence of steps | Timeline (line + dots + labels) |
| Loops continuously | Spiral/Cycle |
| Is an abstract state | Cloud (overlapping ellipses) |
| Transforms input to output | Assembly line |
| Compares two things | Side-by-side |

### Step 3: Ensure Variety
For multi-concept diagrams: each major concept must use a different visual pattern.

### Step 4: Generate JSON, then Render & Validate (MANDATORY)

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text. Add containers only when they serve a purpose. Aim for <30% of text elements inside containers.

## Modern Aesthetics

- `roughness: 0` — Clean, crisp edges (default for professional diagrams)
- `roughness: 1` — Hand-drawn, organic feel
- Always use `opacity: 100` for all elements

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Render & Validate (MANDATORY)

After generating the JSON, run the render-view-fix loop until the diagram looks right:
1. Render to PNG
2. Audit against your original vision
3. Check for visual defects (clipped text, overlapping, wrong arrow connections)
4. Fix and re-render
5. Repeat until passing

## Quality Checklist

- [ ] Isomorphism: Does each visual structure mirror its concept's behavior?
- [ ] Argument: Does the diagram SHOW something text alone couldn't?
- [ ] Variety: Each major concept uses a different visual pattern?
- [ ] Minimal containers: <30% of text inside containers?
- [ ] Rendered to PNG and visually inspected?
- [ ] No text overflow or overlapping elements?
- [ ] Arrows connect to intended elements?
