from datetime import UTC, datetime
from pypigz.connection import mysql_connection, fetch_query
from uuid import uuid4
import pandas as pd

class Product:
    """
    Class to handle product data and generate SQL queries to insert data into the database
    """
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
        self.category_id: int = 10775
        self.name: str = ''
        self.slug: str = ''
        self.category_name: str = ''
        self.description = ''
        self.price: float = 0
        self.start_price = self.price
        self.checkpad = 1
        self.ordersheet = 1
        self.pigzpay = 1
        self.marketplace = 1
        self.pigz_kiosk = 1
        self.removed = 0
        self.created = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        self.updated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        self.type = 1

    def generate_sql_for_product(self, conn, data):
        """
        Generate SQL query to insert product data into the database
        :param conn:
        :param data:
        :return: sql query
        """
        product_values = []
        category_names = {product['Categoria'] for product in data}
        categories = self.get_categories(conn, category_names)

        for product in data:
            category_id = categories.get(product['Categoria'])
            if category_id is None:
                return f"Não foi possível encontrar a categoria {product['Categoria']}"
            self.name = product['Nome']
            self.slug = self.slugify()
            self.category_id = category_id
            self.price = product['Preço']
            self.start_price = self.price

            product_value = f"({self.merchant_id}, {self.category_id}, SUBSTRING('{self.name}',1,50), '{self.slug}', '{self.description}', {self.price}, {self.start_price}, {self.checkpad}, {self.ordersheet}, {self.pigzpay}, {self.marketplace}, {self.removed}, '{self.created}', '{self.updated}', {self.type})"
            product_values.append(product_value)

        sql = f"""
        INSERT INTO product (merchant_id, product_category_id, name, slug, description, price, start_price, checkpad,
                              order_sheet, pigzpay, marketplace, removed, created, updated, type)
        VALUES {', '.join(product_values)};
        """
        return sql

    def generate_sql_for_product_platform(self, conn):
        """
        Generate SQL query to insert product platform data into the database
        :param conn:
        :return:
        """
        query = f"""
        SELECT id
        FROM product
        WHERE merchant_id = {self.merchant_id}
        AND created BETWEEN DATE_SUB(NOW(), INTERVAL 1 MINUTE) AND NOW();
        """
        product_ids = fetch_query(conn, query)
        product_platform_values = [
            f"({product_id[0]}, {self.marketplace}, {self.pigzpay}, {self.checkpad}, {self.ordersheet}, {self.pigz_kiosk})"
            for product_id in product_ids]

        sql = f"""
        INSERT INTO product_platform (product_id, marketplace, pigzpay, checkpad, order_sheet, pigz_kiosk)
        VALUES {', '.join(product_platform_values)};
        """
        return sql

    @staticmethod
    def generate_product_data(data):
        """
        Generate product data from the excel data
        :param data:
        :return: List of product data
        """
        products = []
        for _, row in data.iterrows():
            product = {
                'Nome': row['Nome'],
                'Preço': row['Preço'],
                'Categoria': row['Categoria']
            }
            products.append(product)
        return products

    def get_categories(self, conn, category_names):
        """
        Get categories id by name from database
        :param conn:
        :param category_names:
        :return: Product category ids
        """
        names_str = "', '".join(category_names)
        query = f"""
        SELECT 
            id, category 
        FROM 
            product_category 
        WHERE 
            category IN ('{names_str}')
        AND removed = 0 
        AND merchant_id = {self.merchant_id};
        """
        result = fetch_query(conn, query)
        return {row[1]: row[0] for row in result}

    def read_excel(self, file_path: str):
        """
        Read excel file and validate data
        :param file_path:
        :return: Dataframe or error message
        """
        data = pd.read_excel(file_path)
        validate_data = self.validate_data(data)
        if isinstance(validate_data, str):
            return validate_data
        return data

    @staticmethod
    def validate_data(data):
        """
        Validate data from the excel file
        :param data:
        :return: None or error message
        """
        required_columns = ['Nome', 'Preço', 'Categoria']
        for column in required_columns:
            if column not in data.columns:
                return f'Coluna {column} não está presente no arquivo'
        for index, row in data.iterrows():
            if pd.isnull(row['Nome']) or pd.isnull(row['Preço']) or pd.isnull(row['Categoria']):
                return f'Linha {index + 2} está faltando dados obrigatórios'
            try:
                row['Preço'] = float(row['Preço'])
            except ValueError:
                return f'Linha {index + 2} tem um valor de Preço inválido: {row["Preço"]}'

        return True

    def slugify(self):
        """
        Generate slug for the product
        :return: New slug
        """
        return self.name.replace(" ", "-").lower() + "-" + uuid4().hex[:6]
