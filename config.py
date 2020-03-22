import os
user = "root"
password = "Ritikjain@1272"
host = "localhost"
database = "mapbot"
port = "3306"
key = "AIzaSyBuHPXeUJKVTiHwjY8m9bw4Rvv1fYOCxmk"  # Will be provided by mentors

# your_path_to_stanford-corenlp-x.x.x.jar
stanford_path_to_jar = "../stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2.jar"

# your_path_to_stanford-corenlp-x.x.x-models.jar
stanford_path_to_models_jar = "../stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar"


# DONOT CHANGE THE VALUES BELOW DURING INITIAL CONFIGURATION SET UP

docker = os.getenv("DOCKER")
if(docker=="Y"):
    # print("Inside Docker")
    user = os.getenv('dockeruser')
    password = os.getenv('dockerpassword')
    host = os.getenv('dockerhost')
    javahome = os.getenv('dockerjavahome')
