import glob
import random
import shutil
import base64
import gym
from PIL import Image
from io import BytesIO

from skimage.color import rgb2gray

import gym_maze
import numpy as np
from flask import Flask, request, send_from_directory, jsonify
import os

from example.dcgan_example.explore.dream import Dream

dir_path = os.path.dirname(os.path.realpath(__file__))

class DataFrame:

    def __init__(self, status=None, data=None, message=None):
        self.status = status
        self.data = data
        self.message = message
    def json(self):
        return jsonify({
            "status": self.status,
            "data": self.data,
            "message": self.message
        })

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/experiments', methods=["GET"])
def experiments():

    data = []
    datastore_path = os.path.join(dir_path, "datastore")
    for experiment_path in [x for x in glob.glob(os.path.join(datastore_path, "*")) if os.path.isdir(x)]:
        alias = os.path.basename(experiment_path)
        alias_split = alias.split("__")
        width = int(alias_split[1])
        height = int(alias_split[2])
        models_path = os.path.join(experiment_path, "models")
        models = [{
            "path": x,
            "filename": os.path.basename(x)
        } for x in glob.glob(os.path.join(models_path, "*.h5"))]

        data.append({
            "alias":alias,
            "width": width,
            "height": height,
            "models": models
        })



    return DataFrame(status=True, data=data, message="Sent without errors").json()

@app.route('/test_experiment', methods=["POST"])
def test_experiment():
    data = request.get_json()
    experiment_path = os.path.join(dir_path, "datastore", data["id"])
    current_state_path = os.path.join(experiment_path, "current_state.npy")
    model_path = data["model"]["path"]

    current_state = np.load(current_state_path)

    return DataFrame(status=True, data={"base64": img2base64(current_state)}, message="Sent without errors").json()


    #dream = Dream.create_default(path=experiment_path)
    #dream.load_model(model_file=model_path)

def img2base64(pnyimg):
    img = Image.fromarray(np.uint8(pnyimg[:, ::-1]))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue())


@app.route('/do_action', methods=["POST"])
def do_action():
    data = request.get_json()
    experiment_path = os.path.join(dir_path, "datastore", data["alias"])
    previous_state_path = os.path.join(experiment_path, "previous_state.npy")
    current_state_path = os.path.join(experiment_path, "current_state.npy")
    model_filename = data["model"]["path"]
    action = int(data["action"])
    current_state = np.load(current_state_path)

    # Dream
    dream = Dream.create_default(path=experiment_path)
    dream.load_model(model_filename)
    new_state = dream.act(current_state, action)

    # Save new current state and previous state
    np.save(current_state_path, new_state)
    np.save(previous_state_path, current_state)

    # Send current state back to user
    current_state = np.load(current_state_path)

    return DataFrame(status=True, data={"base64": img2base64(new_state)}, message="Sent without errors").json()

@app.route('/train_experiment', methods=["POST"])
def train_experiment():
    data = request.get_json()
    alias = data["id"]
    alias_split = alias.split("__")
    width = int(alias_split[1])
    height = int(alias_split[2])

    experiment_path = os.path.join(dir_path, "datastore", alias)
    model_filename = data["model"]["path"]

    dream = Dream.create_default()
    dream.load_model(model_file=model_filename)

    env = gym.make("NoMaze-Img-%sx%s-v0" % (width, height))
    env.reset()
    for step in range(0, 1000):
        a = random.randint(0, 3)
        s1, r, terminal, info = env.step(a)
        env.render()
        print(s1.shape)

        # Add sample to replay buffer
        dream.memory.add(s1, r, a, terminal)

        if step > 50:
            dream.train()

        if step % 100 == 0 and step > 50:
            print("Save!")
            dream.save_model()


@app.route('/delete_experiment', methods=["POST"])
def delete_experiment():
    data = request.get_json()

    the_path = os.path.join(dir_path, "datastore", data["id"])
    shutil.rmtree(the_path)
    return DataFrame(status=True, data=the_path, message="Sent without errors").json()


@app.route('/create_experiment', methods=["POST"])
def create_experiment():
    data = request.get_json()

    alias = data["alias"]
    width = data["width"]
    height = data["height"]

    object_name = "%s__%s__%s" % (alias, width, height)
    object_path = os.path.join(dir_path, "datastore", object_name)
    initial_state_path = os.path.join(object_path, "start_state.npy")
    current_state_path = os.path.join(object_path, "current_state.npy")

    try:
        os.makedirs(object_path, exist_ok=False)

        # Create a Dream instance
        dream = Dream.create_default(path=object_path)
        dream.save_model()

        # Create env and get initial state
        env = gym.make("NoMaze-Img-%sx%s-v0" % (width, height))
        initial_state = env.reset()
        env.close()
        np.save(initial_state_path, initial_state)
        np.save(current_state_path, initial_state)

        return DataFrame(status=True, data=data, message="Created Experiment").json(), 200
    except Exception as e:
        print(e)
        return DataFrame(status=False, data=None, message="Failed to create experiment directory").json(), 400




if __name__ == "__main__":
    os.makedirs(os.path.join(dir_path, "datastore"), exist_ok=True)

    app.run(debug=True)

