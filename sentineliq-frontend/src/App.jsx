import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Shield, Cpu, Send, Loader2 } from 'lucide-react';
import Background3D from './components/Background3D';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      role: 'assistant',
      answer: 'Telemetry node initialized. Standby to analyze system log streams.',
      routing: 'system_init'
    }
  ]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userPrompt = query;
    setQuery('');
    setLoading(true);

    // Mount user's prompt directly inside memory log array state
    setChatHistory(prev => [...prev, { role: 'user', answer: userPrompt }]);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userPrompt }),
      });
      
      const data = await response.json();
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        answer: data.answer, 
        routing: data.routing 
      }]);
    } catch (error) {
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        answer: 'Failed to negotiate token handshakes with backend vector nodes. Ensure FastAPI is running.', 
        routing: 'error_network' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full px-4 py-8 md:px-12 selection:bg-cyan-500/30">
      {/* Floating 3D Canvas Space */}
      <Background3D />

      {/* Top Glassmorphic Navigation Bar */}
      <header className="mx-auto max-w-6xl mb-8 flex items-center justify-between p-4 glass-panel rounded-2xl">
        <div className="flex items-center space-x-3">
          <Shield className="h-6 w-6 text-cyan-400 drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]" />
          <h1 className="text-xl font-bold tracking-wider text-white">SENTINEL<span className="text-cyan-400">IQ</span></h1>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="font-mono tracking-tight">VECTOR COMPILER ACTIVE</span>
        </div>
      </header>

      <main className="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Telemetry Widgets */}
        <div className="lg:col-span-1 flex flex-col space-y-4">
          <div className="p-4 glass-panel rounded-2xl flex items-center space-x-3">
            <Cpu className="text-purple-400 h-5 w-5" />
            <div>
              <p className="text-[10px] text-slate-400 font-semibold tracking-wider">EMBED MATRIX</p>
              <p className="text-sm font-semibold text-white font-mono">text-embedding-005</p>
            </div>
          </div>
          <div className="p-4 glass-panel rounded-2xl flex items-center space-x-3">
            <Terminal className="text-cyan-400 h-5 w-5" />
            <div>
              <p className="text-[10px] text-slate-400 font-semibold tracking-wider">CORE GENERATOR</p>
              <p className="text-sm font-semibold text-white font-mono">gemini-2.5-flash</p>
            </div>
          </div>
        </div>

        {/* Center Chat Interaction Screen */}
        <div className="lg:col-span-3 flex flex-col h-[65vh] glass-panel rounded-2xl overflow-hidden">
          <div className="flex-1 p-6 overflow-y-auto space-y-4">
            <AnimatePresence initial={false}>
              {chatHistory.map((msg, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.25 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] p-4 rounded-xl text-sm ${
                    msg.role === 'user' 
                      ? 'bg-cyan-500/10 text-cyan-200 border border-cyan-500/30 shadow-[0_0_15px_rgba(6,182,212,0.05)]' 
                      : 'bg-slate-900/40 text-slate-200 border border-slate-800/80'
                  }`}>
                    <p className="leading-relaxed font-sans">{msg.answer}</p>
                    {msg.routing && (
                      <span className="inline-block mt-2 text-[9px] uppercase font-mono bg-black/40 text-slate-400 px-2 py-0.5 rounded border border-slate-800">
                        DECISION: {msg.routing}
                      </span>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {loading && (
              <div className="flex justify-start">
                <div className="p-4 bg-slate-900/40 border border-slate-800 rounded-xl flex items-center space-x-2 text-sm text-slate-400">
                  <Loader2 className="h-4 w-4 animate-spin text-cyan-400" />
                  <span className="font-mono text-xs">Traversing LangGraph sequence pipeline...</span>
                </div>
              </div>
            )}
          </div>

          {/* Prompt Form Entry Bar */}
          <form onSubmit={handleSubmit} className="p-4 border-t border-slate-800 bg-slate-950/20 flex items-center space-x-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Query telemetry database assets or diagnostic errors..."
              className="flex-1 bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-500/40 transition-colors placeholder-slate-600"
            />
            <button
              type="submit"
              disabled={loading}
              className="p-3 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-900 text-white rounded-xl transition-colors cursor-pointer disabled:text-slate-600 border border-cyan-500/20"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}