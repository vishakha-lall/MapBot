import logging
import logger_config

log = logging.getLogger(__name__)
log.info('Entered module: %s' % __name__)


@logger_config.logger
def connection_to_database():
    import config
    import mysql.connector
    from time import sleep

    max_tries = 10
    tries = 1
    conn = None
    while tries <= max_tries:
        try:
            conn = mysql.connector.connect(
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port,
                database=config.database,
            )
            if conn.is_connected():
                # logging.debug("Connected")
                logging.debug('MySQL connected')
                break

        except mysql.connector.Error as e:
            tries += 1
            print(e, "...Retrying")
            sleep(20)
    try:
        if conn.is_connected():
            # logging.debug("Connected")
            logging.debug('MySQL connected')
            return conn
    except:
        raise Exception("DATABASE NOT CONNECTED")


@logger_config.logger
# setup database
def setup_database():
    db = connection_to_database()
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chat_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS statement_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS question_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS directions_table(id INTEGER PRIMARY KEY AUTO_INCREMENT, origin_location VARCHAR(100), destination_location VARCHAR(100))")


@logger_config.logger
# add classified sentences to database
def add_to_database(classification, subject, root, verb, H):
    db = connection_to_database()
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    if classification == 'C':
        cur.execute(f"INSERT INTO chat_table(root_word,verb,sentence) VALUES ('{root}','{verb}','{H}')")
        db.commit()
    elif classification == 'Q':
        cur.execute("SELECT sentence FROM question_table")
        res = cur.fetchall()
        exist = 0
        for r in res:
            if r[-1] == H:
                exist = 1
                break
        if exist == 0:
            # do not add if question already exists
            cur.execute(f"INSERT INTO question_table(subject,root_word,verb,sentence) VALUES ('{subject}','{root}','{verb}','{H}')")
            db.commit()
    else:
        cur.execute("SELECT sentence FROM statement_table")
        res = cur.fetchall()
        exist = 0
        for r in res:
            if r[-1] == H:
                exist = 1
                break
        if exist == 0:    # do not add if question already exists
            cur.execute(f"INSERT INTO statement_table(subject,root_word,verb,sentence) VALUES ('{subject}','{root}','{verb}','{H}')")
            db.commit()


@logger_config.logger
# get a random chat response
def get_chat_response():
    db = connection_to_database()
    cur = db.cursor()
    cur = db.cursor(buffered=True)
    cur.execute("SELECT COUNT(*) FROM chat_table")
    res = cur.fetchone()
    total_chat_records = res[0]
    import random
    chat_id = random.randint(1, total_chat_records+1)
    cur.execute(f"SELECT sentence FROM chat_table WHERE id = {chat_id}")
    res = cur.fetchone()
    B = res[0]
    return B


@logger_config.logger
def get_question_response(subject, root, verb):
    db = connection_to_database()
    cur = db.cursor(buffered=True)
    if str(subject) == '[]':
        cur.execute("SELECT verb FROM statement_table")
        res = cur.fetchall()
        found = 0
        for r in res:
            if r[-1] == str(verb):
                found = 1
                break
        if found == 1:
            cur.execute(f"SELECT sentence FROM statement_table WHERE verb='{verb}'")
            res = cur.fetchone()
            B = res[0]
            return B, LearnResponse.MESSAGE.name
        else:
            B = "Sorry I don't know the response to this. Please train me."
            return B, LearnResponse.TRAIN_ME.name
    else:
        cur.execute("SELECT subject FROM statement_table")
        res = cur.fetchall()
        found = LearnResponse.MESSAGE.name
        for r in res:
            if r[-1] == str(subject):
                found = 1
                break
        if found == 1:
            cur.execute(f"SELECT verb FROM statement_table WHERE subject='{subject}'")
            res = cur.fetchone()
            checkVerb = res[0]   # checkVerb is a string while verb is a list. checkVerb ['verb']
            if checkVerb == '[]':
                cur.execute(f"SELECT sentence FROM statement_table WHERE subject='{subject}'")
                res = cur.fetchone()
                B = res[0]
                return B, LearnResponse.MESSAGE.name
            else:
                if checkVerb[2:-2] == verb[0]:
                    cur.execute(f"SELECT sentence FROM statement_table WHERE subject='{subject}'")
                    res = cur.fetchone()
                    B = res[0]
                    return B, LearnResponse.MESSAGE.name
                else:
                    B = "Sorry I don't know the response to this. Please train me."
                    return B, LearnResponse.TRAIN_ME.name
        else:
            B = "Sorry I don't know the response to this. Please train me."
            return B, LearnResponse.TRAIN_ME.name


@logger_config.logger
def add_learnt_statement_to_database(subject, root, verb):
    db = connection_to_database()
    cur = db.cursor()
    cur.execute(f"INSERT INTO statement_table(subject,root_word,verb) VALUES ('{subject}','{root}','{verb}')")
    db.commit()


@logger_config.logger
def learn_question_response(H):
    db = connection_to_database()
    cur = db.cursor(buffered=True)
    cur.execute("SELECT id FROM statement_table ORDER BY id DESC")
    res = cur.fetchone()
    last_id = res[0]
    cur.execute(f"UPDATE statement_table SET sentence='{H}' WHERE id={last_id}")
    db.commit()
    B = "Thank you! I have learnt this."
    return B, LearnResponse.MESSAGE.name


def clear_table(table_name):
    db = connection_to_database()
    cur = db.cursor()

    if table_name in ("question_table", "statement_table"):
        tables_to_be_cleaned = ("question_table", "statement_table")
        print("The following tables will be cleaned:\n")
        for table in tables_to_be_cleaned:
            describe_table(cur, table)

        if input("Enter 'Y' to confirm cleaning of BOTH tables: ") in ("Y", "y"):
            for table in tables_to_be_cleaned:
                cur.execute("DELETE FROM {table}")
            db.commit()
            print("Tables cleaned successfully")
        else:
            print("Table cleaning skipped.")

    else:
        print("The following table will be cleaned:\n")
        describe_table(cur, table_name)

        if input("Enter 'Y' to confirm: ") in ("Y", "y"):
            print("Table cleaned successfully")
            cur.execute(f"DELETE FROM {table_name}")
            db.commit()
        else:
            print("Table cleaning skipped.")


def describe_table(cursor, table_name, cur):
    cur.execute(f"DESC {table_name}")
    res = cur.fetchall()
    column_names = [col[0] for col in res]

    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    res = cur.fetchall()
    records_no = res[0][0]

    print("Table Name:", table_name)
    print("Columns:", column_names)
    print("Number of existing records:", records_no)
    print()