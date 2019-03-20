import psycopg2
import psycopg2.extras
import sys
sys.path.append("../")
import db_config


def create_db_conn():
    """ Returns a database connection """
    return psycopg2.connect(host=db_config.host,
                            database=db_config.database,
                            user=db_config.user,
                            password=db_config.password)


def create_db_cur(db_conn):
    """ Returns a database cursor. Fetches data as a dictionary """
    return db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
