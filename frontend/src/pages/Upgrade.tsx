import React, { useState } from 'react';
import api from '../lib/api';
import { Check, Star, Zap, ShieldCheck } from 'lucide-react';

const Upgrade: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleUpgrade = async () => {
    setLoading(true);
    try {
      // Mock upgrade endpoint
      await new Promise(resolve => setTimeout(resolve, 1500));
      // In real life: await api.post('/user/upgrade');
      setSuccess(true);
    } catch (err) {
      console.error('Upgrade failed', err);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center p-8">
        <div className="max-w-md w-full bg-card border rounded-3xl p-12 text-center shadow-xl">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-8">
            <ShieldCheck className="w-10 h-10 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold mb-4">Welcome to Premium!</h1>
          <p className="text-muted-foreground mb-8 text-lg">Your account has been upgraded. You now have full access to Hybrid Intelligence features.</p>
          <a href="/" className="inline-block w-full bg-primary text-primary-foreground font-bold py-4 rounded-2xl hover:opacity-90 transition-all">
            Go to Dashboard
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-8 py-20">
      <header className="text-center mb-20">
        <span className="text-primary font-bold tracking-widest text-sm uppercase mb-4 inline-block">Premium Access</span>
        <h1 className="text-5xl font-extrabold tracking-tight mb-6">Unlock Hybrid Intelligence</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Master AI Agent Development with personalized feedback and adaptive learning paths powered by Gemini 1.5 Pro.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div className="space-y-8">
          <div className="flex gap-6">
            <div className="flex-none w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center">
              <Zap className="w-7 h-7 text-primary" />
            </div>
            <div>
              <h3 className="text-xl font-bold mb-2">AI-Graded Assessments</h3>
              <p className="text-muted-foreground leading-relaxed">Get detailed rubric-based scores and constructive feedback on your code and written answers.</p>
            </div>
          </div>

          <div className="flex gap-6">
            <div className="flex-none w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center">
              <Star className="w-7 h-7 text-primary" />
            </div>
            <div>
              <h3 className="text-xl font-bold mb-2">Adaptive Study Paths</h3>
              <p className="text-muted-foreground leading-relaxed">The system analyzes your quiz results to generate a custom roadmap focusing on your weak areas.</p>
            </div>
          </div>

          <div className="flex gap-6">
            <div className="flex-none w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center">
              <Check className="w-7 h-7 text-primary" />
            </div>
            <div>
              <h3 className="text-xl font-bold mb-2">Unlimited Access</h3>
              <p className="text-muted-foreground leading-relaxed">No restrictions on course content or lesson viewing across all modules.</p>
            </div>
          </div>
        </div>

        <div className="bg-primary text-primary-foreground rounded-3xl p-12 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <Star className="w-32 h-32" />
          </div>
          
          <h2 className="text-2xl font-bold mb-2">Premium Plan</h2>
          <div className="flex items-baseline gap-2 mb-8">
            <span className="text-5xl font-black">$19</span>
            <span className="text-primary-foreground/70 font-medium">/ month</span>
          </div>

          <ul className="space-y-4 mb-12">
            {[
              "Everything in Free",
              "AI Mentorship",
              "Adaptive Curriculum",
              "Priority Support",
              "Certificate of Completion"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-3 font-medium">
                <Check className="w-5 h-5 text-primary-foreground/50" /> {item}
              </li>
            ))}
          </ul>

          <button 
            onClick={handleUpgrade}
            disabled={loading}
            className="w-full bg-background text-primary font-bold py-5 rounded-2xl hover:bg-opacity-90 transition-all shadow-lg flex justify-center items-center gap-2"
          >
            {loading ? "Processing..." : "Upgrade Now"}
          </button>
          
          <p className="mt-6 text-center text-sm text-primary-foreground/60 font-medium italic">
            Cancel anytime. 7-day money back guarantee.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Upgrade;
