from collections import namedtuple

config_class = namedtuple("Config",
                          [
                              "history_length",
                              "memory_size",
                              "batch_size",
                              "screen_width",
                              "screen_height",
                              "cnn_format",
                              "action_size",
                              "screen_dim"
                          ])