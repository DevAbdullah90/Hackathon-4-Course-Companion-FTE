import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { ChevronRight, ChevronDown, CheckCircle, Circle, Lock } from 'lucide-react';

interface SidebarProps {
    currentChapterSlug: string;
}

const Sidebar: React.FC<SidebarProps> = ({ currentChapterSlug }) => {
    const navigate = useNavigate();
    const [courses, setCourses] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [expandedModules, setExpandedModules] = useState<string[]>([]);

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const res = await api.get('/courses/');
                setCourses(res.data);
                // Expand all modules by default for now
                if (res.data.length > 0) {
                    const allModIds = res.data[0].modules.map((m: any) => m.id);
                    setExpandedModules(allModIds);
                }
            } catch (err) {
                console.error('Failed to fetch sidebar data', err);
            } finally {
                setLoading(false);
            }
        };
        fetchCourses();
    }, []);

    const toggleModule = (modId: string) => {
        if (expandedModules.includes(modId)) {
            setExpandedModules(expandedModules.filter(id => id !== modId));
        } else {
            setExpandedModules([...expandedModules, modId]);
        }
    };

    if (loading) return <div className="w-64 border-r h-screen bg-muted/10 p-4">Loading...</div>;

    // Assuming single course for this MVP
    const course = courses[0];
    if (!course) return <div className="hidden"></div>;

    return (
        <div className="w-80 border-r h-screen bg-card overflow-y-auto sticky top-0 hidden lg:flex lg:flex-col">
            <div className="p-6 border-b shrink-0">
                <h2 className="font-bold text-lg">{course.title}</h2>
                <p className="text-xs text-muted-foreground mt-1">Course Content</p>
            </div>

            <div className="p-4 space-y-4 flex-1 overflow-y-auto">
                {course.modules?.map((module: any) => (
                    <div key={module.id} className="space-y-1">
                        <button
                            onClick={() => toggleModule(module.id)}
                            className="flex items-center justify-between w-full p-2 hover:bg-muted/50 rounded-lg text-left"
                        >
                            <span className="font-semibold text-sm">{module.title}</span>
                            {expandedModules.includes(module.id) ? (
                                <ChevronDown className="w-4 h-4 text-muted-foreground" />
                            ) : (
                                <ChevronRight className="w-4 h-4 text-muted-foreground" />
                            )}
                        </button>

                        {expandedModules.includes(module.id) && (
                            <div className="pl-2 space-y-1">
                                {module.chapters?.map((chapter: any) => {
                                    const isActive = chapter.slug === currentChapterSlug;
                                    return (
                                        <button
                                            key={chapter.id}
                                            onClick={() => navigate(`/lesson/${chapter.slug}`)}
                                            className={`w-full flex items-center gap-3 p-2 rounded-lg text-sm transition-colors ${isActive
                                                ? 'bg-primary/10 text-primary font-medium'
                                                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                                                }`}
                                        >
                                            {chapter.is_premium ? <Lock className="w-3 h-3" /> : <Circle className="w-3 h-3 opacity-20" />}
                                            <span className="truncate">{chapter.title}</span>
                                        </button>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className="p-4 border-t mt-auto shrink-0">
                <button
                    onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }}
                    className="w-full px-4 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                    Logout
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
