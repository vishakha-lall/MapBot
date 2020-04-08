import databaseconnect


class TestClass:
    def test_setup_database(self):
        tables = databaseconnect.setup_database()
        expected_tables = [
            ("chat_table",),
            ("directions_table",),
            ("question_table",),
            ("statement_table",),
        ]
        assert sorted(tables) == sorted(expected_tables)

    def test_add_to_database_of_chat_table(self):
        res = databaseconnect.add_to_database("C", "subject", "root", "verb", "H")
        assert res == "Success"

    def test_add_to_database_of_question_table(self):
        res = databaseconnect.add_to_database("Q", "subject", "root", "verb", "H")
        assert res == "Success"

    def test_add_to_database_of_statement_table(self):
        res = databaseconnect.add_to_database("O", "subject", "root", "verb", "H")
        assert res == "Success"

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
        res = databaseconnect.add_learnt_statement_to_database(
            "subject", "root", "verb"
        )
        # test not needed
        # handled by test_add_to_database_of_statement_table()
        assert res

    def test_learn_question_response(self):
        response = databaseconnect.learn_question_response("H")
        assert type(response) is tuple
