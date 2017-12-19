import os
import json
import psycopg2
from falcon.testing import TestCase
from app.app import get_app, create_app
from app.config import DATABASE_URL


class AppTestCase(TestCase):

    def setUp(self):
        super(AppTestCase, self).setUp()
        self.api = get_app()
        self._init_tables()

    @staticmethod
    def _init_tables():
        DATABASE_URL = os.getenv('DATABASE_URL')
        initialization_query = "SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name"
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute(initialization_query)
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("TRUNCATE TABLE " + row[1] + " CASCADE;")
        cursor.close()
        connection.close()
