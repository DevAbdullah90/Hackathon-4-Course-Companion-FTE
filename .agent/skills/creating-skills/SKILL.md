---
name: creating-skills
description: Generates high-quality, predictable, and efficient .agent/skills/ directories. Use when the user requests a new skill, modular capability, or procedural guide for the Antigravity agent environment.
---

# Creating Skills

## When to use this skill
- When requested to build a new capability for the Antigravity environment.
- When organizing complex workflows into reusable agent artifacts.
- When establishing standardized procedures for specialized engineering tasks.

## Workflow
1.  **Requirement Capture**: Identify the skill name (gerund form), triggers, and core logic.
2.  **Structural Planning**: Define necessary helper scripts, examples, or templates.
3.  **Drafting**: Create the `SKILL.md` with strict YAML frontmatter and concise instructions.
4.  **Validation**: Verify naming conventions and path formatting.
5.  **Execution**: Write the files to the `.agent/skills/` directory.

### Skill Checklist
- [ ] Name is in gerund form (e.g., `managing-aws`).
- [ ] Description is in 3rd person and includes keywords.
- [ ] Frontmatter is correctly formatted YAML.
- [ ] All paths use forward slashes `/`.
- [ ] `SKILL.md` is under 500 lines.
- [ ] Scripts include `--help` flags and clear stdout.

## Instructions

### YAML Frontmatter
The frontmatter must be at the very top and follow this structure:
```yaml
---
name: gerund-name
description: 3rd-person description including triggers.
---
```

### Path Conventions
Always use absolute or relative paths with forward slashes:
- Target: `.agent/skills/<skill-name>/SKILL.md`
- Support: `.agent/skills/<skill-name>/scripts/`

### The "Claude Way"
- **High Freedom**: Use bulleted heuristics for non-deterministic tasks.
- **Medium Freedom**: Use markdown code blocks for templates.
- **Low Freedom**: Use specific CLI commands for fragile operations.

## Resources
- [See SKILL_TEMPLATE.md](resources/SKILL_TEMPLATE.md)
- [See VALIDATE_NAMING.py](scripts/validate_naming.py)
