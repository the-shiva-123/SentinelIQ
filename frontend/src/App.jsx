import { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const initialHistory = [
  {
    id: 1,
    role: 'assistant',
    content:
      'SentinelIQ is ready. Ask about auth failures, routing behavior, or suspicious telemetry clusters.',
    meta: { route: 'route', label: 'System ready' },
  },
];

function App() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState(initialHistory);
  const [pending, setPending] = useState(false);

  const metrics = useMemo(
    () => [
      { label: 'Total Records Embedded', value: '174', tone: 'cyan' },
      { label: 'Chroma Sync Status', value: 'Active', tone: 'emerald' },
      { label: 'Current Model Wrapper', value: 'gemini-2.5-flash', tone: 'violet' },
    ],
    []
  );

  const sendQuery = async (event) => {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: trimmed,
      meta: { route: 'user' },
    };

    setHistory((prev) => [...prev, userMessage]);
    setInput('');
    setPending(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: trimmed }),
      });

      const data = await response.json().catch(() => ({}));
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response || data.message || 'The analysis stream has been captured. Review the routed insight below.',
        meta: {
          route: data.route || 'retrieve_rag',
          file: data.file || 'logs/telemetry.trace',
          code: data.code || 'ERR_AUTH_401',
        },
      };

      setHistory((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const fallbackMessage = {
        id: Date.now() + 2,
        role: 'assistant',
        content:
          'A local backend route was not reachable, so SentinelIQ rendered a resilient fallback response with the expected structure.',
        meta: {
          route: 'fallback',
          file: 'ops/incident_review.md',
          code: 'ERR_AUTH_401',
        },
      };
      setHistory((prev) => [...prev, fallbackMessage]);
    } finally {
      setPending(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="ambient ambient-a" />
      <div className="ambient ambient-b" />
      <div className="ambient ambient-c" />

      <main className="dashboard-grid">
        <aside className="left-panel glass-card">
          <div className="panel-header">
            <p className="eyebrow">SentinelIQ</p>
            <h1>Mission Control</h1>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <motion.div
              className="orbits"
              whileHover={{ scale: 1.03, rotate: 4 }}
              transition={{ type: 'spring', stiffness: 200, damping: 18 }}
            >
              <div className="torus" />
              <div className="node node-1" />
              <div className="node node-2" />
              <div className="node node-3" />
            </motion.div>
          </div>

          <div className="metric-stack">
            {metrics.map((metric) => (
              <motion.article
                key={metric.label}
                className={`metric-card metric-${metric.tone}`}
                whileHover={{ y: -4, scale: 1.01 }}
                transition={{ type: 'spring', stiffness: 220, damping: 20 }}
              >
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
              </motion.article>
            ))}
          </div>
        </aside>

        <section className="main-panel glass-card">
          <div className="chat-header">
            <div>
              <p className="eyebrow">Live analysis stream</p>
              <h2>AI log intelligence</h2>
            </div>
            <div className="status-pill">● Secure</div>
          </div>

          <div className={`chat-feed ${pending ? 'pending' : ''}`}>
            <AnimatePresence initial={false}>
              {history.map((message) => (
                <motion.div
                  key={message.id}
                  className={`message-row ${message.role}`}
                  initial={{ opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  transition={{ duration: 0.25, ease: 'easeOut' }}
                >
                  <div className="message-bubble">
                    <div className="message-meta">
                      <span>{message.role === 'user' ? 'Query' : 'Analysis'}</span>
                      {message.meta?.route && (
                        <span className="route-pill">Route: {message.meta.route}</span>
                      )}
                    </div>
                    <p>{message.content}</p>
                    {message.meta?.file && (
                      <div className="code-card">
                        <div className="code-header">
                          <span>{message.meta.file}</span>
                          <span className="code-tag">{message.meta.code}</span>
                        </div>
                        <pre>
                          <code>{`function inspect() {\n  return "${message.meta.code}";\n}`}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <form className="composer" onSubmit={sendQuery}>
            <label className="input-shell">
              <span className="input-icon">✦</span>
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask SentinelIQ about the latest anomaly…"
                aria-label="Query input"
              />
            </label>
            <button type="submit" disabled={pending}>
              {pending ? 'Scanning…' : 'Analyze'}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;
