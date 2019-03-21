import psycopg2
import psycopg2.extras
import sys
sys.path.append("../")
import config


def create_db_conn():
    """ Returns a database connection """
    return psycopg2.connect(host=config.host,
                            database=config.database,
                            user=config.user,
                            password=config.password)


def create_db_cur(db_conn):
    """ Returns a database cursor. Fetches data as a dictionary """
    return db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
