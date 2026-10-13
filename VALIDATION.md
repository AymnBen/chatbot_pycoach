# Vérifications effectuées avant livraison
- 11 tests pytest réussis : validation des entrées, contexte, isolation, reset,
  CORS, erreurs simulées et conservation de l’historique après échec.
- Notebook validé avec nbformat ; syntaxe de toutes les cellules Python vérifiée.
- Installation npm réussie et build Vite réussi (Vite 7.3.6).
- Aucun appel réel à Groq effectué : aucune clé fournie et aucun résultat inventé.
- Essai navigateur automatisé non exécuté : binaire Chromium absent dans
  l’environnement de préparation. Contrôles visuels et bout en bout à réaliser
  sur le PC de l’étudiant en suivant TESTS_WEB.md.

Le notebook doit encore être exécuté avec votre clé, ses résultats évalués et sa
courte analyse complétée avant remise au professeur.
