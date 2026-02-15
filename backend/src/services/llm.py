import os
import yaml
from ..core.config import settings

class LLMService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            # We log a warning but don't crash init, 
            # so the app can start even if key is missing (until feature is used)
            print("WARNING: GEMINI_API_KEY is not set. Hybrid features will fail.")
            
        self.client = openai.OpenAI(
            api_key=settings.GEMINI_API_KEY or "dummy",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = "gemini-flash-lite-latest"
        self.skills = self._load_skills()

    def _load_skills(self):
        skills = []
        # Path specific to the provided environment structure
        # backend/src/services/ -> ../../../.agent/skills
        base_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".agent", "skills")
        
        if not os.path.exists(base_path):
            print(f"Warning: Skills directory not found at {base_path}")
            return skills

        for skill_dir in os.listdir(base_path):
            skill_path = os.path.join(base_path, skill_dir, "SKILL.md")
            if os.path.exists(skill_path):
                try:
                    with open(skill_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Extract basic frontmatter (simple split)
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                frontmatter = yaml.safe_load(parts[1])
                                body = parts[2].strip()
                                skills.append({
                                    "name": frontmatter.get("name", skill_dir),
                                    "keywords": frontmatter.get("trigger_keywords", []),
                                    "content": body
                                })
                except Exception as e:
                    print(f"Failed to load skill {skill_dir}: {e}")
        return skills

    def _generate(self, messages: list) -> tuple[str, int, int]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            content = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            return content, prompt_tokens, completion_tokens
        except Exception as e:
            print(f"LLM Error: {e}")
            raise e

    def grade_assessment(self, question: str, answer: str) -> tuple[dict, int, int]:
        system_prompt = """You are an expert AI tutor. 
Evaluate the student's answer based on:
1. Reasoning depth
2. Factual accuracy
3. Clarity

Return a STRICT JSON object with these fields:
- "score": int (1-5)
- "feedback": { "strengths": [str], "weaknesses": [str] }
- "reasoning": str (explanation of the score)
Do not include any other text."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}
        ]
        
        content, p_tok, c_tok = self._generate(messages)
        
        import json
        try:
            # Cleanup potential markdown formatting
            cleaned = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned)
            return result, p_tok, c_tok
        except json.JSONDecodeError:
            # Fallback for parsing error
            return {
                "score": 1, 
                "feedback": {"strengths": [], "weaknesses": ["Could not parse AI response"]}, 
                "reasoning": content[:200]
            }, p_tok, c_tok

    def generate_study_path(self, weak_topics: list[str]) -> tuple[dict, int, int]:
        if not weak_topics:
            return {"message": "Great job! You are performing well in all modules.", "recommendations": []}, 0, 0
            
        topics_str = ", ".join(weak_topics)
        system_prompt = f"""You are an expert AI academic advisor.
The student is struggling with the following topics: {topics_str}

Generate a personalized study plan.
Return a STRICT JSON object:
{{
    "weak_topics": {str(weak_topics)},
    "recommendations": [
        {{
            "topic": "Topic Name",
            "reason": "Why they need to review this",
            "action_item": "Specific advice or exercise",
            "priority": "HIGH"
        }}
    ]
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate my study path."}
        ]
        
        content, p_tok, c_tok = self._generate(messages)
        
        import json
        try:
            cleaned = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned)
            return result, p_tok, c_tok
        except json.JSONDecodeError:
            return {"error": "Failed to parse plan", "raw": content[:200]}, p_tok, c_tok

    def chat_with_tutor(self, message: str, context: str) -> tuple[str, int, int]:
        # detect active skill
        active_skill = None
        for skill in self.skills:
            for kw in skill["keywords"]:
                if kw.lower() in message.lower():
                    active_skill = skill
                    break
            if active_skill:
                break
        
        skill_instruction = ""
        if active_skill:
            print(f"Activating Skill: {active_skill['name']}")
            skill_instruction = f"""
*** ACTIVE SKILL: {active_skill['name']} ***
{active_skill['content']}
"""
        else:
            # Default behavior
            skill_instruction = "You are a friendly and expert AI Coding Tutor."

        system_prompt = f"""{skill_instruction}

You have access to the current lesson content:
<ongoing_lesson_context>
{context[:2000]}... (truncated for brevity)
</ongoing_lesson_context>

Answer the student's question based on the lesson context (if relevant) and your active skill instructions.
Keep answers concise, encouraging, and use code snippets where helpful.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        content, p_tok, c_tok = self._generate(messages)
        return content, p_tok, c_tok
