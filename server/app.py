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
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.SmallInteger, default=0)  # -1 for downvote, 1 for upvote, 0 for neutral



@app.route('/signup', methods=['POST'])
def signup():
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
    data = request.json
    user_id = data['user_id']
    message_id = data['message_id']

    existing_like = Like.query.filter_by(user_id=user_id, message_id=message_id).first()
    if not existing_like:
        new_like = Like(user_id=user_id, message_id=message_id, value=1)
        db.session.add(new_like)
    else:
        existing_like.value = 1

    db.session.commit()
    return jsonify({"message": "Message upvoted!"})


@app.route('/downvote_message', methods=['POST'])
def downvote_message():
    data = request.json
    user_id = data['user_id']
    message_id = data['message_id']

    existing_like = Like.query.filter_by(user_id=user_id, message_id=message_id).first()
    if not existing_like:
        new_like = Like(user_id=user_id, message_id=message_id, value=-1)
        db.session.add(new_like)
    else:
        existing_like.value = -1

    db.session.commit()
    return jsonify({"message": "Message downvoted!"})


@app.route('/get-username', methods=['POST'])
def get_username():
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
    current_user_email = request.args.get('current_user_email')
    users = User.query.filter(User.email != current_user_email).all()
    
    return jsonify([{"id": user.id, "name": user.name} for user in users])



@app.route('/save_message', methods=['POST'])
def save_message():
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



if __name__ == "__main__":
    app.run(debug=True)
