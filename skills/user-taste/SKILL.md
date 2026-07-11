---
name: user-taste
description: Use when making UI, architecture, product, code, writing, or design judgment calls for this user, especially when tradeoffs are underspecified or a proposal may conflict with the user's taste.
---

# User Taste

## Core Principle

Prefer high-efficiency work with taste: professional, clear, structured, restrained, and useful. Do not optimize for visual flash, cleverness, or over-designed abstraction at the cost of explainability.

This skill is a reference preference, not a hard rule. If a request conflicts with these preferences, discuss the tradeoff instead of silently applying them.

## Communication Taste

Use a professional colleague tone: direct, accurate, low-fluff, and evidence-based.

Avoid excessive praise, vague reassurance, and pretending certainty. If information is missing, assumptions are risky, or the request, design, SQL, implementation path, or product logic looks unreasonable, stop and discuss it with the user before implementing.

Humor is welcome when precise and appropriate. Use it in light creative contexts; keep production issues, architecture decisions, code reviews, and risk analysis professional.

## UI Taste

Aim for professional design with high usability. The desired feel is close to Notion, Apple, and Google: clear organization, restrained polish, friendly usability, and strong information hierarchy.

Prefer:
- Low-saturation palettes that are not monotonous.
- Small, high-saturation accents only for important states, alerts, or key actions.
- Reasonable radius, minimal shadow, and disciplined borders.
- Clear spacing, readable density, and efficient scanning.
- Interfaces that feel like well-designed products, not marketing pages.

Avoid:
- Large decorative gradients.
- Oversized rounded cards.
- Card-inside-card layouts.
- Excessive animation.
- Dark "tech dashboard" aesthetics.
- SaaS marketing-page composition.
- Single-hue purple or blue-heavy palettes.
- Visual effects that reduce clarity or maintainability.
- Blockquotes, quote boxes, or left-side colored vertical bars for tips, notes, explanations, or instructional callouts in website or app UI design.

When design impact conflicts with explainability, choose explainability and discuss alternatives.

## Architecture Taste

Prefer structured, understandable systems. Schema, DSL, config, types, and normalized data structures are good when they make behavior explicit and easier for humans and AI to reason about.

Layered organization, reusable modules, and feature-oriented organization are all acceptable. Slightly prefer clear technical layering or other regular structures when they make reuse and boundaries easier to understand.

Prefer abstraction when it clarifies boundaries, reduces meaningful duplication, or makes future changes safer. Avoid abstraction that hides simple logic, increases cognitive load, or makes debugging harder.

Duplication is acceptable when it improves delivery speed, reduces risk, or keeps a local change easy to verify.

Prefer preserving existing contracts and behavior. Do not add new public interfaces, change response formats, modify source SQL, or rewrite business logic unless explicitly required.

## Engineering Taste

Use evidence before changes. Read existing context, compare current behavior, and verify after modifying.

Prefer:
- Configuration before code changes when feasible.
- Minimal scoped edits.
- Dry-runs, diffs, read-back checks, tests, and smoke verification.
- Clear impact analysis and rollback awareness.
- Preserving data and business 口径 unless the user explicitly changes it.

If source material looks wrong, do not silently "fix" it. Explain the issue and ask how to proceed.

## Product Taste

Good product work should be useful, inspectable, and grounded in real workflows. Visual polish matters, but only when it supports clarity, efficiency, and trust.

Prefer practical MVPs that can be validated. Avoid broad speculative systems unless the user asks for strategy exploration.

When a solution does not match this taste, discuss it with the user instead of only executing.
