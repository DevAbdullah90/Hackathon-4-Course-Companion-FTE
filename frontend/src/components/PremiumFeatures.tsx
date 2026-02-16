import React, { useState } from 'react';
import { Sparkles, BrainCircuit, AlertCircle, RefreshCcw } from 'lucide-react';
import api from '../lib/api';

interface Feedback {
  score: number;
  feedback: {
    strengths: string[];
    weaknesses: string[];
  };
  reasoning: string;
}

interface PremiumFeaturesProps {
  chapterId: string;
  questionId: string;
}

const PremiumFeatures: React.FC<PremiumFeaturesProps> = ({ chapterId, questionId }) => {
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [error, setError] = useState('');
  const [answer, setAnswer] = useState('');

  const getAIFeedback = async (answer: string) => {
    setLoading(true);
    setError('');
    try {
      const res = await api.post('/premium/grade', {
        chapter_id: chapterId,
        question_id: questionId,
        user_answer: answer
      });
      setFeedback(res.data);
    } catch (err: any) {
      if (err.response?.status === 429) {
        setError('Rate limit exceeded. Please try again later.');
      } else {
        setError('Failed to get AI feedback. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* AI Grading Section */}
      <section className="bg-card border rounded-2xl p-8 overflow-hidden relative">
        <div className="absolute top-0 right-0 p-4 opacity-5">
          <BrainCircuit className="w-24 h-24" />
        </div>

        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Sparkles className="w-5 h-5 text-purple-600" />
          </div>
          <h2 className="text-xl font-bold italic">AI Tutor Insights</h2>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Your Answer:</label>
          <textarea
            className="w-full p-3 border rounded-xl bg-background min-h-[150px] focus:ring-2 focus:ring-purple-500 outline-none"
            placeholder="Type your detailed answer here..."
            value={answer} // We need to add this state
            onChange={(e) => setAnswer(e.target.value)} // And this setter
          />
          <button
            onClick={() => getAIFeedback(answer)}
            disabled={loading || !answer.trim()}
            className="mt-4 bg-purple-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Get AI Feedback'}
          </button>
        </div>

        {loading ? (
          <div className="py-12 text-center">
            <RefreshCcw className="w-8 h-8 animate-spin mx-auto mb-4 text-purple-500" />
            <p className="text-muted-foreground font-medium">AI is analyzing your response...</p>
          </div>
        ) : feedback ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-4 mb-8">
              <div className="text-4xl font-black text-purple-600">{feedback.score}/5</div>
              <div className="h-10 w-[1px] bg-border" />
              <p className="text-sm font-medium leading-tight text-muted-foreground">{feedback.reasoning}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-green-50 border border-green-100 rounded-xl p-5">
                <h4 className="text-sm font-bold text-green-700 uppercase tracking-wider mb-3">Strengths</h4>
                <ul className="space-y-2">
                  {feedback.feedback.strengths.map((s, i) => (
                    <li key={i} className="text-sm text-green-800 flex gap-2">
                      <span className="opacity-50">•</span> {s}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-amber-50 border border-amber-100 rounded-xl p-5">
                <h4 className="text-sm font-bold text-amber-700 uppercase tracking-wider mb-3">Refinements</h4>
                <ul className="space-y-2">
                  {feedback.feedback.weaknesses.map((w, i) => (
                    <li key={i} className="text-sm text-amber-800 flex gap-2">
                      <span className="opacity-50">•</span> {w}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ) : error ? (
          <div className="bg-destructive/10 border border-destructive/20 rounded-xl p-6 flex gap-4 items-center">
            <AlertCircle className="w-6 h-6 text-destructive" />
            <p className="text-sm font-medium text-destructive">{error}</p>
          </div>
        ) : (
          <p className="text-muted-foreground italic text-center py-8">Complete the assessment to receive AI-powered guidance.</p>
        )}
      </section>
    </div>
  );
};

export default PremiumFeatures;
