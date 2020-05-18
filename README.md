<p align="center">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg">
</p>
<p align="center">
  <a href="https://travis-ci.com/vishakha-lall/MapBot">
    <img alt="Travis CI Build Status" src="https://travis-ci.com/vishakha-lall/MapBot.svg?branch=gssoc-master">
  </a>
  <a href="https://github.com/vishakha-lall/MapBot/">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/vishakha-lall/MapBot?color=darkblue&label=%20&logo=github">
  </a>
</p>

# MapBot :earth_africa:

#### Hey! I'm your friendly navigator bot! Try me out, not to brag but I'm FUN!



### What I do?

I aim to give users a new way to interact with Google Maps through engaging text-based conversational interfaces.

### How old am I?

I'm only a baby bot right now, I need you to feed me with logic, data and inspiration.

### What is the motivation behind building me?

The primary motivation of the developers of MapBot is to provide a playground to tech enthusiasts, both beginners and advanced to try algorithms, approaches and ideas while contributing to a real-life project.

### What I aspire to be one day?

- I want to help users in the most comprehensive way.
- I want to give 'geeks' a platform to try out all things 'cool'.

------

### Are you here for GSSoC 2020?

Check out all related information [here](GSSoC.md)

------

### What are some pre-requisites?

- MySQL
  - Install the community version of mySQL from the [official mySQL documentation page](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).
  - Create root user credentials during installation.
  - Verify the installation, running the command  `mysql -uroot -p -hlocalhost` should open the mySQL monitor. (Enter the root password when prompted)
- StanfordCoreNLP
  - StanfordCoreNLP has a dependency on Java 8. `java -version` should complete successfully with version 1.8 or higher.
  - Windows- Download as a .zip file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  
  - Linux and MacOS- Follow the instructions to download the file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).

-----

### Setting Up

<details>
<summary><strong>How to set me up on CLI?</strong></summary>
<br>

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file paths `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Run `git update-index --assume-unchanged ENV/.env`
- Fill the existing template in `ENV/.env` with the corresponding values following the `KEY=VALUE` format
- Install dependencies from `requirements.txt` file. Run `pip install -r requirements.txt`
- You're all set up, run the `init.py` file. `python init.py`
- It is recommended that you set this project up in a virtual environment to keep the dependencies separated and for easier debugging. Here's how you can do that -
    1. [Python](https://realpython.com/python-virtual-environments-a-primer/#why-the-need-for-virtual-environments)
    2. [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

</details>

------

<details>
<summary><strong>How to set me up with an UI?</strong></summary>
<br>

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file paths `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Run `git update-index --assume-unchanged ENV/.env`
- Fill the existing template in `ENV/.env` with the corresponding values following the `KEY=VALUE` format
- Install dependencies from `requirements.txt` file. Run `pip install -r requirements.txt`
- You're all set up. Execute `python webapp.py` to start up the server.
- Visit `http://127.0.0.1:5000/` to interact with your MapBot.
- It is recommended that you set this project up in a virtual environment to keep the dependencies separated and for easier debugging. Here's how you can do that -
    1. [Python](https://realpython.com/python-virtual-environments-a-primer/#why-the-need-for-virtual-environments)
    2. [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

</details>

------

<details>
<summary><strong>How to deploy on Docker?</strong></summary>
<br>

#### What are some pre-requisites? (with Docker)

- Docker
  - Take a look at [this](https://docs.docker.com/install/) for detailed installation instructions for Docker on Windows, Linux and Mac systems.
  - Verify the installations by `docker --version` and `docker-compose --version`

#### How to set me up Docker style?
- Clone the repository
- Fill up the `GCLOUD_API_KEY` in `ENV/docker.env`
- Run `docker-compose up`
- Visit `localhost:5000` to interact with the deployment

</details>

------

<details>
<summary><strong>How to set me up on Telegram?</strong></summary>
<br>

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file paths `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Run `git update-index --assume-unchanged ENV/.env`
- Fill the existing template in `ENV/.env` with the corresponding values following the `KEY=VALUE` format
- For `TELEGRAM_BOT_TOKEN=<YOUR_API_KEY_HERE>`, open your Telegram app and follow [this](https://core.telegram.org/bots#creating-a-new-bot) tutorial on how to create a new bot on Telegram and get your own bot token. Once your token is generated, update the `.env` file in `/ENV` with it.
- Find your bot on Telegram using `@bot_username` that you chose, and send the first text to your new bot. Nothing is supposed to happen for now. No worries.
- Install dependencies from `requirements.txt` file. Run `pip install -r requirements.txt`
- You're all set up, run the `telegram.py` file. `python telegram.py` and converse with your bot in real time.

</details>

------

<details>
<summary><strong>How to set me up on Slack?</strong></summary>
<br>

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file paths `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Run `git update-index --assume-unchanged ENV/.env`
- Fill the existing template in `ENV/.env` with the corresponding values following the `KEY=VALUE` format
- Follow the steps prompted [here](https://api.slack.com/apps?new_classic_app=1) to create a **classic** slack app. Navigate to **Basic Information** section of the slack app. Under the **Add features and functionality** subheading click on **Bots**. Click on **Add Legacy Bot User** and enter the **display name** and **default username** of your bot. Navigate to **Basic Information** section of the slack app on the sidebar and copy the **Client ID** and **Client Secret** and then paste these to the `ENV/.env` file as: `SLACK_CLIENT_ID=<Your Client ID>` and `SLACK_CLIENT_SECRET=<Your Client Secret>`. Navigate to the **OAuth & Permissions** section. Under the **Redirect URLs** subheading add `http://localhost:5000/post_auth`.
- Install dependencies from `requirements.txt` file. Run `pip install -r requirements.txt`
- Run `python app.py`. The server will start at your localhost. Navigate to `http://localhost:5000/begin_auth`. Click `Add to Slack` button. Select the workspace from the top right and hit `Allow`. Successfully completing this step would automate the creation of  `SLACK_BOT_TOKEN` in the `ENV/.env` file.
- In another terminal, run `python slackbot.py`.
- Open the workspace in Slack and invite the bot to the channel: `@YOUR_BOT_DEFAULT_USERNAME` message in the channel. Click on **Invite to Channel**.

</details>

------

<details>
<summary><strong>How to set me up on Facebook Messenger?</strong></summary>
<br>

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file paths `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Run `git update-index --assume-unchanged ENV/.env`
- Fill the existing template in `ENV/.env` with the corresponding values following the `KEY=VALUE` format
- Create Facebook app from [here](https://developers.facebook.com/). Fill out basic information.
- Set Up **Messenger** option under Add a Product.
- Generate the **Access Token** by creating a facebook page for your bot by clicking on **Create New Page** button.
- Click on **Add or Remove Pages** and add your facebook page just created.
- Click on **Generate Token** and copy the token to the `ENV/.env` file as `ACCESS_TOKEN=<YOUR_ACCESS_TOKEN>`.
- Install [ngrok](https://gist.github.com/jwebcat/ecaac7bc7ee26e01cd4a).
- Open a terminal window, type `ngrok http 5000`. Once you do this, a screen will appear with a link after the  “Forwarding” section — make sure to copy the link that begins with “https”.
- Click on **Add Callback URL** under **Webhooks** section. Paste the above link in the **Callback URL**. Add **Verify Token** of your choice. Copy Verify Token you added in the `ENV/.env` file as `VERIFY_TOKEN=YOUR_VERIFY_TOKEN`. Hit **Verify and Save**
- Click on **Add Subscriptions**. Check **messages, messaging_postbacks, message_deliveries, messaging_pre_checkouts** boxes.
- Run `python app.py`
- You can interact with bot on Facebook Messenger.

</details>

------

### How do I work?

The `/analysis` folder contains data files for the project. The `sentences.csv` contains the base training dataset which is used to classify the user's input into three classes - *Statement*, *Question*, and *Chat*. Going through some examples would clarify the difference between statement and chat. The `featuresDump.csv` is the result of text pre-processing done using the code in `features.py` and `featuresDump.py`.

------
### Want to see me in action?

Here's a [Medium article](http://bit.ly/39Y9WCq) with the some superficial explanations, there are some video links too!
