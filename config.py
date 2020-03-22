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

# for eg. 'C:\\Program\ Files\\Java\\jdk1.8.0_201\\bin\\java.exe' or '/usr/local/openjdk-11/bin/java'
javahome = '*your_path_to_jdk_bin_java.exe*'

# DONOT CHANGE THE VALUES BELOW DURING INITIAL CONFIGURATION SET UP

if os.getenv("DOCKER"):
    # print("Inside Docker")
    user = "root"
    password = "root"
    host = "db"
    javahome = '/usr/local/openjdk-11/bin/java'
