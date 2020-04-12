*For contribution guidelines, check out [CONTRIBUTING.md](CONTRIBUTING.md)*

##### What are the scopes for MapBot during GSSoC 2020?

MapBot is one of the projects open for contribution under [GSSoC 2020](https://www.gssoc.tech/projects.html).

During the GSSoC term, the primary scopes for MapBot would be around:

- NLP improvements
    - [ ] Increase the training data set through various methods (crowd sourcing, public datasets etc.)
    - [ ] Try out different NLP models (Sequence to Sequence Models, Ensemble Classification Models etc.) and word vectorization techniques (word2vec, tfidf)
    - [ ] Retraining of models after a certain number of incorrect responses have been given as input by users

- Containerizing the application
    - [x] Set up docker-compose
    - [x] Persist data in db and automate schema initialisation and data seeding

- Broad-ranging API integration
    - [ ] Places API
    - [ ] Distance Matrix API
    - [x] Elevation API
    - [x] Geocoding API
    - [ ] Geolocation API
    - [ ] Roads API
    - [x] Time Zone API

- Broad-ranging UI integration
    - [ ] Facebook Messenger
    - [ ] Whatsapp
    - [x] Telegram
    - [ ] Slack

#### What are the expectations from participants during GSSoC 2020?

- This project is suitable for participants who find their skills aligning to the scopes as described above.
- Following is the proficiency expected from participants based on the level of tasks.
  - The codebase is in Python, so **at least** beginner proficiency in the language is expected to pick up any task.
  - Beginner level tasks would be suitable for those completely new to Open Source Contribution, these tasks would help you get in the gear for further contributions to the project. Look for the <kbd>beginner</kbd> label in open issues.
  - Easy level tasks would require understanding the project. These would still be tasks that could typically be completed in a couple of hours. Look for the <kbd>easy</kbd> label in opne issues.
  - Medium level tasks would be specific modules of the bigger picture. These would consume a few hours so make sure you get your cup of coffee. Look for the <kbd>medium</kbd> label in open issues.
  - Hard level tasks will be gamechangers! Look for the <kbd>hard</kbd> label in open issues.
- The mentors and admin will be extremely liberal with points awarded to participants as long as participants respect the correct methodology of contribution.
- Participants are required to strictly follow the guidelines while attempting a task and raising pull requests.
- All task issues would be created with a description of the requirements, if participants find any ambiguity/require clarification, feel free to start a thread on the issue tagging any mentor/admin. GitHub should be the primary medium to ask for clarifications on a specific issue.
- Participants are expected to be creative, if you feel that an approach towards the issue is better for the project, do speak up! Express your idea on the issue thread, we might even create new issues and assign them to you to implement your idea! Remember more issues = more points for grabs!
- If a participant wishes to try out something entirely new (beyond the scopes of the project), talk to the mentor and admins! We would be more than willing to adapt, the idea should of course align with the goals. Brownie points for thinking out of the box!
- Mentors and project admin would support participants throughout the contribution period (and beyond) but never code out the solution.
- Make sure you are respectful of others participants, mentors and admin. Take criticism positively and share positive feedback whenever you feel like.

#### Debugging
Use the `init.py` file to debug any changes made to the bot (with or without the API) before pushing it into your GitHub branch.
