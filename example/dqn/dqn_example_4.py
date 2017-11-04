# -*- coding: utf-8 -*-
import numpy as np
from collections import deque


from keras.models import Sequential
from keras.layers import Input, Dense, Flatten, Conv2D, K, LSTM, PReLU
from keras.optimizers import Adam, RMSprop


class DQN:
    def __init__(self, state_size, action_size, memory_size=1000, batch_size=32, train_epochs=8):

        self.state_size = state_size[1:]
        self.action_size = action_size
        self.memory = deque(maxlen=memory_size)
        self.gamma = 0.99    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.00001
        self.model = self._build_model()
        self.cumulative_loss = 0
        self.train_steps = 0
        self.batch_size = batch_size
        self.train_epochs = train_epochs

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

    def _build_model(self):
        model = Sequential()

        model.add(Conv2D(64, (1, 1), strides=(1, 1), activation="relu", input_shape=self.state_size))
        model.add(Conv2D(64, (1, 1), strides=(1, 1), activation="relu"))
        model.add(Conv2D(64, (1, 1), strides=(1, 1), activation="relu"))
        model.add(Flatten())
        model.add(Dense(512, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self):

        inputs = np.zeros(((self.batch_size, ) + self.state_size))
        targets = np.zeros((self.batch_size, self.action_size))

        for i, j in enumerate(np.random.choice(len(self.memory), self.batch_size, replace=False)):
            state, action, reward, next_state, terminal = self.memory[i]

            target = reward

            if not terminal:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            targets[i] = self.model.predict(state)
            targets[i, action] = target
            inputs[i] = state

        history = self.model.fit(inputs, targets, epochs=self.train_epochs, verbose=0)

        self.cumulative_loss += history.history["loss"][0]
        self.train_steps += 1

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
