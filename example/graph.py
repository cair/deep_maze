import matplotlib.pyplot as plt
import os
import json
os.makedirs("plots", exist_ok=True)


class LogFile:

    def __init__(self, path):
        self.path = path
        self.data = []

    def load(self):
        with open(self.path, "r") as f:
            for line in f.readlines():
                self.data.append(json.loads(line))


log_files = []

for file in os.listdir("./"):
    if not os.path.isfile(file) or not file.endswith(".log"):
        continue
    log_files.append(LogFile("./%s" % file))

for log_file in log_files:
    log_file.load()

    fig = plt.figure()
    loss = fig.add_subplot(221)
    loss_rate = fig.add_subplot(222)
    steps = fig.add_subplot(223)
    epsilon = fig.add_subplot(224)

    fig.tight_layout()

    loss.set_title("Training Loss")
    loss_rate.set_title("Loss Rate (Victory/Loss)")
    steps.set_title("Steps")
    epsilon.set_title("Epsilon")

    data_loss = []
    data_loss_rate = []
    data_steps = []
    data_actions = []

    for item in log_file.data:
        data_loss.append(item["loss"])
        data_loss_rate.append(item["score"])
        data_steps.append(item["epoch"])
        data_actions.append(item["actions"])

    loss.plot(data_loss)
    loss_rate.plot(data_loss_rate)
    steps.plot(data_steps)
    epsilon.plot(data_actions)

    fig.savefig("plots/%s.png" % log_file.path)












