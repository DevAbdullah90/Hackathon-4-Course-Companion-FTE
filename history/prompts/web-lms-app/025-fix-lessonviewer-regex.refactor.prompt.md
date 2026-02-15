---
id: 025
title: Fixed unterminated regex in LessonViewer
stage: refactor
date: 2026-02-14
surface: agent
model: gemini-2.0-flash
feature: web-lms-app
branch: 003-web-lms-app
user: abdullah9873
command: /sp.refactor
labels: ["frontend", "bugfix", "vite"]
links:
  spec: null
  plan: null
  tasks: null
files:
  - frontend/src/components/LessonViewer.tsx
tests: []
prompt: "Fix the 'Unterminated regular expression' error in LessonViewer.tsx during Vite build."
response: "The error was caused by a literal newline within a regular expression in the LessonViewer component. I have updated the code to use the escaped newline sequence `
` instead."
outcome: "Vite dependency scanning should now complete successfully."
evaluation: "Resolved a syntax error that was blocking the frontend development server."
---

# PHR: Fixed unterminated regex in LessonViewer

The syntax error in `src/components/LessonViewer.tsx` where a literal newline was used inside a regex literal has been corrected.

## Details
- **Issue**: `String(children).replace(/ 
 $/ , '')` had a raw newline.
- **Fix**: Changed to `String(children).replace(/
$/, '')`.
