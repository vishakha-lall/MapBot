import mysql.connector

db = mysql.connector.connect(user='root',password='viks1995',host='127.0.0.1',database='mapbot')
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS chat_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), sentence VARCHAR(200))")
cur.execute("CREATE TABLE IF NOT EXISTS statement_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), sentence VARCHAR(200))")
cur.execute("CREATE TABLE IF NOT EXISTS question_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), sentence VARCHAR(200))")
