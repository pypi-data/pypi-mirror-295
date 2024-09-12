import time
import csv
import matplotlib.pyplot as plt

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
        self._start_self()
        self.last_time_calls[context] = time.time_ns()
        self._stop_self()
    

    def stop(self, context: str) -> None:
        self._start_self()
        if not context in self.last_time_calls:
            if self.verbose:
                print(f"Profiller: Called stop() on context {context} without calling start() first")
            self._stop_self()
            return

        if not context in self.total_times:
            self.total_times[context] = 0
        
        self.total_times[context] += (time.time_ns() - self.last_time_calls[context]) / 1000000000.0
        self._stop_self()


    def save_csv(self, path: str):
        self._start_self()
        self._update_total_time()

        with open(path + ".csv", "w", newline="") as f:
            w = csv.DictWriter(f, self.total_times.keys())
            w.writeheader()
            w.writerow(self.total_times)
        
        self._stop_self()
    

    def plot(self, path: str, excludes: list=[]):
        self._start_self()
        self._update_total_time()

        for context in excludes:
            self.total_times["Total time"] -= self.total_times[context]

        percentages = {}
        for context in self.total_times:
            if context != "Total time" and not context in excludes:
                percentages[context] = self.total_times[context] / self.total_times["Total time"] * 100

        fig = plt.figure()
        plt.bar(percentages.keys(), percentages.values())
        plt.xlabel("Contexts")
        plt.ylabel("Relative time spent (%)")
        plt.title("Profile")
        plt.savefig(path + str(".png"))

        self._stop_self()


profiller = Profiller()