import json
import uuid
from datetime import datetime

import storage

import markdown
from flask import Flask, url_for, request
app = Flask(__name__)

@app.route("/")
def main():
  with open("static/index.html") as f:
    return f.read()

# apis
@app.route("/api/find")
def find():
  return ""

@app.route("/api/def/<word>/add/<pos>/", methods=["POST", "PUT"])
@app.route("/api/def/<word>/add/", methods=["POST", "PUT"])
def add_def(word, pos=None):
  data = storage.get_def(word)
  if not data:
    data = []
  d = json.loads(request.data)
  if not d or "def" not in d:
    return json.dumps({"status": "error", "message":"Incorrect or no Data sent"})
  def_data = {
    "id": str(uuid.uuid4()),
    "def": d["def"].strip(),
    "html": markdown.markdown(d["def"]),
    "last_touch": datetime.now().isoformat()
    }
  if pos is None:
    data.append(def_data)
  else:
    def_data["id"] = pos
    found = False
    for d, i in zip(data, range(len(data))):
      if d["id"] == pos:
        data[i] = def_data
        found = True
        break
    if not found:
      return json.dumps({"status": "error", "message": "the def id was wrong" })

  storage.set_def(word, data)
  return json.dumps({"status": "worked"})

@app.route("/api/def/<word>/add/<pos>/del", methods=["POST", "PUT"])
def del_def(word, pos):
  data = storage.get_def(word)
  if not data:
    return json.dumps({"status": "error", "message":"word is already deleted"})
  for i in range(len(data)):
    d = data[i]
    if d["id"] == pos:
      del data[i]
      break

  storage.set_def(word, data)
  return json.dumps({"status": "worked"})


@app.route("/api/def/<word>/<pos>")
def single_word_def(word, pos):
  data = storage.get_def(word)
  if not data:
    return json.dumps({"status": "error"})
  result = None
  for d in data:
    if d["id"] == pos:
      result = d
      break
  if not result:
    return json.dumps({"status": "error"})
  return json.dumps({
    "status": "worked",
    "word": word,
    "def": result
  });
@app.route("/api/def/<word>/")
def single_word(word):
  data = storage.get_def(word)
  if not data:
    return json.dumps({"status": "error"})
  return json.dumps({
    "status": "worked",
    "word": word,
    "defs": data
  });

@app.route("/api/all_defs")
@app.route("/api/all_defs/")
def all_words():
  return json.dumps(storage.get_all_def())

if __name__ == "__main__":
  app.run(debug=True)
  url_for("static", filename='index.html')
  url_for("static", filename='js/jquery.min.js')
  url_for("static", filename='js/shodow.js')
  url_for("static", filename='js/bootstrap.min.js')
  url_for("static", filename='js/ICanHaz.min.js')
  url_for("static", filename='css/bootstrap.css')
