from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import subprocess 
import json

app = Flask("image_recognition")
api = Api(app)

class imageRecognition(Resource):
    def post(self):

        posted_data = request.get_json()

        url = posted_data["image_url"]

        r = requests.get(url)

        retJson = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as f:
                retJson = json.load(f)

        return retJson

api.add_resource(imageRecognition, "/image")

if __name__ == "__main__":
    app.run(host="0.0.0.0")