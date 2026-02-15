from typing import Dict, Any, List
from sqlmodel import Session, select
from uuid import UUID
from ..models.base import Progress, Chapter, Module

class QuizService:
    def get_weak_modules(self, session: Session, user_id: UUID) -> List[str]:
        """
        Identify modules where average quiz score is < 70%.
        """
        statement = select(Progress).where(Progress.user_id == user_id).where(Progress.is_completed == True)
        progress_records = session.exec(statement).all()
        
        if not progress_records:
            return []
            
        module_scores = {} # { "Module Title": [scores] }
        
        for p in progress_records:
            if p.quiz_score is None: continue
            
            chapter = session.get(Chapter, p.chapter_id)
            if not chapter: continue
            
            module = session.get(Module, chapter.module_id)
            if not module: continue
            
            if module.title not in module_scores:
                module_scores[module.title] = []
            
            module_scores[module.title].append(p.quiz_score)
                
        weak_modules = []
        for title, scores in module_scores.items():
            if not scores: continue
            avg = sum(scores) / len(scores)
            if avg < 70:
                weak_modules.append(title)
                
        return weak_modules

    def grade_quiz(self, submission: Dict[str, str], answer_key: Dict[str, str]) -> Dict[str, Any]:
        """
        Deterministic grading: Compare submission keys against answer_key.
        """
        score = 0
        total = len(answer_key)
        results = {}

        if total == 0:
            return {"score": 0, "passed": False, "results": {}}

        for q_id, correct_ans in answer_key.items():
            user_ans = submission.get(q_id)
            is_correct = (user_ans == correct_ans)
            if is_correct:
                score += 1
            results[q_id] = {"correct": is_correct, "correct_answer": correct_ans}

        percentage = int((score / total) * 100)
        passed = percentage >= 70  # Static threshold for now

        return {
            "score": percentage,
            "passed": passed,
            "details": results
        }
