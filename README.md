# MapBot

#### Hey! I'm your friendly navigator bot! Try me out, not to brag but I'm FUN!



#### What I do?

I aim to give users a new way to interact with Google Maps through engaging text-based conversational interfaces.

#### How old am I?

I'm only a baby bot right now, I need you to feed me with logic, data and inspiration.

#### What is the motivation behind building me?

The primary motivation of the developers of MapBot is to provide a playground to tech enthusiasts, both beginners and advanced to try algorithms, approaches and ideas while contributing to a real-life project.

#### What I aspire to be one day?

- I want to help users in the most comprehensive way.
- I want to give 'geeks' a platform to try out all things 'cool'.

------

#### Are you here for GSSoC 2020?

Check out all related information [here](GSSoC.md)

------

#### What are some pre-requisites?

- MySQL
  - Install the community version of mySQL from the [official mySQL documentation page](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/).
  - Create root user credentials during installation.
  - Verify the installation, running the command  `mysql -uroot -p -hlocalhost` should open the mySQL monitor. (Enter the root password when prompted)
- StanfordCoreNLP
  - StanfordCoreNLP has a dependency on Java 8. `java -version` should complete successfully with version 1.8 or higher.
  - Windows- Download as a .zip file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  
  - Linux and MacOS- Follow the instructions to download the file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).

#### How to set me up?

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost`
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package in the repository and keep the file names `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Add config.py file to .gitignore to avoid pushing changes made to config
- Run `git rm --cached config.py`
- Edit the `config.py` file with the corresponding values
  - user = "root"
  - password = <your_root_password>
  - host = "localhost"
  - database = "mapbot"
  - key = <your_Google_Cloud_API_key>
  - stanford_path_to_jar = <your_path_to_stanford-corenlp-x.x.x.jar>
  - stanford_path_to_models_jar = <your_path_to_stanford-corenlp-x.x.x-models.jar>
  - javahome = <your_path_to_jdk_bin_java.exe>
- Install dependencies from `requirements.txt` file. Run `pip install -r requirements.txt`
- You're all set up, run the `init.py` file. `python init.py`
- It is recommended that you set this project up in a virtual environment to keep the dependencies separated and for easier debugging. Here's how you can do that -
    1. [Python](https://realpython.com/python-virtual-environments-a-primer/#why-the-need-for-virtual-environments)
    2. [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

------

#### What are some pre-requisites? (with Docker)

- StanfordCoreNLP
  - StanfordCoreNLP has a dependency on Java 8. `java -version` should complete successfully with version 1.8 or higher.
  - Windows- Download as a .zip file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  
  - Linux and MacOS- Follow the instructions to download the file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  
- Docker
  - Take a look at [this](https://docs.docker.com/install/) for detailed installation instructions for Docker on Windows, Linux and Mac systems.
  - Verify the installations by `docker --version` and `docker-compose --version`
- You won't need to download MySQL locally to make Docker work, but it's recommended as a pre-requisite to be able to debug programs outside Docker.

#### How to set me up Docker style?
- Clone the repository
- Unzip the StanfordCoreNLP package in the repository. Make sure the StanfordCoreNLP folder you downloaded in the prerequisite steps are in the cloned repository folder.
- Add config.py file to .gitignore to avoid pushing changes made to config
- Run `git rm --cached config.py`
- Modify *only* the following fields in `config.py` file with the corresponding values:
  - key = <your_Google_Cloud_API_key>
- You're all set up, kick off with `start.sh` file by running `bash start.sh`.

------
#### How do I work?

The analysis folder contains data files for the project. The sentences.csv contains the base training dataset which is used to classify the user's input into three classes - Statement, Question, and Chat. Going through some examples would clarify the difference between statement and chat. The featuresDump.csv is the result of text pre-processing done using the code in features.py and featuresDump.py.

------
#### Want to see me in action?

Here's a [Medium article](http://bit.ly/39Y9WCq) with the some superficial explanations, there are some video links too!
