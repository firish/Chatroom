import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

from create_tables import User, Message, Like  

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'postgresql://postgres:Rsg007..@localhost:5432/nimble_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

def create_mock_data():
    # Create two users
    john = User(email="john.doe@example.com", name="John Doe", password="hashed_password_john")
    jane = User(email="jane.doe@example.com", name="Jane Doe", password="hashed_password_jane")

    # Add users to the database
    db.session.add(john)
    db.session.add(jane)
    db.session.commit()

    # Create three messages between them
    message1 = Message(content="Hello from John!", timestamp=datetime.utcnow(), sender_id=john.id, receiver_id=jane.id)
    message2 = Message(content="Hello back from Jane!", timestamp=datetime.utcnow(), sender_id=jane.id, receiver_id=john.id)
    message3 = Message(content="How are you, Jane?", timestamp=datetime.utcnow(), sender_id=john.id, receiver_id=jane.id)

    # Add messages to the database
    db.session.add(message1)
    db.session.add(message2)
    db.session.add(message3)
    db.session.commit()

    # Add an upvote to the second message from John
    upvote = Like(message_id=message2.id, user_id=john.id, value=1)

    # Add the upvote to the database
    db.session.add(upvote)
    db.session.commit()

    print("Mock data added successfully!")


if __name__ == "__main__":
    with app.app_context():
        create_mock_data()
