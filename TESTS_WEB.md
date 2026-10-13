# Vérification de bout en bout — à exécuter sur votre ordinateur
Les tests pytest simulent le fournisseur et vérifient la logique HTTP. Ils ne prouvent
ni la qualité des réponses Groq ni le fonctionnement réel du navigateur.

## Scénarios pédagogiques
Reprendre les dix scénarios de `backend/scenarios.py` dans React, avec V2.
Cliquer sur Nouvelle conversation entre chaque scénario ; conserver la conversation
entre les deux messages de C1 et C2. Noter attendu, obtenu, appréciation et amélioration
pour chacun. Comparer avec le tableau du notebook. Les réponses peuvent varier.

## Vérifications techniques
| Cas | Manipulation | Attendu | Observé |
|---|---|---|---|
| Message vide | Envoyer un texte composé d’espaces | Message clair, aucun appel au modèle | À compléter |
| Mémoire | C1, puis « Et si elle est vide ? » | Comprend la référence à la liste | À compléter |
| Réinitialisation | Nouvelle conversation, puis « Quelle était ma liste ? » | Ne connaît plus la liste | À compléter |
| Isolation | Deux onglets : parler d'une liste dans A, demander sa valeur dans B | B ne connaît pas les données de A | À compléter |
| Backend arrêté | Arrêter uvicorn avec Ctrl+C, puis envoyer | Erreur lisible, question conservée | À compléter |
| Modèle indisponible | Mettre temporairement BASE_URL_GROQ=http://127.0.0.1:9/v1 puis redémarrer backend | Erreur fournisseur lisible, pas de faux échange en historique | À compléter |
| Configuration restaurée | Rétablir l’adresse Groq et redémarrer backend | Conversation opérationnelle | À compléter |
| Mobile | Outils développeur du navigateur, largeur 390 px | Saisie et boutons accessibles, pas de débordement global | À compléter |

Ne jamais montrer la clé .env dans les captures. /health vérifie le serveur, pas l’accès à Groq.

Tests automatisés : 11 réussis en 4,24 secondes.
Un avertissement de dépréciation lié à Starlette/httpx.
Ces tests utilisent un modèle simulé et ne valident pas la qualité des réponses de Groq.
Compilation frontend : npm.cmd run build réussi en 7,44 secondes.

| Test | Résultat observé |
|---|---|
| Message vide | Message « Écris un message avant de l’envoyer. » |
| FastAPI arrêté | Erreur « Serveur inaccessible » et texte saisi conservé |
| FastAPI redémarré | Réponse du chatbot reçue |

Isolation des conversations vérifiée dans deux onglets : aucun partage du contexte observé

C2 — Adaptation au niveau débutant : partiel.
La réponse propose des exemples corrects, mais reste trop dense.
Amélioration : commencer par une fonction avec un seul paramètre,
expliquer la différence entre paramètre et argument, puis introduire
progressivement les valeurs par défaut et les arguments nommés.