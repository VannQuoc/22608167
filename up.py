import subprocess
import threading

def run_main():
    subprocess.run(["python", "main.py"])
def run_prx():
    subprocess.run(["python", "prx.py"])


if __name__ == "__main__":
  if __name__ == "__main__":
    prx_thread = threading.Thread(target=run_prx)
    main_thread = threading.Thread(target=run_main)

    prx_thread.start()
    main_thread.start()