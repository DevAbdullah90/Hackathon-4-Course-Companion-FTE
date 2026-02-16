import React, { useEffect, useState } from 'react';
import { TrendingUp, AlertCircle, CheckCircle, ArrowRight, Zap } from 'lucide-react';
import api from '../lib/api';

interface Recommendation {
    topic: string;
    reason: string;
    action_item: string;
    priority: string;
}

interface AdaptivePathData {
    weak_topics: string[];
    recommendations: Recommendation[];
}

const AdaptivePath: React.FC = () => {
    const [data, setData] = useState<AdaptivePathData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchPath = async () => {
            console.log("AdaptivePath: Fetching data...");
            try {
                const res = await api.get('/premium/adaptive-path');
                console.log("AdaptivePath: Data received", res.data);
                setData(res.data);
            } catch (err: any) {
                console.error("Adaptive Path Error", err);
                if (err.response?.status === 403) {
                    setError("Upgrade to Premium to unlock your personalized AI Study Path.");
                } else {
                    setError("Failed to generate study path.");
                }
            } finally {
                setLoading(false);
            }
        };

        fetchPath();
    }, []);

    if (loading) return (
        <div className="bg-card border rounded-xl p-6 animate-pulse">
            <div className="h-6 bg-muted rounded w-1/3 mb-4"></div>
            <div className="h-20 bg-muted rounded mb-4"></div>
            <div className="h-20 bg-muted rounded"></div>
        </div>
    );

    if (error) return (
        <div className="bg-muted/30 border dashed border-muted-foreground/20 rounded-xl p-6 text-center">
            <Zap className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
            <p className="text-sm text-muted-foreground">{error}</p>
        </div>
    );

    // Safety check for invalid data structure
    if (!data || !data.weak_topics || !data.recommendations) {
        // If data is invalid but no error state, we might have received an error object from LLM
        // or just unexpected structure. Let's show the 'On Track' state as fallback
        // or unexpected error state if we want to be strict.
        // For now, if we have data but it's missing fields, likely an error response.
        if (data && (data as any).error) {
            return (
                <div className="bg-muted/30 border dashed border-muted-foreground/20 rounded-xl p-6 text-center">
                    <Zap className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">AI could not generate a plan right now. Try again later.</p>
                </div>
            );
        }

        return (
            <div className="bg-green-50 border border-green-100 rounded-xl p-6 text-center">
                <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
                <h3 className="font-bold text-green-700">You're on track!</h3>
                <p className="text-green-600 text-sm">No weak areas detected. Keep up the great work!</p>
            </div>
        );
    }

    if (data.weak_topics.length === 0 && data.recommendations.length === 0) return (
        <div className="bg-green-50 border border-green-100 rounded-xl p-6 text-center">
            <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <h3 className="font-bold text-green-700">You're on track!</h3>
            <p className="text-green-600 text-sm">No weak areas detected. Keep up the great work!</p>
        </div>
    );

    return (
        <div className="bg-card border rounded-xl overflow-hidden shadow-sm">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
                <div className="flex items-center gap-3 mb-2">
                    <TrendingUp className="w-6 h-6" />
                    <h2 className="text-xl font-bold">Adaptive Learning Path</h2>
                </div>
                <p className="text-indigo-100 text-sm">AI-generated recommendations based on your quiz performance.</p>
            </div>

            <div className="p-6">
                {data.weak_topics.length > 0 && (
                    <div className="mb-6">
                        <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider mb-3">Focus Areas</h4>
                        <div className="flex flex-wrap gap-2">
                            {data.weak_topics.map((topic, i) => (
                                <span key={i} className="bg-red-50 text-red-700 px-3 py-1 rounded-full text-sm font-medium border border-red-100">
                                    {topic}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                <div className="space-y-4">
                    {data.recommendations.map((rec, i) => (
                        <div key={i} className="bg-muted/30 border rounded-lg p-4 hover:border-primary/50 transition-colors">
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="font-bold text-primary">{rec.topic}</h4>
                                <span className={`text-xs font-bold px-2 py-0.5 rounded ${rec.priority === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                                    {rec.priority} PRIORITY
                                </span>
                            </div>
                            <p className="text-sm text-muted-foreground mb-3">{rec.reason}</p>
                            <div className="flex items-center gap-2 text-sm font-medium text-foreground bg-background p-3 rounded border">
                                <ArrowRight className="w-4 h-4 text-primary" />
                                {rec.action_item}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdaptivePath;
