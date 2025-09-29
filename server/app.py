from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():

    if request.method == 'GET':

        messages = Message.query.order_by(asc(Message.created_at)).all()
        messages_list = [message.to_dict() for message in messages]

        response = make_response(jsonify(messages_list), 200)

        return response

    elif request.method == 'POST':
        data = request.get_json()

        body =data.get("body")
        username = data.get("username")

        if not body or not username:
            response = make_response(jsonify({"Error":"Body and username required"}), 400)
            return response

        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()

        response = make_response(jsonify(new_message.to_dict()), 201)
        return response

@app.route('/messages/<int:id>', methods = ['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        data = request.get_json()
        body = data.get("body")

        if not body:
            response = make_response(jsonify({"Error":"Body is required"}), 400)
            return response

        message.body = body
        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 200)
        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = make_response(jsonify({"Success":"Message Successfuly deleted"}), 200)
        return response


if __name__ == '__main__':
    app.run(port=5555, debug= True)