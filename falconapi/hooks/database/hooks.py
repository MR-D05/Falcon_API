import falcon
from falconapi.utilities.database.resources import connection


def generate_cursor(req, resp, resource, params): 
    db = connection()
    resource.db = db
    resource.cursor = db.cursor()


def kill_cursor(req, resp, resource):
    db = connection()
    resource.cursor.close()

