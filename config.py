import os
from dotenv import load_dotenv

if os.getenv("DOCKER") == "Y":
    load_dotenv("ENV/docker.env")
else:
    load_dotenv("ENV/.env")

""" MAKE SURE you have filled environment variables in `.env` files in `./ENV/` folder"""

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DATABASE")
port = os.getenv("DB_PORT")
key = os.getenv("GCLOUD_API_KEY")  # Will be provided by mentors
tbot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# your_path_to_stanford-corenlp-x.x.x.jar
stanford_path_to_jar = os.getenv("STANFORD_PATH_TO_JAR")

# your_path_to_stanford-corenlp-x.x.x-models.jar
stanford_path_to_models_jar = os.getenv("STANFORD_PATH_TO_MODELS_JAR")

# for eg. 'C:\\Program\ Files\\Java\\jdk1.8.0_201\\bin\\java.exe' or '/usr/local/openjdk-11/bin/java'
javahome = os.getenv("JAVAHOME")
