# MapBot

#### Hey! I'm your friendly navigator bot! Try me out, not to brag but I'm FUN!



##### What I do?

I aim to give users a new way to interact with Google Maps through engaging text-based conversational interfaces. 

##### How old am I?

I'm only a baby bot right now, I need you to feed me with logic, data and inspiration.

##### What is the motivation behind building me?

The primary motivation of the developers of MapBot is to provide a playground to tech enthusiasts, both beginners and advanced to try algorithms, approaches and ideas while contributing to a real-life project. 

##### What I aspire to be one day?

- I want to help users in the most comprehensive way.
- I want to give 'geeks' a platform to try out all things 'cool'.

------

##### What are the scopes for MapBot during GSSoC 2020?

MapBot is one of the projects open for contribution under [GSSoC 2020](https://www.gssoc.tech/). 

During the GSSoC term, the primary scopes for MapBot would be around:

- NLP algorithm
- Containerizing the application
- Broad-ranging API integration
- Broad-ranging UI integration

------

##### What are some pre-requisites?

-  MySQL 
  - Install the community version of mySQL from the [official mySQL documentation page](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/). 
  - Create root user credentials during installation.
  - Verify the installation, running the command  `mysql -uroot -p -hlocalhost` should open the mySQL monitor. (Enter the root password when prompted)
- StanfordCoreNLP
  - StanfordCoreNLP has a dependency on Java 8. `java -version` should complete successfully with version 1.8 or higher. 
  - Windows- Download as a .zip file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  
  - Linux and MacOS- Follow the instructions to download the file from [here](https://stanfordnlp.github.io/CoreNLP/download.html).  

##### How to set me up?

- Clone the repository
- Create the **mapbot** database in mySQL
  -  `mysql -uroot -p -hlocalhost` 
  - Enter root password when prompted
  - `create database mapbot;`
  - Verify creation of the database `show databases;`
- Unzip the StanfordCoreNLP package and keep the path to `stanford-corenlp-x.x.x.jar` and `stanford-corenlp-x.x.x-models.jar` handy.
- Edit the config.py file with the corresponding values
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

------

##### Want to see me in action?

Here's a Medium article with the some superficial explanations, there are some video links too!

