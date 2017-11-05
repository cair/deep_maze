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
    phase = fig.add_subplot(222)
    steps = fig.add_subplot(223)
    epsilon = fig.add_subplot(224)

    fig.tight_layout()

    loss.set_title("Training Loss")
    phase.set_title("Phase")
    steps.set_title("Steps")
    epsilon.set_title("Epsilon")

    data_loss = []
    data_epsilon = []
    data_steps = []
    data_phase = []

    for item in log_file.data:
        data_loss.append(item["loss"])
        data_steps.append([min(item["optimal"] * 2, item["steps"]), item["optimal"]])
        data_epsilon.append(item["epsilon"])
        data_phase.append(1 if item["phase"] == "exploit" else 0)

    loss.plot(data_loss)
    phase.plot(data_phase)
    steps.plot(data_steps)
    epsilon.plot(data_epsilon)

    fig.savefig("plots/%s.png" % log_file.path)












