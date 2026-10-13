import React, {useState, useEffect, useRef} from 'react';
import {createRoot} from 'react-dom/client';
import Markdown from 'react-markdown';
import './style.css';
const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
async function request(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 60000);
  try {
    const res = await fetch(API + path, {...options, signal: controller.signal});
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(typeof data.detail === 'string' ? data.detail : 'Message invalide ou trop long.');
    }
    return res.status === 204 ? null : await res.json();
  } catch (err) {
    if (err.name === 'AbortError') throw new Error('Délai dépassé. Le serveur peut encore traiter la demande ; commence une nouvelle conversation si nécessaire.');
    if (err instanceof TypeError) throw new Error('Serveur inaccessible. Vérifie que FastAPI est démarré.');
    throw err;
  } finally { clearTimeout(timer); }
}
function App() {
  const [messages, setMessages] = useState([]);
  const [id, setId] = useState(null);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const bottom = useRef(null);
  useEffect(() => {bottom.current?.scrollIntoView({behavior:'smooth'});}, [messages, busy]);
  async function send(e) {
    e.preventDefault();
    if (busy) return;
    const text = input.trim();
    if (!text) {setError('Écris un message avant de l’envoyer.'); return;}
    setBusy(true); setError('');
    try {
      const data = await request('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:text, conversation_id:id})});
      setId(data.conversation_id);
      setMessages(prev => [...prev, {role:'user', content:text}, {role:'assistant', content:data.answer}]);
      setInput('');
    } catch(err) {setError(err.message);}
    finally {setBusy(false);}
  }
  async function reset() {
    setBusy(true); setError('');
    try {
      if (id) await request('/chat/' + id, {method:'DELETE'});
      setId(null); setMessages([]); setInput('');
    } catch(err) {setError(err.message + ' La conversation actuelle est conservée.');}
    finally {setBusy(false);}
  }
  return <div className="layout">
    <aside>
      <div className="brand">py<span>coach</span><sup> / TP</sup></div>
      <p className="eyebrow">TON TUTEUR PYTHON</p>
      <h1>Comprendre.<br/>Essayer.<br/>Progresser.</h1>
      <p>Un espace pour poser tes questions, comprendre tes erreurs et apprendre à ton rythme.</p>
      <button className="new" disabled={busy} onClick={reset}>+ Nouvelle conversation</button>
      <details><summary>Ce que je peux faire</summary><p>Bases Python, listes, boucles, fonctions, débogage simple et environnements virtuels.</p></details>
      <details><summary>Limites d’utilisation</summary><p>Je peux me tromper et je n’exécute pas ton code. Vérifie les exemples. Ne partage pas de clé API ni de données sensibles. Pas de diagnostic médical ni d’aide à l’intrusion. Historique temporaire, limité à 20 échanges.</p></details>
      <small>Projet pédagogique · FastAPI + React<br/>Les messages sont envoyés à Groq.</small>
    </aside>
    <main>
      <header><strong>Atelier Python</strong><span>Débutants · Français</span></header>
      <section className="messages" aria-label="Conversation" aria-live="polite" aria-busy={busy}>
        {!messages.length && <div className="welcome"><div className="icon">&gt;_</div><h2>Qu’aimerais-tu comprendre ?</h2><p>Commence par une question ou un petit extrait de code.</p><div className="suggestions">{['Explique la boucle for avec un exemple.', 'Quelle différence entre une liste et un tuple ?', 'À quoi sert un environnement virtuel ?'].map(q => <button key={q} disabled={busy} onClick={()=>setInput(q)}>{q}<span>↗</span></button>)}</div></div>}
        {messages.map((m,i)=><article key={i} className={m.role}><div className="label">{m.role==='user'?'TOI':'PYCOACH'}</div><Markdown>{m.content}</Markdown></article>)}
        {busy && <p className="loading" role="status">Traitement en cours…</p>}
        <div ref={bottom}/>
      </section>
      <footer>{error && <p role="alert" className="error">{error}</p>}<form onSubmit={send}><label htmlFor="message">Ta question</label><textarea id="message" value={input} disabled={busy} maxLength={4000} rows={3} placeholder="Ex. Pourquoi mon code affiche-t-il une erreur ?" onChange={e=>setInput(e.target.value)}/><div className="formbar"><small>{input.length}/4000 caractères</small><button disabled={busy} type="submit">Envoyer →</button></div></form></footer>
    </main>
  </div>;
}
createRoot(document.getElementById('root')).render(<App/>);
