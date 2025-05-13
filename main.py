import multiprocessing
import subprocess

def run_prediction_api():
    subprocess.run(["python", "backend/assessment.py"])

def run_exploration_api():
    subprocess.run(["python", "backend/introduction.py"])

if __name__ == "__main__":
    api1 = multiprocessing.Process(target=run_prediction_api)
    api2 = multiprocessing.Process(target=run_exploration_api)

    api1.start()
    api2.start()

    api1.join()
    api2.join()
