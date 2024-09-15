from flask import Flask, render_template
import datetime
app = Flask(__name__)

start_time = datetime.datetime.now()

@app.route('/')
def index():
  return render_template('index.html')
@app.route('/main')
def run_main():
  try:
      process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      return "main.py executed successfully"
  except Exception as e:
      return f"An error occurred: {str(e)}"
@app.route('/time')
def get_running_time():
    current_time = datetime.datetime.now()
    running_time = current_time - start_time
    years = running_time.days // 365
    months = (running_time.days % 365) // 30
    days = (running_time.days % 365) % 30
    hours = running_time.seconds // 3600
    minutes = (running_time.seconds % 3600) // 60
    seconds = (running_time.seconds % 3600) % 60

    return f"Bot Đã Chạy: {years} năm {months} tháng {days} ngày {hours} giờ {minutes} phút {seconds} giây"


if __name__ == '__main__':
  app.run(host='0.0.0.0')
