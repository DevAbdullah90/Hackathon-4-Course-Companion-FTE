import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, User } from 'lucide-react';
import api from '../lib/api';

interface AITutorProps {
    context: string;
}

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const AITutor: React.FC<AITutorProps> = ({ context }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const toggleChat = () => setIsOpen(!isOpen);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const res = await api.post('/premium/chat', {
                message: userMsg.content,
                context: context
            });

            const aiMsg: Message = { role: 'assistant', content: res.data.response };
            setMessages(prev => [...prev, aiMsg]);
        } catch (err) {
            console.error("Chat error", err);
            const errorMsg: Message = { role: 'assistant', content: "Sorry, I'm having trouble connecting to the AI Tutor right now." };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* Floating Action Button */}
            <button
                onClick={toggleChat}
                className="fixed bottom-8 right-8 bg-primary text-primary-foreground p-4 rounded-full shadow-lg hover:opacity-90 transition-all z-50 flex items-center justify-center cursor-pointer"
            >
                {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6" />}
            </button>

            {/* Chat Window */}
            {isOpen && (
                <div className="fixed bottom-24 right-8 w-96 h-[500px] bg-card border rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-4">

                    {/* Header */}
                    <div className="bg-primary/10 p-4 border-b flex items-center gap-3">
                        <div className="p-2 bg-primary/20 rounded-lg">
                            <Bot className="w-5 h-5 text-primary" />
                        </div>
                        <div>
                            <h3 className="font-bold text-sm">AI Tutor</h3>
                            <p className="text-xs text-muted-foreground">Ask me anything about this lesson!</p>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.length === 0 && (
                            <div className="text-center p-8 text-muted-foreground text-sm">
                                <p>👋 Hi! I'm your AI Tutor.</p>
                                <p className="mt-2">I've read the lesson. What questions do you have?</p>
                            </div>
                        )}
                        {messages.map((m, i) => (
                            <div key={i} className={`flex gap-3 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-secondary' : 'bg-primary/20'}`}>
                                    {m.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4 text-primary" />}
                                </div>
                                <div className={`p-3 rounded-2xl text-sm max-w-[80%] ${m.role === 'user'
                                        ? 'bg-primary text-primary-foreground rounded-br-none'
                                        : 'bg-muted rounded-bl-none'
                                    }`}>
                                    {m.content}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex gap-3">
                                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                                    <Bot className="w-4 h-4 text-primary" />
                                </div>
                                <div className="bg-muted p-3 rounded-2xl rounded-bl-none text-sm self-start">
                                    <span className="animate-pulse">Thinking...</span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-4 border-t bg-card">
                        <form
                            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                            className="flex gap-2"
                        >
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Type your question..."
                                className="flex-1 bg-muted px-4 py-2 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                            />
                            <button
                                type="submit"
                                disabled={loading || !input.trim()}
                                className="bg-primary text-primary-foreground p-2 rounded-xl hover:opacity-90 transition-all disabled:opacity-50 cursor-pointer"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </form>
                    </div>

                </div>
            )}
        </>
    );
};

export default AITutor;
