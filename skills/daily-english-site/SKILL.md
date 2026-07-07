---
name: daily-english-site
description: Use this skill when generating or maintaining a JSON-driven Daily English learning website for GitHub Pages. It defines lesson schema, review flow, mobile UI rules, privacy-safe metadata, and publishing steps.
---

# Daily English Site Skill

## Purpose

Maintain a static Daily English learning website where each day is one JSON lesson and the page reads the latest lesson from an index file.

The output should be a reusable website update, not a long chat-only lesson.

## When to use

Use this skill when the user asks to:

- Generate daily English learning JSON.
- Publish daily learning content to GitHub Pages.
- Build or improve a mobile-first vocabulary website.
- Maintain review questions, weak-word tracking, and daily word lists.

Do not use it for one-off translation or grammar explanations unless the user asks to publish the result to the website.

## Repository structure

```text
public/english-daily/
  index.html
  style.css
  app.js
  data/
    index.json
    YYYY-MM-DD.json
```

The website must stay static and GitHub Pages compatible.

## Daily lesson schema

Each `YYYY-MM-DD.json` must follow this shape:

```json
{
  "date": "YYYY-MM-DD",
  "title": "YYYY-MM-DD｜Daily English",
  "reviewQuiz": [
    { "zh": "中文提示", "answer": "English answer" }
  ],
  "words": [
    {
      "word": "availability",
      "phonetic": "/əˌveɪləˈbɪləti/",
      "meaning": "可用情况；库存；余量",
      "phrase": "check availability",
      "sentence": "We need to check availability before booking.",
      "category": "业务"
    }
  ],
  "focus": [
    "今天重点复习 availability / itinerary。"
  ]
}
```

Rules:

- `words` must contain exactly 10 items.
- Every word must include `word`, `phonetic`, `meaning`, `phrase`, `sentence`, and `category`.
- Use generic categories such as `业务`, `技术`, `沟通`, or `旅行`.
- `reviewQuiz` should contain recent weak words before new words.
- Public titles should use only dates or `Daily English`.

## Index schema

`data/index.json` must follow this shape:

```json
{
  "latest": "YYYY-MM-DD",
  "lessons": [
    {
      "date": "YYYY-MM-DD",
      "title": "YYYY-MM-DD｜Daily English",
      "path": "./data/YYYY-MM-DD.json"
    }
  ]
}
```

Rules:

- Newest lesson appears first.
- `latest` matches the newest lesson.
- Paths are relative to the page.

## Daily workflow

1. Read the previous lesson if available.
2. Build `reviewQuiz` from weak or repeated words.
3. Generate exactly 10 new words.
4. Mix practical business, technical, communication, and travel examples.
5. Write `public/english-daily/data/YYYY-MM-DD.json`.
6. Update `public/english-daily/data/index.json`.
7. Verify JSON validity and schema completeness.
8. Reply with the GitHub Pages URL and a short focus summary.

## UI rules

- Mobile-first layout.
- Single-column cards on narrow screens.
- Clear flow: Review → Words → Focus.
- Sticky date selector on mobile.
- Progress feedback for remembered words.
- Tap targets should be at least 44px tall.
- Use semantic cards: quiz item, word card, focus card, progress card.
- Use CSS variables for color, radius, shadow, and spacing.
- Avoid public headings that reveal personal identity or job background.

## Acceptance checklist

- [ ] Website loads from `/english-daily/`.
- [ ] Latest lesson is controlled by `data/index.json`.
- [ ] Daily JSON is valid.
- [ ] `words` contains exactly 10 items.
- [ ] Review questions appear before new words.
- [ ] Public title is privacy-safe.
- [ ] Mobile layout is readable and touch-friendly.
- [ ] GitHub Pages URL is returned after publishing.
