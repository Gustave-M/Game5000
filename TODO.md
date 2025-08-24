# 🚀 TODO

- [ ] Proper user management (not based only on `sid`), scalable to support more than 7 users *(currently pending)*
  - Rooms, UserEntity = (pas sid mais UUID ou DB id, (coockie local)), GameManadger (gère l'attente, ...), Flask-Socket-io room
  - Use Flask-coockei, SECREAT-KEY et pas UUID, prévoit JWT pour plusieurs serveurs
- [ ] Allow players to choose their seat upon joining
- [ ] Add a maximum play time per turn (otherwise move player to waiting list)
- [ ] Embed 3D dice models + positioning based on the current turn
- [ ] Add message animations:  
  - Points gained  
  - Loss  
  - Full-hand  
  - Victory / Defeat
- [ ] Chat intégration
- [ ] BDD d'historique
- [ ] Faire une doc
- [ ] directory '/docs' avec install.md, architecture.md, ..., 'pdoc --html mon_module'