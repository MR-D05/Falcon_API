import io
import os
import re
import uuid
import mimetypes
import falcon
import collections
import json
import smtplib
from psycopg2 import IntegrityError
from falconapi.hooks.verification.hooks import authenticate, validate
from falconapi.hooks.database.hooks import generate_cursor, kill_cursor
from falconapi.utilities.password.resources import hash, verify
from falconapi.utilities.token.resources import generate_token


@falcon.before(generate_cursor)
@falcon.after(kill_cursor)
class UserCollection(object):


    @falcon.before(authenticate)
    def on_get(self, req, resp, username):
        try:
            resp.body = json.dumps(username)
            resp.status = falcon.HTTP_200
        except:
            raise falcon.HTTPBadRequest
        finally:
            if len(req.cookies) == 0:
                resp.location = '/index.html'
                

    @falcon.before(authenticate)
    def on_post(self, req, resp, username):
        try:
            self.cursor.callproc('fetch_user', [username])
            result = self.cursor.fetchone()[0]
            status = result['is_admin']
            if status:
                resp.location = '/admins.html'
                resp.body = json.dumps(username)
            else:
                resp.location = '/users.html'
                resp.body = json.dumps(username)
        except (TypeError, KeyError):
            raise falcon.HTTPBadRequest
            
            
    @falcon.before(validate)
    def on_put(self, req, resp):
        email = req.context['d']['email_address']
        username = req.context['d']['username']
        encrypted_password = hash(req.context['d']['password'])
        self.cursor.callproc('insert_user', [email, username, encrypted_password])
        result = self.cursor.fetchone()[0]
        id = result['id']
        token = generate_token(128)
        self.cursor.callproc('insert_token', [id, token])
        resp.set_cookie("SSSNTKN", token, secure=False)
        resp.location = '/users.html'
        resp.status = falcon.HTTP_200


    def on_delete(self, req, resp):
        email = req.context['Data']['Email']
        username = req.context['Data']['Username']
        encrypted_password = hashpw(req.context['Data']['Password'])
        self._user_store.delete(email, username, password)


@falcon.before(generate_cursor)
@falcon.after(kill_cursor)
class PasswordResource(object):
    

    def on_post(self, req, resp):
        try:
            email_address = req.context['d']['user_email']
            self.cursor.callproc('fetch_user_by_email', [email_address])
            result = self.cursor.fetchone()[0]
            verify_token = verify(result['reset_password_token'], req.context['d']['reset_token'])
            if verify_token:
                json.dumps(result['username'])
                resp.location = '/password_reset.html'
                resp.status = falcon.HTTP_200
        except:
            raise falcon.HTTPBadRequest


    @falcon.before(authenticate)
    def on_put(self, req, resp, username):
        try:
            new_password = hash(req.context['d']['new_password'])
            self.cursor.callproc('update_password', [username, new_password])
            result = self.cursor.fetchone()[0]
            if result:
                resp.location = '/index.html'
                resp.status = falcon.HTTP_200
        except (TypeError, KeyError):
             raise falcon.HTTPBadRequest


@falcon.before(generate_cursor)
@falcon.after(kill_cursor)
class PasswordResetRequestResource(object):
    

    def on_post(self, req, resp):
        try:
            email_address = req.context['d']['user_email']
            print(email_address)
            self.cursor.callproc('fetch_user_by_email', [email_address])
            result = self.cursor.fetchone()[0]
            print(result)
            token = hash(result['reset_password_token'])
            fromaddr = 'examplefalconapismtpserver@gmail.com'
            toaddrs  = email_address
            msg = token
            username = 'examplefalconapismtpserver@gmail.com'
            password = 'asdfasdfasdfasdf'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
        except (TypeError):
            raise falcon.HTTPBadRequest


