---
name: concept-explainer
description: Explain concepts at various complexity levels
trigger_keywords: ["explain", "what is", "how does"]
---

# Concept Explainer Skill

## Purpose
To break down complex technical concepts into understandable explanations tailored to the learner's level, using analogies and examples.

## Workflow
1.  **Analyze Request**: Identify the core concept and the user's current understanding (based on context or query).
2.  **Determine Level**: Assess if the user needs a "ELI5" (Explain Like I'm 5), Beginner, Intermediate, or Advanced explanation. Default to Beginner if unsure.
3.  **Generate Explanation**:
    *   **Define**: Give a clear, concise definition.
    *   **Analogy**: Provide a real-world analogy (e.g., "A Variable is like a box...").
    *   **Example**: Show a code snippet or practical example.
    *   **Why It Matters**: Explain the importance/utility of the concept.
4.  **Check Understanding**: Ask a follow-up question to ensure the user grasped the concept.

## Response Templates
*   "Think of [Concept] like a [Analogy]..."
*   "In simple terms, [Concept] is..."
*   "Here's how this works in code: [Code Snippet]"

## Key Principles
*   **Simple is better**: Avoid jargon unless defined.
*   **Concrete over Abstract**: Use tangible examples.
*   **Encouraging**: Validate the user's curiosity.
