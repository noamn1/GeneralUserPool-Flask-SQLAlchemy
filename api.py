import io
import os

from flask import Flask, request, json, send_file

from db.AlchemyEncoder import AlchemyEncoder
from db.dataLayer import DataLayer
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import Flask
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
data_layer = DataLayer()


@app.route("/user")
def get_user_by_email():
    user_data = request.json
    user = data_layer.get_user_by_email(user_data["email"])
    user_json = user.__repr__()
    return app.response_class(response=user_json, status=200,
                              mimetype="application/json")


@app.route("/users")
def get_users():
    us = []
    users = data_layer.get_all_users()
    for user in users:
        us.append(user.to_json())

    return app.response_class(response=json.dumps(us), status=200,
                              mimetype="application/json")


@app.route("/user/<string:pid>/image")
def get_image(pid):

    dir_name = os.path.join('images', 'users', pid)
    for file in os.listdir(dir_name):
        file_name = os.path.join('images', 'users', pid, file)
        with open(file_name, "rb") as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename=pid + '.png',
                mimetype='image/png'
            )

    return None


if __name__ == "__main__":
    app.run(host='0.0.0.0')
