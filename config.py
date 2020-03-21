import os
import dotenv

dotenv.load_dotenv()

user = os.getenv('mapbotuser')
password = os.getenv('mapbotpassword')
host = os.getenv('mapbothost')
database = os.getenv('mapbotdatabase')
port = os.getenv('mapbotport')
key = os.getenv('mapbotkey')

stanford_path_to_jar = os.getenv('stanford_path_to_jar')

stanford_path_to_models_jar = os.getenv('stanford_path_to_models_jar')

javahome = os.getenv('javahome')


# DONOT CHANGE THE VALUES BELOW DURING INITIAL CONFIGURATION SET UP

docker = os.getenv("DOCKER"):
if(docker=="Y"):
    # print("Inside Docker")
    user = os.getenv('dockeruser')
    password = os.getenv('dockerpassword')
    host = os.getenv('dockerhost')
    javahome = os.getenv('dockerjavahome')
