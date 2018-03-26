import random

import os
from py_image_stitcher import ImageStitch
from tensorflow.python.keras import Input

from tensorflow.python.keras.layers import Conv2D, Flatten, Dense, concatenate, Reshape, UpSampling2D
from tensorflow.python.keras.models import Sequential, Model
from tensorflow.python.keras.optimizers import Adam


class Dream:

    def __init__(self, config, memory):
        self.config = config
        self.memory = memory
        self.model = self.build_model()

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
            [actions, prestates],
            [poststates],
            epochs=1
        )

    def test(self):
        samples = self.memory.sample()
        prestates = samples[0]
        actions = samples[1]
        actions = [[1 if y == x else 0 for y in range(0, 4)] for x in actions]
        rewards = samples[2]
        poststates = samples[3]
        terminals = samples[4]

        n = int(((8*2) / 2))
        X = [actions, prestates]
        X_pred = self.model.predict_on_batch(X)


        real = X[1]
        fake = X_pred[:n]

        stitch = ImageStitch((84, 84), rows=8, columns=2)

        real_fake = []
        for j in range(int(len(real) / 2)):
            the_real = real[j] * 255
            the_fake = fake[j] * 255
            stitch.add(the_real.astype('uint8'))
            stitch.add(the_fake.astype('uint8'))

        stitch.save("./results.png")




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
        model.summary()

        return model
