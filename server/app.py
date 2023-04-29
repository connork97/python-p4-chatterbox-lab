from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all()
        all_json_messages_dict = []
        for message in all_messages:
            all_json_messages_dict.append(message.to_dict())
        
        response = make_response(jsonify(all_json_messages_dict), 200)

    elif request.method == 'POST':
        form_data = request.get_json()
        new_message = Message(
            body = form_data['body'],
            username = form_data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(jsonify(new_message.to_dict()), 200)

    return response


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        form_data = request.get_json()
        for attr in form_data:
            setattr(message, attr, form_data[attr])

        db.session.add(message)
        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 200,)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted..."
        }

        response = make_response(response_body, 200)

    return response

if __name__ == '__main__':
    app.run(port=5555)
