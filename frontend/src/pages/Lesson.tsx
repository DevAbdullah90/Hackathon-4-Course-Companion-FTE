import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../lib/api';
import LessonViewer from '../components/LessonViewer';
import Quiz from '../components/Quiz';
import PremiumFeatures from '../components/PremiumFeatures';
import Sidebar from '../components/Sidebar';
import AITutor from '../components/AITutor';
import { ArrowLeft, ArrowRight, CheckCircle, BrainCircuit } from 'lucide-react';

const Lesson: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [completed, setCompleted] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);

  useEffect(() => {
    const fetchLesson = async () => {
      try {
        const res = await api.get(`/chapters/${slug}/content`);
        setLesson(res.data);
      } catch (err) {
        console.error('Failed to fetch lesson', err);
      } finally {
        setLoading(false);
      }
    };

    fetchLesson();
  }, [slug]);

  const handleMarkComplete = async () => {
    try {
      await api.post('/progress/', {
        chapter_slug: slug,
        is_completed: true
      });
      setCompleted(true);
      alert("Lesson marked as complete! 🎉");
    } catch (err) {
      console.error('Failed to update progress', err);
      alert("Failed to mark lesson as complete. Please try again.");
    }
  };

  if (loading) return <div className="p-8 text-center">Loading lesson...</div>;
  if (!lesson) return <div className="p-8 text-center text-destructive">Lesson not found.</div>;

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="border-b bg-card sticky top-0 z-10 px-8 py-4 flex items-center justify-between lg:hidden">
        {/* Mobile Nav Header - Sidebar is hidden on mobile for now, or could be a drawer */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
        <div className="flex items-center gap-4">
          {completed && (
            <span className="flex items-center gap-1 text-sm font-bold text-green-600 bg-green-50 px-3 py-1 rounded-full border border-green-200">
              <CheckCircle className="w-4 h-4" />
            </span>
          )}
        </div>
      </nav>

      <div className="flex flex-1">
        <Sidebar currentChapterSlug={slug || ''} />

        <div className="flex-1 flex flex-col min-h-screen">
          <nav className="border-b bg-card sticky top-0 z-10 px-8 py-4 hidden lg:flex items-center justify-between">
            <button
              onClick={() => navigate(-1)}
              className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Dashboard
            </button>
            <div className="flex items-center gap-4">
              {completed && (
                <span className="flex items-center gap-1 text-sm font-bold text-green-600 bg-green-50 px-3 py-1 rounded-full border border-green-200">
                  <CheckCircle className="w-4 h-4" /> Completed
                </span>
              )}
              <button
                onClick={handleMarkComplete}
                disabled={completed}
                className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${completed
                  ? 'bg-secondary text-muted-foreground cursor-default'
                  : 'bg-primary text-primary-foreground hover:opacity-90'
                  }`}
              >
                {completed ? 'Finished' : 'Mark as Complete'}
              </button>
            </div>
          </nav>

          <main className="flex-1 max-w-4xl mx-auto w-full p-8 md:p-12">
            {!showQuiz ? (
              <>
                <LessonViewer title={lesson.title} content={lesson.markdown_content} />

                {lesson.quiz && (
                  <div className="mt-12 p-8 bg-muted/20 rounded-xl border text-center">
                    <h3 className="text-2xl font-bold mb-4">Ready to test your knowledge?</h3>
                    <button
                      onClick={() => setShowQuiz(true)}
                      className="bg-primary text-primary-foreground px-8 py-3 rounded-lg font-bold hover:opacity-90 transition-all cursor-pointer"
                    >
                      Start Quiz
                    </button>
                  </div>
                )}

                {lesson.title.includes("Assessment") && (
                  <div className="mt-12">
                    <PremiumFeatures chapterId={slug || ''} questionId="q1" />
                  </div>
                )}
              </>
            ) : (
              <div className="animate-in fade-in slide-in-from-bottom-8 duration-500">
                <button
                  onClick={() => setShowQuiz(false)}
                  className="mb-6 flex items-center gap-2 text-sm text-muted-foreground hover:text-primary cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" /> Back to Lesson
                </button>
                <Quiz
                  questions={lesson.quiz.questions || []}
                  onComplete={(score) => {
                    handleMarkComplete();
                    // alert(`Quiz Finished! Score: ${score}`);
                    setShowQuiz(false);
                  }}
                />
              </div>
            )}
          </main>

          <footer className="border-t bg-muted/30 px-8 py-6">
            <div className="max-w-4xl mx-auto flex justify-between items-center">
              <div className="text-sm text-muted-foreground font-medium">
                {lesson.next_chapter_slug ? 'Next Lesson Available' : 'End of Course'}
              </div>
              <button
                onClick={() => lesson.next_chapter_slug && navigate(`/lesson/${lesson.next_chapter_slug}`)}
                className={`flex items-center gap-2 font-bold transition-colors ${lesson.next_chapter_slug
                  ? 'hover:text-primary cursor-pointer'
                  : 'text-muted-foreground cursor-not-allowed opacity-50'
                  }`}
                disabled={!lesson.next_chapter_slug}
              >
                Next Lesson <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </footer>

          {/* AI Tutor Floating Widget - Pass lesson markdown as context */}
          <AITutor context={lesson.markdown_content || ""} />
        </div>
      </div>
    </div>
  );
};

export default Lesson;
