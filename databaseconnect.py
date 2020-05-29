import logging
import logger_config
import chatbot

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


@logger_config.logger
def connection_to_database():
    import config
    import psycopg2
    from time import sleep
    import sys

    called_from = sys.argv[0]
    logging.debug(called_from)

    max_tries = 10
    tries = 1
    conn = None
    while tries <= max_tries:
        try:
            if called_from.endswith("pytest"):
                conn = psycopg2.connect(
                    user="test_mapbot",
                    password="",
                    host=config.host,
                    port=config.port,
                    dbname="pytest_testdb",
                )
            elif config.HEROKU_DATABASE_URL:
                conn = psycopg2.connect(config.HEROKU_DATABASE_URL, sslmode="require")
            else:
                conn = psycopg2.connect(
                    user=config.user,
                    password=config.password,
                    host=config.host,
                    port=config.port,
                    dbname=config.database,
                )
            if conn.status == 1:
                logging.debug("PostgreSQL connected")
                break

        except psycopg2.Error as e:
            tries += 1
            logging.debug(e)
            logging.debug("...Retrying")
            sleep(20)
    try:
        if conn.status == 1:
            logging.debug("PostgreSQL connected")
            return conn
    except Exception:
        raise Exception("DATABASE NOT CONNECTED")


@logger_config.logger
# setup database
def setup_database():
    db = connection_to_database()
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS chat_table (id SERIAL PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))"  # noqa: E501
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS statement_table (id SERIAL PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))"  # noqa: E501
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS question_table (id SERIAL PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))"  # noqa: E501
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS directions_table (id SERIAL PRIMARY KEY, origin_location VARCHAR(100), destination_location VARCHAR(100))"  # noqa: E501
    )
    cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    TABLES = cur.fetchall()
    db.commit()
    return TABLES


@logger_config.logger
# add classified sentences to database
def add_to_database(classification, subject, root, verb, H):
    db = connection_to_database()
    cur = db.cursor()
    try:
        if classification == "C":
            cur.execute(
                "INSERT INTO chat_table(root_word,verb,sentence) VALUES (%s, %s, %s)",
                (str(root), str(verb), H,),
            )
            db.commit()
        elif classification == "Q":
            cur.execute("SELECT sentence FROM question_table")
            res = cur.fetchall()
            exist = 0
            for r in res:
                if r[-1] == H:
                    exist = 1
                    break
            if exist == 0:
                # do not add if question already exists
                cur.execute(
                    "INSERT INTO question_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",
                    (str(subject), str(root), str(verb), H,),
                )
                db.commit()
        else:
            cur.execute("SELECT sentence FROM statement_table")
            res = cur.fetchall()
            exist = 0
            for r in res:
                if r[-1] == H:
                    exist = 1
                    break
            if exist == 0:  # do not add if question already exists
                cur.execute(
                    "INSERT INTO statement_table(subject,root_word,verb,sentence) VALUES (%s,%s,%s,%s)",
                    (str(subject), str(root), str(verb), H,),
                )
                db.commit()
    except Exception as e:
        return e
    else:
        return "Success"


@logger_config.logger
# get a random chat response
def get_chat_response():
    db = connection_to_database()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM chat_table")
    res = cur.fetchone()
    total_chat_records = res[0]
    import random

    chat_id = random.randint(1, total_chat_records)
    cur.execute("SELECT sentence FROM chat_table WHERE id = %s", (str(chat_id),))
    res = cur.fetchone()
    try:
        B = res[0]
    except Exception:
        B = "Hello, I'm MapBot! \U0001F44B"
    return B


@logger_config.logger
def get_question_response(subject, root, verb):
    db = connection_to_database()
    cur = db.cursor()
    if str(subject) == "[]":
        cur.execute("SELECT verb FROM statement_table")
        res = cur.fetchall()
        found = 0
        for r in res:
            if r[-1] == str(verb):
                found = 1
                break
        if found == 1:
            cur.execute(
                "SELECT sentence FROM statement_table WHERE verb= %s", (str(verb),)
            )
            res = cur.fetchone()
            B = res[0]
            return B, chatbot.LearnResponse.MESSAGE.name
        else:
            B = "Sorry I don't know the response to this. Please train me."
            return B, chatbot.LearnResponse.TRAIN_ME.name
    else:
        cur.execute("SELECT subject FROM statement_table")
        res = cur.fetchall()
        found = 0
        for r in res:
            if r[-1] == str(subject[0]):
                found = 1
                break
        if found == 1:
            cur.execute(
                "SELECT verb FROM statement_table WHERE subject= %s", (str(subject[0]),)
            )
            res = cur.fetchone()
            checkVerb = res[0]
            # checkVerb is a string while verb is a list. checkVerb ['verb']
            if checkVerb == "[]":
                cur.execute(
                    "SELECT sentence FROM statement_table WHERE subject= %s",
                    (str(subject[0]),),
                )
                res = cur.fetchone()
                B = res[0]
                return B, chatbot.LearnResponse.MESSAGE.name
            else:
                if checkVerb[2:-2] == verb[0]:
                    cur.execute(
                        "SELECT sentence FROM statement_table WHERE subject= %s",
                        (str(subject[0]),),
                    )
                    res = cur.fetchone()
                    B = res[0]
                    return B, chatbot.LearnResponse.MESSAGE.name
                else:
                    B = "Sorry I don't know the response to this. Please train me."
                    return B, chatbot.LearnResponse.TRAIN_ME.name
        else:
            B = "Sorry I don't know the response to this. Please train me."
            return B, chatbot.LearnResponse.TRAIN_ME.name


# May be redundant. Can be handled by add_to_database("O", subject, root, verb, H)
@logger_config.logger
def add_learnt_statement_to_database(subject, root, verb):
    db = connection_to_database()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO statement_table(subject,root_word,verb) VALUES (%s,%s,%s)",
        (str(subject), str(root), str(verb),),
    )
    db.commit()
    # return db
    return True


@logger_config.logger
def learn_question_response(H):
    db = connection_to_database()
    cur = db.cursor()
    cur.execute("SELECT id FROM statement_table ORDER BY id DESC")
    res = cur.fetchone()
    last_id = res[0]
    cur.execute(
        "UPDATE statement_table SET sentence = %s WHERE id = %s", (H, str(last_id),)
    )
    db.commit()
    B = "Thank you! I have learnt this."
    return B, chatbot.LearnResponse.MESSAGE.name


@logger_config.logger
def clear_table(table_name):
    db = connection_to_database()
    cur = db.cursor()

    if table_name in ("question_table", "statement_table"):
        tables_to_be_cleaned = ("question_table", "statement_table")
        logging.debug("The following tables will be cleaned:\n")
        for table in tables_to_be_cleaned:
            _describe_table(cur, table)

        if input("Enter 'Y' to confirm cleaning of BOTH tables: ") in ("Y", "y",):
            for table in tables_to_be_cleaned:
                cur.execute(f"DELETE FROM {table}")
            db.commit()
            logging.debug("Tables cleaned successfully")
        else:
            logging.debug("Table cleaning skipped.")

    elif table_name in ("chat_table", "directions_table"):
        logging.debug("The following table will be cleaned:\n")
        _describe_table(cur, table_name)

        if input("Enter 'Y' to confirm: ") in ("Y", "y"):
            cur.execute(f"DELETE FROM {table_name}")
            db.commit()
            logging.debug("Table cleaned successfully")
        else:
            logging.debug("Table cleaning skipped.")
    else:
        raise Exception("WRONG TABLE NAME")


def _describe_table(cur, table_name):
    cur.execute(
        f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    )  # using f-strings with the assumption that `table_name` will be correct
    res = cur.fetchall()
    column_names = [col[0] for col in res]

    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    # using f-strings with the assumption that `table_name` will be correct
    res = cur.fetchall()
    records_no = res[0][0]

    logging.debug(f"Table Name: {table_name}")
    logging.debug(f"Columns: {column_names}")
    logging.debug(f"Number of existing records: {records_no}")

    return records_no
