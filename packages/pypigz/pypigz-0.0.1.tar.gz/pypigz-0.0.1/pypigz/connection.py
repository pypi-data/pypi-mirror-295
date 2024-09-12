from mysql.connector import connect

def mysql_connection(host, user, port, passwd=None, database=None):
    """
    Connect to a MySQL database
    :param host:
    :param user:
    :param port:
    :param passwd:
    :param database:
    :return: MySQL connection
    """
    connection = connect(
        host = host,
        user = user,
        port = port,
        passwd = passwd,
        database = database
    )
    return connection

def execute_query(connection, query):
    """
    Execute a SQL query
    :param connection:
    :param query:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

def fetch_query(connection, query):
    """
    Fetch the result of a SQL query
    :param connection:
    :param query:
    :return: SQL query result
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

