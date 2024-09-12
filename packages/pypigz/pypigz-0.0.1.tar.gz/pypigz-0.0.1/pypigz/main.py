from pypigz.connection import mysql_connection, execute_query
from pypigz.product import Product
from mysql.connector.errors import ProgrammingError


def main(file_path, merchant_id, host, user, passwd, database, port):
    """
    Main function to insert data into the database

    :param file_path: Excel file path
    :param merchant_id: Merchant id
    :param host: Database host
    :param user: Database user
    :param passwd: Database password
    :param database: Database name
    :param port: Database port
    :return: Success message or error message
    """
    try:
        conn = mysql_connection(host=host, user=user, database=database, port=port, passwd=passwd)
        product = Product(merchant_id)
        data = product.read_excel(file_path)

        if isinstance(data, str):
            return data
        else:
            product_data = product.generate_product_data(data)
            sql_product = product.generate_sql_for_product(conn, product_data)
            if "Não foi possível encontrar a categoria" in sql_product:
                conn.close()
                return sql_product
            else:
                execute_query(conn, sql_product)
                sql_product_platform = product.generate_sql_for_product_platform(conn)
                execute_query(conn, sql_product_platform)
                conn.close()
                return "Data inserted successfully"

    except ProgrammingError as e:
        return f"Ocorreu um erro ao executar a consulta SQL. Por favor, verifique a sintaxe e tente novamente. {e}"
    except Exception as e:
        return f"Ocorreu um erro: {e}"