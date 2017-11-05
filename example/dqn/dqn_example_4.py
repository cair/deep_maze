# -*- coding: utf-8 -*-
from threading import Thread

import numpy as np
from collections import deque

import time
import tensorflow as tf
from keras import Input
from keras.engine import Model
from keras.layers import Conv2D, K, Flatten, Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import plot_model
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

from example.dqn.capsulelayers import PrimaryCap, CapsuleLayer, Length
"""
class Trainer(Process):

    def __init__(self):
        super().__init__()

    def train(self, model):
        inputs = np.zeros(((self.agent.batch_size, ) + self.agent.state_size))
        targets = np.zeros((self.agent.batch_size, self.agent.action_size))

        for i, j in enumerate(np.random.choice(len(self.agent.memory), self.agent.batch_size, replace=False)):
            state, action, reward, next_state, terminal = self.agent.memory[j]

            target = reward

            if not terminal:
                target = reward + self.agent.gamma * np.amax(model.predict(next_state)[0])

            targets[i] = model.predict(state)
            targets[i, action] = target
            inputs[i] = state

            if self.agent.q_table is not None:

                player_pos = np.where(state == 2)

                if len(player_pos[0]) > 0:
                    x, y = player_pos[1][0], player_pos[2][0]

                    try:
                        self.agent.q_table[x, y] = np.argmax(targets[i]) + 1
                    except:
                        pass

        history = model.fit(inputs, targets, epochs=self.agent.train_epochs, verbose=0)

        self.agent.cumulative_loss += history.history["loss"][0]
        self.agent.train_steps += 1

    def update_weights(self):
        weights = self.model.get_weights()
        self.agent.weight_queue.append(weights)

    def run(self):
        with tf.get_default_graph().as_default():
            model = self.agent._build_model()

        while True:
            if len(self.agent.memory) > self.agent.batch_size:
                self.train(model)

                #if self.agent.train_steps % 10 == 0:
                #    self.update_weights()
"""


class DQN:
    def __init__(self,
                 state_size,
                 action_size,
                 memory_size=1000,
                 batch_size=32,
                 train_epochs=8,
                 e_min=0,
                 e_max=1.0,
                 e_steps=1000,
                 lr=0.00001,
                 discount=0.99
                 ):

        self.q_table = np.zeros(shape=(state_size[0], state_size[1]))
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=memory_size)
        self.gamma = discount    # discount rate
        self.epsilon = e_max  # exploration rate
        self.epsilon_min = e_min
        self.epsilon_max = e_max
        self.epsilon_decay = (e_max - e_min) / e_steps
        self.learning_rate = lr

        self.cumulative_loss = 0
        self.train_steps = 0
        self.batch_size = batch_size
        self.train_epochs = train_epochs
        self.model = self._build_model()

    def average_loss(self):
        return self.cumulative_loss / (self.train_steps + 0.0001)

    @staticmethod
    def huber_loss(y_true, y_pred, clip_value=1):
        # Huber loss, see https://en.wikipedia.org/wiki/Huber_loss and
        # https://medium.com/@karpathy/yes-you-should-understand-backprop-e2f06eab496b
        # for details.
        assert clip_value > 0.

        x = y_true - y_pred
        if np.isinf(clip_value):
            # Spacial case for infinity since Tensorflow does have problems
            # if we compare `K.abs(x) < np.inf`.
            return .5 * K.square(x)

        condition = K.abs(x) < clip_value
        squared_loss = .5 * K.square(x)
        linear_loss = clip_value * (K.abs(x) - .5 * clip_value)
        if K.backend() == 'tensorflow':
            import tensorflow as tf
            if hasattr(tf, 'select'):
                return tf.select(condition, squared_loss, linear_loss)  # condition, true, false
            else:
                return tf.where(condition, squared_loss, linear_loss)  # condition, true, false
        elif K.backend() == 'theano':
            from theano import tensor as T
            return T.switch(condition, squared_loss, linear_loss)
        else:
            raise RuntimeError('Unknown backend "{}".'.format(K.backend()))

    def _huber_loss(self, target, prediction):
        # sqrt(1+error^2)-1
        error = prediction - target
        return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

    def _build_model(self):
        """
        n_rounting = 3

        x = Input(shape=self.state_size)
        conv1 = Conv2D(filters=256, kernel_size=2, strides=1, padding='valid', activation='relu', name='conv1')(x)
        primarycaps = PrimaryCap(conv1, dim_vector=8, n_channels=32, kernel_size=9, strides=2, padding='valid')
        digitcaps = CapsuleLayer(num_capsule=self.action_size, dim_vector=16, num_routing=n_rounting, name='digitcaps')(primarycaps)
        out_caps = Length(name='out_caps')(digitcaps)

        model = Model(inputs=[x], outputs=[out_caps])
        model.compile(optimizer="adam", loss=self._huber_loss)
        """
        #"""
        model = Sequential()
        model.add(Conv2D(256, (1, 1), strides=(1, 1), activation="relu", input_shape=self.state_size))
        model.add(Conv2D(256, (1, 1), strides=(1, 1), activation="relu"))
        model.add(Conv2D(256, (1, 1), strides=(1, 1), activation="relu"))
        model.add(Flatten())
        model.add(Dense(1024, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(optimizer=Adam(lr=self.learning_rate), loss=self._huber_loss)
        #"""

        plot_model(model, to_file='model.png', show_layer_names=True, show_shapes=True)
        SVG(model_to_dot(model).create(prog='dot', format='svg'))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, force_exploit=True):
        self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_decay)

        if force_exploit:
            act_values = self.model.predict(state)
            return np.argmax(act_values[0])  # returns action

        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, self.action_size)

        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, q_table=None):
        inputs = np.zeros(((self.batch_size, ) + self.state_size))
        targets = np.zeros((self.batch_size, self.action_size))

        for i, j in enumerate(np.random.choice(len(self.memory), self.batch_size, replace=False)):
            state, action, reward, next_state, terminal = self.memory[j]

            target = reward

            if not terminal:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            targets[i] = self.model.predict(state)
            targets[i, action] = target
            inputs[i] = state

            if q_table is not None:

                player_pos = np.where(state == 2)

                if len(player_pos[0]) > 0:
                    x, y = player_pos[1][0], player_pos[2][0]

                    try:
                        q_table[x, y] = np.argmax(targets[i]) + 1
                    except:
                        pass

        history = self.model.fit(inputs, targets, epochs=self.train_epochs, verbose=0)

        self.cumulative_loss += history.history["loss"][0]
        self.train_steps += 1

        self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_decay)

    def replay_gen(self):

        while True:
            inputs = np.zeros(((self.batch_size, ) + self.state_size))
            targets = np.zeros((self.batch_size, self.action_size))

            if len(self.memory) < self.batch_size:
                yield inputs, targets
                time.sleep(5)
                continue

            for i, j in enumerate(np.random.choice(len(self.memory), self.batch_size, replace=False)):
                state, action, reward, next_state, terminal = self.memory[j]

                target = reward

                if not terminal:
                    target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

                targets[i] = self.model.predict(state)
                targets[i, action] = target
                inputs[i] = state

            yield inputs, targets


    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
