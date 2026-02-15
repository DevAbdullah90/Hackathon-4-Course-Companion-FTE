from src.services.quiz import QuizService

def test_grade_quiz_correct():
    service = QuizService()
    submission = {"q1": "A", "q2": "C"}
    key = {"q1": "A", "q2": "C"}
    
    result = service.grade_quiz(submission, key)
    
    assert result["score"] == 100
    assert result["passed"] is True
    assert result["details"]["q1"]["correct"] is True
    assert result["details"]["q2"]["correct"] is True

def test_grade_quiz_partial():
    service = QuizService()
    submission = {"q1": "A", "q2": "B"} # q2 wrong
    key = {"q1": "A", "q2": "C"}
    
    result = service.grade_quiz(submission, key)
    
    assert result["score"] == 50
    assert result["passed"] is False # 50% < 70% threshold
    assert result["details"]["q1"]["correct"] is True
    assert result["details"]["q2"]["correct"] is False
    assert result["details"]["q2"]["correct_answer"] == "C"

def test_grade_quiz_empty_submission():
    service = QuizService()
    submission = {}
    key = {"q1": "A"}
    
    result = service.grade_quiz(submission, key)
    
    assert result["score"] == 0
    assert result["passed"] is False

def test_grade_quiz_empty_key():
    service = QuizService()
    submission = {"q1": "A"}
    key = {}
    
    result = service.grade_quiz(submission, key)
    
    assert result["score"] == 0
    assert result["passed"] is False
