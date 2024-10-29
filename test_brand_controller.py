import pytest
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from brand_controller import app, db, security

class TestBase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_test_user()

    def create_test_user(self):
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.datastore = user_datastore

        if not user_datastore.find_user(email="test@example.com"):
            user_datastore.create_user(email="test@example.com", password=generate_password_hash("password"))
        db.session.commit()

    def login(self):
        return self.client.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)

class TestBrandController(TestBase):
    def test_browse_brands(self):
        self.login()
        response = self.client.get('/brand')
        assert response.status_code == 200
        assert b'brand/browse.html' in response.data

    def test_view_sub_brand(self):
        self.login()
        brand = self.create_random_brand()
        response = self.client.get(f'/brand/{brand.id}')
        assert response.status_code == 200
        assert b'brand/brand_view.html' in response.data

    def create_random_brand(self):
        brand = Brand(name="Test Brand")
        db.session.add(brand)
        db.session.commit()
        return brand

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

if __name__ == '__main__':
    pytest.main()