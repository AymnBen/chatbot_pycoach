# PyCoach — TP chatbot spécialisé
Projet pédagogique Mundiapolis / Pr. H. Ayad. Binôme : Aymen Benbouhia + nom à compléter.

## Ce qui est fourni
- Phase 1 : `notebooks/TP_PyCoach.ipynb`, identité, boucle, historique, deux prompts,
  dix scénarios et génération d’un tableau de réponses réelles.
- Phase 2 : backend FastAPI structuré et interface React responsive.
- `.env.example`, ce README et `TESTS_WEB.md`.
- Tests techniques avec fournisseur simulé : aucun résultat LLM fabriqué.

Réutilisation des supports : uv/Python 3.12, dotenv et client OpenAI configuré pour
Groq. Le TP résumé de site apporte les rôles system/user et Markdown ; ici, le
scraping n’est pas nécessaire, on ajoute un historique de dialogue.

## 1. Installer sous Windows (PowerShell)
Extraire l’archive : le dossier racine `pycoach` contient ce README, pyproject.toml,
backend, frontend et notebooks. Exemple si placé dans C:\Users\Aymn\pycoach :

```powershell
cd C:\Users\Aymn\pycoach
uv sync
Copy-Item .env.example .env
```
La copie est à faire une seule fois, si `.env` n’existe pas. Ouvrir `.env` dans Cursor,
coller la clé Groq après GROQ_API_KEY= et enregistrer. Ne pas modifier l’ancien
`.env` du projet `projet_ia` ; recopier uniquement la valeur nécessaire dans le nouveau.
Le modèle est configurable avec MODEL si votre compte n’y a pas accès.

## 2. Phase 1 : notebook
Ouvrir le dossier pycoach dans Cursor, puis notebooks/TP_PyCoach.ipynb.
Choisir le kernel de `pycoach/.venv` (Python 3.12), puis exécuter de haut en bas.
Dans la cellule d’évaluation, passer LANCER_EVALUATION à True pour effectuer
24 appels API. Évaluer les résultats du CSV généré, le recharger dans le notebook,
compléter l’analyse et enregistrer avec Ctrl+S. Renseigner le deuxième membre du binôme.
Ne pas présenter le tableau comme évalué avant cette étape.

## 3. Phase 2 : backend (terminal 1)
Depuis la racine pycoach :
```powershell
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Santé : http://127.0.0.1:8000/health
Documentation interactive : http://127.0.0.1:8000/docs
Laisser ce terminal ouvert. Les modifications de .env nécessitent un redémarrage.

## 4. Phase 2 : frontend (terminal 2)
Installer Node.js LTS depuis https://nodejs.org/ si absent. Vite utilisé dans ce projet
nécessite Node 20.19+ ou 22.12+ ; utiliser une version LTS récente compatible.
Fermer/rouvrir le terminal après installation puis :
```powershell
node --version
npm --version
cd C:\Users\Aymn\pycoach\frontend
npm.cmd install
npm.cmd run dev
```
Ouvrir http://localhost:5173. `npm.cmd` évite le blocage de npm.ps1 par PowerShell.
L’API cible http://127.0.0.1:8000. Si besoin, la personnaliser avec VITE_API_URL dans
un fichier frontend/.env (aucune clé Groq dans le frontend).

## 5. Contrôles
Depuis la racine :
```powershell
uv run pytest -q
```
Depuis frontend :
```powershell
npm.cmd run build
```
Suivre TESTS_WEB.md pour les contrôles navigateur réels et les dix scénarios.
Les résultats du modèle demandent la clé de votre compte : ils ne sont pas livrés
préexécutés. Tests techniques et qualité des réponses sont deux vérifications distinctes.

## Routes
- GET /health : état du serveur (ne contacte pas Groq).
- POST /chat : JSON {"message":"Explique une liste"}. Réponse : conversation_id et answer.
- Pour poursuivre, renvoyer conversation_id dans le prochain POST /chat.
- DELETE /chat/{conversation_id} : efface l’historique, réponse 204.
- 422 : entrée invalide ; 404 : conversation perdue/inconnue ; 429 : quota ;
  502 : fournisseur en erreur ; 503 : configuration/clé ; 504 : délai dépassé.

## Structure et explication
- backend/prompts.py : versions V1/V2 du comportement.
- backend/chat.py : composition des messages, appel modèle et gestion des erreurs.
- backend/main.py : validation Pydantic, routes et mémoire distincte par identifiant.
- backend/config.py : variables d’environnement et CORS pour le port 5173.
- backend/scenarios.py : situations fictives pour l’évaluation.
- frontend/src/main.jsx : état React, appels API, attente, erreurs et nouvelle conversation.
- frontend/src/style.css : affichage ordinateur et mobile.

## Limites et choix techniques
Application locale pédagogique, sans authentification : ne pas l’exposer publiquement.
Historique en mémoire, perdu au redémarrage ; chaque onglet démarre sa conversation.
Un seul worker ; verrou global pour empêcher les mises à jour concurrentes incohérentes
(compromis pédagogique : les requêtes sont sérialisées). Maximum 20 échanges par
conversation, 4 000 caractères par message. Un déploiement réel nécessiterait une
base de données, authentification, limites de débit, nettoyage mémoire et supervision.
Le frontend attend au plus 60 s, le fournisseur 45 s par requête ; en cas de timeout
navigateur le serveur peut encore achever la demande. Markdown rendu sans HTML brut.
La spécialisation est guidée par prompt, pas garantie : l’évaluation sert à constater
les limites. Aucun entraînement ou fine-tuning n’est exigé par ce TP.

## À remettre
Notebook avec sorties réelles, appréciations et analyse ; backend et frontend ;
.env.example sans secret ; README. Compléter le binôme et TESTS_WEB.md.
Ne pas inclure .env, .venv, node_modules ou caches dans le rendu.

## Références
- Supports fournis : Installation et utilisation de uv, Cursor et Ollama ;
  tp-resume-site.ipynb ; TP_Chatbot_Specialise.pdf.
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/models
- https://fastapi.tiangolo.com/tutorial/cors/
- https://vite.dev/guide/
