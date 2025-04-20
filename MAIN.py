import multiprocessing
import subprocess
import time

def run_api():
    subprocess.run(["python", "projectAPI.py"])

def run_ui():
    # Wait a bit to make sure the API is ready before UI tries to connect
    time.sleep(2)
    subprocess.run(["streamlit", "run", "projectUI.py"])

if __name__ == "__main__":
    # Create two processes
    api_process = multiprocessing.Process(target=run_api)
    ui_process = multiprocessing.Process(target=run_ui)

    # Start both
    api_process.start()
    ui_process.start()

    # Wait for both to finish (optional)
    api_process.join()
    ui_process.join()
