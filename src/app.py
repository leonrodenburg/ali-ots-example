from flask import Flask, abort, jsonify, request
from tablestore import OTSClient, Row
import json

app = Flask(__name__)

@app.route("/profile/<user_id>", methods=["GET"])
def fetch_profile(user_id):
  key = [('userId', user_id)]

  client = _ots_client()
  consumed, row, next_token = client.get_row("Profile", key)
  if row is not None:
    return jsonify(_to_dict(row))
  else:
    abort(404)

@app.route("/profile/<user_id>", methods=["POST"])
def save_profile(user_id):
  profile = request.json
  key = [("userId", user_id)]
  attribute_columns = [(key, val) for key, val in profile.items() if key != "userId"]
  row = Row(key, attribute_columns)

  client = _ots_client()
  client.put_row("Profile", row)
  return jsonify(_to_dict(row))

@app.errorhandler(404)
def entity_not_found(error):
  return jsonify({"message": "Not Found"}), 404

def _to_dict(row):
  result = {}

  for pk in row.primary_key:
    result[pk[0]] = pk[1]

  for att in row.attribute_columns:
    result[att[0]] = att[1]

  return result


def _ots_client():
  return OTSClient()
