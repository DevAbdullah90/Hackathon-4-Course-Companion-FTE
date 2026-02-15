import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { BookOpen, CheckCircle, TrendingUp } from 'lucide-react';

interface CourseDashboard {
  course: {
    title: string;
    slug: string;
    description: string;
  };
  total_chapters: number;
  completed_chapters: number;
  percentage: number;
  next_chapter_slug?: string;
}

const Dashboard: React.FC = () => {
  const [dashboards, setDashboards] = useState<CourseDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboards = async () => {
      try {
        const coursesRes = await api.get('/courses/');
        const dashPromises = coursesRes.data.map((c: any) => api.get(`/courses/${c.slug}/dashboard?t=${Date.now()}`));
        const dashResults = await Promise.all(dashPromises);
        const data = dashResults.map(r => r.data);
        console.log('Dashboard Data:', data);
        setDashboards(data);
      } catch (err: any) {
        console.error('Failed to fetch dashboard', err);
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboards();
  }, []);

  if (loading) return <div className="p-8">Loading dashboard...</div>;
  if (error) return <div className="p-8 text-destructive">Error: {error}. Please ensure backend is running at http://127.0.0.1:8000</div>;

  return (
    <div className="max-w-7xl mx-auto p-8">
      <header className="mb-12 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">Your Learning Journey</h1>
          <p className="mt-2 text-muted-foreground">Track your progress and continue learning AI Agent Development.</p>
        </div>
        <button
          onClick={() => {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }}
          className="px-4 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
        >
          Logout
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {dashboards.map((dash) => (
          <div key={dash.course.slug} className="group relative bg-card border rounded-xl p-6 hover:shadow-lg transition-all">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-primary/10 rounded-lg">
                <BookOpen className="w-6 h-6 text-primary" />
              </div>
              <span className="text-sm font-medium px-2 py-1 bg-secondary rounded-full">
                {Math.round(dash.percentage)}% Complete
              </span>
            </div>

            <h3 className="text-xl font-semibold mb-2">{dash.course.title}</h3>
            <p className="text-muted-foreground text-sm mb-6 line-clamp-2">{dash.course.description}</p>

            <div className="w-full bg-secondary h-2 rounded-full overflow-hidden mb-6">
              <div
                className="bg-primary h-full transition-all duration-500"
                style={{ width: `${dash.percentage}%` }}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center text-sm text-muted-foreground">
                <CheckCircle className="w-4 h-4 mr-1 text-green-500" />
                {dash.completed_chapters} / {dash.total_chapters} Lessons
              </div>
              <a
                href={dash.next_chapter_slug ? `/lesson/${dash.next_chapter_slug}` : '#missing-slug'}
                onClick={() => { if (!dash.next_chapter_slug) alert('Next chapter not found!'); }}
                className="text-sm font-bold text-primary hover:underline"
              >
                Continue →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
