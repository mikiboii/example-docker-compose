from flask import Flask, render_template
import threading

import requests

import os
import subprocess
import time
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

        # Live stream URL
url = "https://pull-f5-tt03.tiktokcdn.com/game/stream-3287551689678128005_sd.flv?expire=1745061710&sign=0f4efcf4a632867daa673569992d60da&_webnoredir=1"

        # Twitch RTMP URL
twitch_rtmp_url = "rtmp://live-lax.twitch.tv/app/live_1072101235_ztWGwxq7oMHGHkVmsrbqDIGvTV5DW2"

def miki():

    # while True:


        # Duration to stream in seconds
        stream_duration = 60  # Stream for 1 minute

        start_time = time.time()
        subprocess.run(["apt", "update"], check=True)

        
        # Update package lists heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
        #subprocess.run(["heroku", "buildpacks:add", "https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git"], check=True)

        # Install FFmpeg (with -y to avoid manual confirmation)
        #subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)

        try:
            # Use FFmpeg to stream the live stream to the Twitch RTMP URL
            subprocess.run([
                "ffmpeg",
                "-i", url,
                "-c", "copy",
                "-f", "flv",
                "-fflags", "nobuffer",
                "-flags", "low_delay",
                twitch_rtmp_url
            ], check=True)

        except subprocess.CalledProcessError as e:
            print(f"Error streaming live stream: {e}")

        except KeyboardInterrupt:
            print("Stream interrupted by user")



def miki_tester():

    while True:
         
        time.sleep(30)
        try:
            response = requests.get('https://flask-ap18.onrender.com/')
            print(f"Response status code from miki_test: {response.status_code}")
           
        except requests.exceptions.RequestException as e:
                print(f"Error: {e}")




#t1 = threading.Thread(target=miki)
#t1.start()

#t2 = threading.Thread(target=miki_tester)
#t2.start()
# print("server starting...")

# print(os.system("ls"))

# print(os.system("ffmpeg"))

# https://flask-ap18.onrender.com/

@app.route('/')
def index():
    # return "cc"
    return "miki streaming app new #2"

@app.route('/bart')
def use_jinja():
    return "miki streaming app page 2"



if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve(port=5000)
    print("server starting...")
    app.run(host="0.0.0.0", port=5000)
