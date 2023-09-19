# pandemic-simple
Pythonic version of boardgame Pandemic. for learning purposes only. Buy the original boardgame.

Status: incomplete

Current status as of 18-sep-2023:
v0.1: targeted to be a simple version of the game.
- [x] graphics.py loads successfully, 
- [x] graphics.py has a link to main game.
- [x] graphics.py some elements are clickable.
- [x] graphics.py player movement implemented.
- [x] graphics.py cards are showing.
- [x] graphics.py action buttons are clickable.
- [x] graphics.py card buttons aren't clickable.
- [x] graphics.py movements that depend on cards are fully functional.
- [x] graphics.py movements that depend on research centers are functional.
- [ ] graphics.py incomplete: need to display other team members' cards in order to share knowledge.
- [ ] graphics.py incomplete: need to select multiple cards to discover cure.
- [x] engine.py board setup is complete,
- [ ] engine.py game dynamics is incomplete,
- [ ] engine.py action buttons don't count as moves
- [ ] engine.py required Pawn move countdown function,
- [ ] engine.py required Pawn end of turn function,
- [x] engine.py game dynamics is not linking to graphics.py

TBD v0.2
- [ ] graphics.py aesthetics: game messages box.
- [ ] graphics.py aesthetics: selected city info box.

TBD v0.3: targeted to be a playable version of the game over the internet
- [ ] tbd server.py responsible for game server management and database.
- [ ] figure out how to use something like Heroku to deploy the server.
- [ ] figure out how to deliver the interface to different users.

TBD v0.4:
- [ ] tbd refactor engine.py to be more modular
- [ ] tbd refactor graphics.py to be more modular and simpler.
- [ ] tbd refactor config.yaml to split game configs and display configs
- [ ] tbd refactor config.yaml to enable language localization

TBD v0.5:
- [ ] tbd refactor graphics.py to be browser-based

### To run the game
Not yet possible.
However, graphics.py loads the board in a PyGame canvas.


