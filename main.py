import multiprocessing
import subprocess
import time

def run_api():
    subprocess.run(["python", "backend/api.py"])

def run_ui():
    time.sleep(2)  # ensure API starts first
    subprocess.run(["streamlit", "run", "frontend/ui.py"])

if __name__ == "__main__":
    api_process = multiprocessing.Process(target=run_api)
    ui_process = multiprocessing.Process(target=run_ui)

    api_process.start()
    ui_process.start()

    api_process.join()
    ui_process.join()