from src import postgreasy


def test_connect1():
    postgreasy.get_connection()
