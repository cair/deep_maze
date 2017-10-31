# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, K, LSTM
from keras.optimizers import Adam, RMSprop
from keras.utils import plot_model

class DQN:
    def __init__(self, state_size, action_size):

        self.state_size = state_size[1:]
        self.action_size = action_size
        self.memory = deque(maxlen=200000)
        self.gamma = 0.99    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.00001
        self.model = self._build_model()
        self.cumulative_loss = 0
        self.train_steps = 0

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
        # Neural Net for Deep-Q learning Model
        model = Sequential()

        #model.add(Flatten(input_shape=self.state_size))
        #model.add(Dense(64, activation='relu'))
        #model.add(Dense(64, activation='relu'))
        #model.add(Dense(64, activation='relu'))
        #model.add(Dense(self.action_size, activation='linear'))

        #model.add(Conv2D(32, (8, 8), strides=(4, 4), activation="relu", input_shape=self.state_size, data_format="channels_last"))
        #model.add(Conv2D(64, (4, 4), strides=(2, 2), activation="relu",))
        #model.add(Conv2D(64, (3, 3), strides=(1, 1), activation="relu",))

        print(self.state_size)

        model.add(Conv2D(64, (4, 4), padding="same", strides=(4, 4), activation="relu", input_shape=self.state_size, data_format="channels_last"))
        model.add(Conv2D(64, (3, 3), padding="same", strides=(4, 4), activation="relu",))
        model.add(Conv2D(64, (2, 2), padding="same", strides=(4, 4), activation="relu",))
        model.add(Flatten())
        model.add(Dense(512,  activation="relu"))
        model.add(Dense(self.action_size, activation='linear'))

        # DQN.huber_loss
        model.compile(loss=DQN.huber_loss, optimizer=Adam(lr=self.learning_rate))
        plot_model(model, to_file='model.png', show_shapes=True)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):

        rnd = np.random.choice(len(self.memory), size=batch_size)
        mini_batch = [self.memory[idx] for idx in rnd]
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            history = self.model.fit(state, target_f, epochs=1, verbose=0)

            self.cumulative_loss += history.history["loss"][0]
            self.train_steps += 1

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
