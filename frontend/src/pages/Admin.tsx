import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Users, CreditCard, BarChart3, Activity } from 'lucide-react';

const Admin: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await api.get('/admin/summary');
        setSummary(res.data);
      } catch (err) {
        console.error('Failed to fetch admin summary', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) return <div className="p-8">Loading analytics...</div>;
  if (!summary) return <div className="p-8">Access Denied or Error.</div>;

  return (
    <div className="max-w-7xl mx-auto p-8">
      <header className="mb-12">
        <h1 className="text-3xl font-bold">Admin Console</h1>
        <p className="text-muted-foreground mt-1">Platform-wide analytics and performance monitoring.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <StatCard 
          icon={<Users className="text-blue-600" />} 
          title="Total Users" 
          value={summary.users.total} 
          subtitle={`${summary.users.premium} Premium`}
        />
        <StatCard 
          icon={<CreditCard className="text-green-600" />} 
          title="LLM Cost" 
          value={`$${summary.llm_usage.total_cost_usd}`} 
          subtitle="Estimated Spend"
        />
        <StatCard 
          icon={<Activity className="text-purple-600" />} 
          title="Total Tokens" 
          value={summary.llm_usage.total_tokens.toLocaleString()} 
          subtitle="Processed"
        />
        <StatCard 
          icon={<BarChart3 className="text-amber-600" />} 
          title="Avg. Score" 
          value="4.2" 
          subtitle="Across Quizzes"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="bg-card border rounded-2xl p-8">
          <h2 className="text-xl font-bold mb-6">Usage by Feature</h2>
          <div className="space-y-6">
            {summary.llm_usage.by_feature.map((f: any) => (
              <div key={f.feature} className="flex items-center justify-between">
                <div>
                  <p className="font-bold">{f.feature}</p>
                  <p className="text-sm text-muted-foreground">{f.calls} requests</p>
                </div>
                <div className="text-right">
                  <p className="font-bold">${f.cost}</p>
                  <div className="w-24 h-1 bg-secondary rounded-full mt-1 overflow-hidden">
                    <div 
                      className="bg-primary h-full" 
                      style={{ width: `${(f.cost / summary.llm_usage.total_cost_usd) * 100}%` }} 
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="bg-card border rounded-2xl p-8 flex items-center justify-center">
          <p className="text-muted-foreground italic text-center">
            [Interactive Charts Placeholder]<br/>
            (Requires Chart.js or Recharts)
          </p>
        </section>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, subtitle }: any) => (
  <div className="bg-card border rounded-2xl p-6">
    <div className="flex items-center gap-4 mb-4">
      <div className="p-2 bg-secondary rounded-lg">{icon}</div>
      <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">{title}</h3>
    </div>
    <div className="flex items-baseline gap-2">
      <span className="text-3xl font-black">{value}</span>
      <span className="text-xs font-medium text-muted-foreground">{subtitle}</span>
    </div>
  </div>
);

export default Admin;
