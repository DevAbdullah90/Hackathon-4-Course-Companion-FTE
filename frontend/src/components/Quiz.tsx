import React, { useState } from 'react';
import { Check, X, ArrowRight } from 'lucide-react';

interface Question {
  id: string;
  text: string;
  options: string[];
  correct_answer: number;
}

interface QuizProps {
  questions: Question[];
  onComplete: (score: number) => void;
}

const Quiz: React.FC<QuizProps> = ({ questions, onComplete }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);

  const handleSelect = (index: number) => {
    if (isAnswered) return;
    setSelected(index);
  };

  const handleSubmit = () => {
    if (selected === null) return;
    setIsAnswered(true);
    if (selected === questions[currentIndex].correct_answer) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelected(null);
      setIsAnswered(false);
    } else {
      onComplete(score);
    }
  };

  const currentQ = questions[currentIndex];

  return (
    <div className="bg-card border rounded-2xl p-8 max-w-2xl mx-auto shadow-sm">
      <div className="flex justify-between items-center mb-8">
        <span className="text-sm font-bold text-primary px-3 py-1 bg-primary/10 rounded-full">
          Question {currentIndex + 1} of {questions.length}
        </span>
        <span className="text-sm text-muted-foreground font-medium">
          Score: {score}
        </span>
      </div>

      <h2 className="text-2xl font-bold mb-8">{currentQ.text}</h2>

      <div className="space-y-4 mb-8">
        {currentQ.options.map((option, idx) => (
          <button
            key={idx}
            onClick={() => handleSelect(idx)}
            className={`w-full text-left p-4 rounded-xl border-2 transition-all flex justify-between items-center ${
              selected === idx 
                ? isAnswered 
                  ? idx === currentQ.correct_answer 
                    ? 'border-green-500 bg-green-50' 
                    : 'border-red-500 bg-red-50'
                  : 'border-primary bg-primary/5'
                : isAnswered && idx === currentQ.correct_answer
                  ? 'border-green-500 bg-green-50'
                  : 'border-border hover:border-primary/50'
            }`}
          >
            <span className="font-medium">{option}</span>
            {isAnswered && idx === currentQ.correct_answer && <Check className="w-5 h-5 text-green-600" />}
            {isAnswered && selected === idx && idx !== currentQ.correct_answer && <X className="w-5 h-5 text-red-600" />}
          </button>
        ))}
      </div>

      {!isAnswered ? (
        <button
          onClick={handleSubmit}
          disabled={selected === null}
          className="w-full bg-primary text-primary-foreground font-bold py-4 rounded-xl disabled:opacity-50"
        >
          Check Answer
        </button>
      ) : (
        <button
          onClick={handleNext}
          className="w-full bg-primary text-primary-foreground font-bold py-4 rounded-xl flex justify-center items-center gap-2"
        >
          {currentIndex === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
          <ArrowRight className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};

export default Quiz;
