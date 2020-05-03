<p align="center">
  <a href="https://github.com/vishakha-lall/MapBot/issues?q=is%3Aopen+is%3Aissue+label%3Agssoc20">
    <img alt="GSSoC20" src="https://img.shields.io/github/issues/vishakha-lall/MapBot/gssoc20?color=orange&style=for-the-badge">
  </a>
</p>

<p align="center">
  <a href="https://github.com/vishakha-lall/MapBot/graphs/contributors">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors-anon/vishakha-lall/MapBot?color=red&logo=github&style=for-the-badge">
  </a>
</p>

<hr>

<p align="center">
  <a href="https://github.com/vishakha-lall/MapBot/issues?q=is%3Aopen+is%3Aissue+label%3Abeginner">
    <img alt="Beginner Issues" src="https://img.shields.io/github/issues/vishakha-lall/MapBot/beginner?color=purple&style=for-the-badge">
  </a>
  <a href="https://github.com/vishakha-lall/MapBot/issues?q=is%3Aopen+is%3Aissue+label%3Aeasy">
    <img alt="Easy Issues" src="https://img.shields.io/github/issues/vishakha-lall/MapBot/easy?color=mediumgreen&style=for-the-badge">
  </a>
</p>

<p align="center">
  <a href="https://github.com/vishakha-lall/MapBot/issues?q=is%3Aopen+is%3Aissue+label%3Amedium">
    <img alt="Medium Issues" src="https://img.shields.io/github/issues/vishakha-lall/MapBot/medium?color=darkgreen&style=for-the-badge">
  </a>
  <a href="https://github.com/vishakha-lall/MapBot/issues?q=is%3Aopen+is%3Aissue+label%3Ahard">
    <img alt="Hard Issues" src="https://img.shields.io/github/issues/vishakha-lall/MapBot/hard?color=darkblue&style=for-the-badge">
  </a>
</p>

#### Contribution Flow - How do I start contributing?
- Fork and clone this repository.
- Find an open issue that you find interesting. Go over to the [Issues](https://github.com/vishakha-lall/MapBot/issues) and look for active issues. Few things to keep in mind:
  - Only issues labelled as <kbd>gssoc20</kbd> are being monitored constantly. If you want to take up a different issue or suggest a new issue, get in touch with the mentors/project admin. They will certainly help you take it up. Follow the issue templates.
  - Select the issue based on the level of difficulty. Look out for the <kbd>beginner</kbd>, <kbd>easy</kbd>, <kbd>medium</kbd> and <kbd>hard</kbd> labels.
- Take a look at this [dummy issue](https://github.com/vishakha-lall/MapBot/issues/11) that describes the procedure of interacting on an issue.
  - Comment on the issue asking for any clarifications (Make sure you tag a mentor/project admin to notify them immediately).
  - Comment on the issue with your approach of resolving it.
  - Seek feedback from the mentor/project admin and ask them to assign the issue to you.
- *After* the issue is assigned to you, start working on it.
  - Make changes and add meaningful commit messages (that describe the commit neatly).
  - Complete all commits related to the issue.
- Perform quality checks locally in your cloned directory.
  - Run following tests:
    - `black --check .`
    - `flake8 . --count --select=E101,E722,E9,F4,F63,F7,F82,W191 --show-source --statistics`
    - `flake8 . --count --exit-zero --max-line-length=127 --statistics`
  - Change any files according to errors:
    - For `psf/black` formatting errors, running `black <file_name>` on the file you are working on will automatically remove formatting errors. Refer [this site](https://black.readthedocs.io/en/stable/editor_integration.html) for editor integration of `psf/black`, to avoid performing this step each time manually.
    - For `flake8` errors, look up the error code and try to solve it. If error persists, contact the mentors / project admin.
  - If changes are made in `chatbot.py`, it's mandatory to run `pytest test_chatbot.py -v` and post the screenshot of the results with the raised PR.
- Testing your code locally for **logical errors** before raising a PR must be done by using `pytest -v --ignore test_chatbot.py`
- Once tested locally with zero failed tests, raise a pull request with the title `<issue_title>\_resolved` over [gssoc-master](https://github.com/vishakha-lall/MapBot/tree/gssoc-master) as the base branch. Do not raise the PR over the master branch, if the contribution is meant for `GSSoC20`.
  - Refer to the [dummy pull request](https://github.com/vishakha-lall/MapBot/pull/12) that describes the correct procedure to raise a PR. Stick to the directions to make merging and reviewing easier and faster. Follow the PR template.
  - Refer to the issue (`Fixes #<issue_number>`)
  - Write a clear description of changes made to resolve the issue.
  - Tag a mentor/project admin to review the changes and merge the PR
- Repeat with a new issue!
