import databaseconnect
import config
import pytest
import mysql.connector as mysql


class TestClass:
    @pytest.fixture(scope="session", autouse=True)
    def setup_init(self):
        # Will be executed before the first test
        main_database = config.database
        config.database = "test"
        try:
            test_db = mysql.connect(
                host=config.host,
                user=config.user,
                passwd=config.password,
                database=config.database,
            )

            cursor = test_db.cursor()
            cursor.execute("CREATE DATABASE {}".format(config.database))
            print("test database created")

        except Exception:
            print("Failed to create test database")
            # rolling back to main db
            config.database = main_database
            pytest.exit("Exiting test!")

        yield test_db

        # Will be executed after the last test is executed
        try:
            mycursor = test_db.cursor()
            mycursor.execute("DROP DATABASE {}".format(config.database))
            mycursor.close()
            print("test database deleted.")

        except Exception:
            print("Failed to delete test database.")

        config.database = main_database

    def test_setup_database(self):
        db = databaseconnect.setup_database()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        expected_tables = [
            ("chat_table"),
            ("statement_table"),
            ("question_table"),
            ("directions_table"),
        ]
        assert tables.sort() == expected_tables.sort()

    def test_add_to_database_of_chat_table(self):
        db = databaseconnect.add_to_database("C", "subject", "root", "verb", "H")
        cursor = db.cursor()
        cursor.execute(
            "select * from chat_table where root_word='root' and verb='verb' and sentence='H'"
        )
        res = cursor.fetchone()[0]
        assert res == 1

    def test_add_to_database_of_question_table(self):
        db = databaseconnect.add_to_database("Q", "subject", "root", "verb", "H")
        cursor = db.cursor()
        cursor.execute(
            "select * from question_table where subject='subject' and root_word='root' and verb='verb' and sentence='H'"
        )
        res = cursor.fetchone()[0]
        assert res == 1

    def test_add_to_database_of_statement_table(self):
        db = databaseconnect.add_to_database("O", "subject", "root", "verb", "H")
        cursor = db.cursor()
        cursor.execute(
            "select * from statement_table where subject='subject' and root_word='root' and verb='verb' and sentence='H'"
        )
        res = cursor.fetchone()[0]
        assert res == 1

    def test_get_chat_response(self):
        response = databaseconnect.get_chat_response()
        assert type(response) is str

    def test_get_question_response_without_subject(self):
        response = databaseconnect.get_question_response("[]", "root", "verb")
        assert type(response) is tuple

    def test_get_question_response_with_subject(self):
        response = databaseconnect.get_question_response("subject", "root", "verb")
        assert type(response) is tuple

    def test_add_learnt_statement_to_database(self):
        db = databaseconnect.add_learnt_statement_to_database("subject", "root", "verb")
        cursor = db.cursor()
        cursor.execute(
            "select * from question_table where subject='subject' and root_word='root' and verb='verb'"
        )
        res = cursor.fetchone()[0]
        assert res == 1

    def test_learn_question_response(self):
        response = databaseconnect.learn_question_response("H")
        assert type(response) is tuple

    def test_clear_table_with_chat_table(self, monkeypatch):
        from io import StringIO

        yes = StringIO("y\n")
        monkeypatch.setattr("sys.stdin", yes)

        db = databaseconnect.clear_table("chat_table")

        cursor = db.cursor()
        cursor.execute("select * from chat_table")
        entries = cursor.fetchone()
        assert entries is None

    def test_clear_table_with_statement_or_question_table(self, monkeypatch):
        from io import StringIO

        yes = StringIO("y\n")
        monkeypatch.setattr("sys.stdin", yes)

        db = databaseconnect.clear_table("statement_table")

        cursor = db.cursor()
        cursor.execute("select * from statement_table")
        entries_1 = cursor.fetchone()

        cursor.execute("select * from question_table")
        entries_2 = cursor.fetchone()

        assert entries_1 is None and entries_2 is None
