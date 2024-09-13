import time
import csv
import matplotlib.pyplot as plt
import numpy as np

class Profiller:
    _instance = None

    def __init__(self) -> None:
        self.verbose = True
        
        self.total_times = {"Profiller": 0.0}
        self.last_time_calls = {}
        self.start_time = time.time_ns()
    

    def _start_self(self) -> None:
        self.last_time_calls["Profiller"] = time.time_ns()
    

    def _stop_self(self) -> None:
        self.total_times["Profiller"] += (time.time_ns() - self.last_time_calls["Profiller"]) / 1000000000.0


    def _update_total_time(self) -> None:
        self.total_times["Total time"] = (time.time_ns() - self.start_time) / 1000000000.0


    def start(self, context: str) -> None:
        self.last_time_calls[context] = time.time_ns()
    

    def stop(self, context: str) -> None:
        if not context in self.last_time_calls:
            if self.verbose:
                print(f"Profiller: Called stop() on context {context} without calling start() first")
            return

        if not context in self.total_times:
            self.total_times[context] = 0
        
        self.total_times[context] += (time.time_ns() - self.last_time_calls[context]) / 1000000000.0


    def save_csv(self, path: str):
        self._start_self()
        self._update_total_time()

        with open(path + ".csv", "w", newline="") as f:
            w = csv.DictWriter(f, self.total_times.keys())
            w.writeheader()
            w.writerow(self.total_times)
        
        self._stop_self()
    

    def plot(self, path: str):
        self._start_self()
        self._update_total_time()

        percentages = {}
        time_remaining = 100
        for context in self.total_times:
            if context != "Total time":
                percentages[context] = self.total_times[context] / self.total_times["Total time"] * 100
                time_remaining -= percentages[context]
        if time_remaining > 0:
            percentages["Untracked time"] = time_remaining

        width = 0.5
        species = ("Program")
        fig, ax = plt.subplots()
        bottom = np.zeros(3)
        for boolean, percentage in percentages.items():
            p = ax.bar(species, percentage, width, label=boolean, bottom=bottom)
            bottom += percentage
        
        ax.set_title("Profile")
        ax.legend(loc="upper right")
        plt.ylabel("Relative time spent (%)")

        plt.savefig(path + str(".png"))

        self._stop_self()


profiller = Profiller()