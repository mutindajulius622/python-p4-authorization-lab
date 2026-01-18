#!/usr/bin/env python3

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

import pytest
from app import app
from models import db, User, Article
from faker import Faker
from random import randint, choice as rc

@pytest.fixture(scope='module', autouse=True)
def seed_db():
    with app.app_context():
        Article.query.delete()
        User.query.delete()
        db.create_all()
        
        fake = Faker()

        print("Creating users...")
        users = []
        usernames = []
        for i in range(25):

            username = fake.first_name()
            while username in usernames:
                username = fake.first_name()
            
            usernames.append(username)

            user = User(username=username)
            users.append(user)

        db.session.add_all(users)

        print("Creating articles...")
        articles = []
        for i in range(100):
            content = fake.paragraph(nb_sentences=8)
            preview = content[:25] + '...'
            
            article = Article(
                author=fake.name(),
                title=fake.sentence(),
                content=content,
                preview=preview,
                minutes_to_read=randint(1,20),
                is_member_only = rc([True, False, False])
            )

            articles.append(article)

        db.session.add_all(articles)
        
        db.session.commit()