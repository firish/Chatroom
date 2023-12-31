"""
This module defines a Flask server with associated API endpoints for user registration, 
authentication, messaging, and managing likes for messages. It also integrates with a 
PostgreSQL database using SQLAlchemy to store users, messages, likes, and some constants.
"""

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Enable CORS so that the client can communicate with the server.
CORS(app, origins=["http://localhost:3000"])


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rsg007..@localhost/nimble_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning
db = SQLAlchemy(app)


class User(db.Model):
    """Defines the User model for the database."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Message(db.Model):
    """Defines the Message model for the database."""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Like(db.Model):
    """Defines the Like model for the database."""
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.SmallInteger, default=0)  # -1 for downvote, 1 for upvote, 0 for neutral

class Constants(db.Model):
    """Defines the Constants model for the database."""
    __tablename__ = 'constants'

    id = db.Column(db.Integer, primary_key=True)
    reload = db.Column(db.Boolean, default=False)


@app.route('/signup', methods=['POST'])
def signup():
    """API endpoint for user registration."""
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:  # If a user exists with that email
        return jsonify({"message": "Email already registered!"}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(name=name, email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User signed up!"})


@app.route('/login', methods=['POST'])
def login():
    """API endpoint for user authentication."""
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password!"}), 401

    # Advanced: later, consider adding jwt tokens?
    return jsonify({"message": "Success"})


@app.route('/upvote_message', methods=['POST'])
def upvote_message():
    """API endpoint to upvote a message."""
    data = request.json
    user_id = data['user_id']
    message_id = data['message_id']

    existing_like = Like.query.filter_by(user_id=user_id, message_id=message_id).first()
    if not existing_like:
        new_like = Like(user_id=user_id, message_id=message_id, value=1)
        db.session.add(new_like)
    else:
        if existing_like.value == 0:
            existing_like.value = 1
        else:
            existing_like.value = 0

    db.session.commit()
    return jsonify({"message": "Message upvoted!"})


@app.route('/downvote_message', methods=['POST'])
def downvote_message():
    """API endpoint to downvote a message."""
    data = request.json
    user_id = data['user_id']
    message_id = data['message_id']

    existing_like = Like.query.filter_by(user_id=user_id, message_id=message_id).first()
    if not existing_like:
        new_like = Like(user_id=user_id, message_id=message_id, value=-1)
        db.session.add(new_like)
    else:
        if existing_like.value == 0:
            existing_like.value = -1
        else:
            existing_like.value = 0

    db.session.commit()
    return jsonify({"message": "Message downvoted!"})



@app.route('/get-username', methods=['POST'])
def get_username():
    """API endpoint to fetch a user's name based on their email."""
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required!"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404
    return jsonify({"name": user.name, "id": user.id})




@app.route('/get_users', methods=['GET'])
def get_users():
    """API endpoint to get a list of users, excluding the current user."""
    current_user_email = request.args.get('current_user_email')
    users = User.query.filter(User.email != current_user_email).all()
    
    return jsonify([{"id": user.id, "name": user.name} for user in users])



@app.route('/save_message', methods=['POST'])
def save_message():
    """API endpoint to save a new message."""
    try:
        data = request.json
        new_message = Message(
            content=data['content'],
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"status": "success", "message": "Message saved successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/get_messages', methods=['GET'])
def get_messages():
    """API endpoint to fetch messages between two users."""
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    
    if not sender_id or not receiver_id:
        return jsonify({"error": "Both sender_id and receiver_id are required!"}), 400

    # Fetching messages between the two users
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == sender_id, Message.receiver_id == receiver_id),
            db.and_(Message.receiver_id == sender_id, Message.sender_id == receiver_id)
        )
    ).order_by(Message.timestamp).all()

    # Format the messages for JSON serialization
    formatted_messages = [{
        "id": msg.id,
        "content": msg.content,
        "timestamp": msg.timestamp.isoformat(),
        "sender_id": msg.sender_id,
        "receiver_id": msg.receiver_id
    } for msg in messages]

    return jsonify(formatted_messages)


@app.route('/get_reload', methods=['GET'])
def get_reload():
    """API endpoint to fetch the reload state from the Constants table."""
    constant_row = Constants.query.first()
    if not constant_row:
        return jsonify({"error": "No row found in Constants table."}), 400
    return jsonify({"reload": constant_row.reload})


@app.route('/flip_reload', methods=['POST'])
def flip_reload():
    """API endpoint to toggle the reload state in the Constants table."""
    constant_row = Constants.query.first()
    if not constant_row:
        return jsonify({"error": "No row found in Constants table."}), 400

    constant_row.reload = not constant_row.reload
    db.session.commit()
    return jsonify({"message": "Reload state flipped successfully.", "new_state": constant_row.reload})


@app.route('/get_likes', methods=['GET'])
def get_likes():
    """API endpoint to fetch the likes of a specific message."""
    message_id = request.args.get('message_id')
    
    if not message_id:
        return jsonify({"error": "message_id is required!"}), 400

    # Fetching likes for the given message
    likes = Like.query.filter_by(message_id=message_id).all()
    # Calculate the total like value for the message
    like_value = sum([like.value for like in likes])

    return jsonify({"message_id": message_id, "like_value": like_value})



if __name__ == "__main__":
    app.run(debug=True)
