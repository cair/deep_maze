import random
import glob
import os
import numpy as np
#from py_image_stitcher import ImageStitch
from tensorflow.python.keras import Input

from tensorflow.python.keras.layers import Conv2D, Flatten, Dense, concatenate, Reshape, UpSampling2D
from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.optimizers import Adam

from example.dcgan_example.memory import ReplayMemory
from example.dcgan_example.util import config_class


class Dream:

    def __init__(self, config, memory, model=None, path="./"):
        self.config = config
        self.memory = memory
        self.model = self.build_model() if model is None else model
        self.path = path
        os.makedirs(os.path.join(self.path, "models"), exist_ok=True)

    def save_model(self, suffix=""):
        self.model.save_weights(os.path.join(self.path, "models", "model%s.h5" % suffix))

    def load_model(self, model_file=None):
        if model_file is None:
            list_of_files = glob.glob(os.path.join(self.path, "models", "*.h5"))
            model_file = max(list_of_files, key=os.path.getctime)
        print(model_file)
        self.model.load_weights(model_file)

    @staticmethod
    def create_default(path="./"):
        config = config_class(
            history_length=1,
            batch_size=16,
            screen_width=84,
            screen_height=84,
            screen_dim=3,
            action_size=4,
            cnn_format="N/A",
            memory_size=1000
        )

        memory = ReplayMemory(config)
        dream = Dream(config, memory, None, path)
        return dream

    def train(self):
        # self.prestates, actions, rewards, self.poststates, terminals

        samples = self.memory.sample()
        prestates = samples[0]
        actions = samples[1]
        actions = [[1 if y == x else 0 for y in range(0, 4)] for x in actions]

        rewards = samples[2]
        poststates = samples[3]
        terminals = samples[4]

        self.model.fit(
            [np.array(actions), np.array(prestates)],
            [np.array(poststates)],
            epochs=1
        )

    def act(self, s0, a):
        one_hot_a = np.array([1 if y == a else 0 for y in range(0, 4)])
        s1 = self.model.predict_on_batch([np.array([one_hot_a]), np.array([s0])])
        return s1[0]


    def test(self):
        samples = self.memory.sample()
        prestates = samples[0]
        actions = samples[1]
        actions = [[1 if y == x else 0 for y in range(0, 4)] for x in actions]
        rewards = samples[2]
        poststates = samples[3]
        terminals = samples[4]

        """n = int(((8*2) / 2))
        X = [actions, prestates]
        X_pred = self.model.predict_on_batch(X)


        real = X[1]
        fake = X_pred[:n]
        """

        """stitch = ImageStitch((84, 84), rows=8, columns=2)

        real_fake = []
        for j in range(int(len(real) / 2)):
            the_real = real[j] * 255
            the_fake = fake[j] * 255
            stitch.add(the_real.astype('uint8'))
            stitch.add(the_fake.astype('uint8'))

        stitch.save("./results.png")
        """




    def build_model(self):
        state_size = (self.config.screen_width, self.config.screen_height, self.config.screen_dim)
        action_size = self.config.action_size


        action = Input(shape=(action_size, ), name="action")
        image = Input(shape=state_size, name="image")

        img_conv = Sequential()
        img_conv.add(Conv2D(256, (4, 4), strides=(2, 2), activation="relu", input_shape=state_size))
        img_conv.add(Conv2D(128, (3, 3), strides=(2, 2), activation="relu"))
        img_conv.add(Conv2D(64, (1, 1), strides=(2, 2), activation="relu"))
        img_conv.add(Flatten())
        img_conv.add(Dense(64, activation="relu"))
        img_conv.add(Dense(64, activation="relu"))

        action_s = Sequential()
        action_s.add(Dense(64, activation="relu", input_shape=(action_size, )))
        action_s.add(Dense(64, activation="relu"))

        stream_1 = img_conv(image)
        stream_2 = action_s(action)

        x = concatenate([stream_1, stream_2])
        x = Dense(128 * 21 * 21, activation="relu")(x)
        x = Reshape((21, 21, 128))(x)
        #x = BatchNormalization(momentum=0.8)(x)

        x = UpSampling2D()(x)
        x = Conv2D(128, (3, 3), padding="same", activation="relu")(x)
        #x = BatchNormalization(momentum=0.8)(x)

        x = UpSampling2D()(x)
        x = Conv2D(64, (3, 3), padding="same", activation="relu")(x)
        #x = BatchNormalization(momentum=0.8)(x)

        x = Conv2D(self.config.screen_dim, (3, 3), padding='same', activation="relu")(x)

        model = Model(inputs=[action, image], outputs=[x])
        model.compile(
            optimizer=Adam(0.00001),
            loss=['mse'],
            metrics=['accuracy']
        )
        #model.summary()

        return model
