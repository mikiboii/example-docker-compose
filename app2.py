from flask import Flask, render_template
import threading

import requests

import os
import subprocess
import time
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

        
url = "https://pull-f5-tt03.tiktokcdn.com/game/stream-3287574732312150917_uhd.flv?_session_id=053-2025040717132867A9607E97ABF21C98EB.1744046104554&_webnoredir=1&expire=1745255609&sign=c1ce004ad4972a900bfdfdb4d07f8711"

twitch_rtmp_url = "rtmp://live-lax.twitch.tv/app/live_1072101235_ztWGwxq7oMHGHkVmsrbqDIGvTV5DW2"

p_thread = None

stream_t1 = None

is_running = False

def miki():

        try:
            subprocess.run(["apt", "update"], check=True)

        
            # Update package lists heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
            #subprocess.run(["heroku", "buildpacks:add", "https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git"], check=True)

            # Install FFmpeg (with -y to avoid manual confirmation)
            subprocess.run(["apt", "install", "-y", "ffmpeg"], check=True)
            global p_thread
            global stream_t1
            global is_running

            if is_running == False:

                # p_thread = subprocess.Popen(["python", "test_thread2.py"])

                # p_thread = subprocess.Popen(["ffmpeg",
                #     "-i", url,
                #     "-c", "copy",
                #     "-f", "flv",
                #     "-fflags", "nobuffer",
                #     "-flags", "low_delay",
                #     twitch_rtmp_url])


                p_thread = subprocess.Popen(
                                    [
                                        "ffmpeg",
                                        "-i", url,
                                        "-c", "copy",
                                        "-f", "flv",
                                        "-fflags", "nobuffer",
                                        "-flags", "low_delay",
                                        "-loglevel", "error",  # Only show errors
                                        "-reconnect", "1",
                                        "-reconnect_at_eof", "1",
                                        "-reconnect_streamed", "1",
                                        "-reconnect_delay_max", "5",
                                        twitch_rtmp_url
                                    ],
                                    stderr=subprocess.PIPE,  # Capture stderr
                                    universal_newlines=True
                                )



                is_running = True

                

            

            print("streaming started")

            

            

        except subprocess.CalledProcessError as e:
            print(f"Error streaming live stream: {e}")

        except KeyboardInterrupt:
            print("Stream interrupted by user")

        # subprocess.Popen(["sudo", "apt" , "update"])

        # subprocess.Popen(["sudo", "apt" , "install", "ffmpeg", "-y"])

#         sudo apt update
# sudo apt install ffmpeg -y

def miki_tester():

    while True:
         
        time.sleep(300)

        if stream_t1 != None:
            if stream_t1.is_alive() == True:
                try:

                    response = requests.get('https://flask-zddy.onrender.com')
                    print(f"Response status code from miki_test: {response.status_code}")
                
                except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")



stream_t1 = threading.Thread(target=miki)
stream_t1.start()


# t2 = threading.Thread(target=miki_tester)
# t2.start()


def stream_restarter():

    while True:
         
        time.sleep(5)

        try:
        
            # p_thread.terminate()
            # p_thread.wait()
            # print("stoped thread")

            # global is_running
            # is_running = False


            global stream_t1
            global is_running

    

            if stream_t1 == None:

                try:
        
                    p_thread.terminate()
                    p_thread.wait()
                    

                    
                    is_running = False
                except:
                    pass

                stream_t1 = threading.Thread(target=miki)
                stream_t1.start()
                # return f"True"    
            else:
                if stream_t1.is_alive() == False:

                    try:
        
                        p_thread.terminate()
                        p_thread.wait()
                       

                        # global is_running
                        is_running = False
                    except:
                        pass

                    print("Stream stopped on its own ")
                    stream_t1 = threading.Thread(target=miki)

                    print("Now restarting...")
                    stream_t1.start()
        except:
            pass
       

# restarter_t1 = threading.Thread(target=stream_restarter)

# restarter_t1.start()





# https://flask-ap18.onrender.com/

@app.route('/')
def index():
    if stream_t1 == None:
        return render_template('app.html', is_streaming="False")

    else:        

        return render_template('app.html', is_streaming=stream_t1.is_alive())
    
    # return f"miki streaming app is {stream_t1.is_alive()}"

@app.route('/start')
def start_stream():

    global stream_t1

    

    if stream_t1 == None:

        stream_t1 = threading.Thread(target=miki)
        stream_t1.start()
        return f"True"    
    else:
        if stream_t1.is_alive() == False:
            # stream_t1 = threading.Thread(target=miki)
            stream_t1.start()
        return f"{stream_t1.is_alive()}"

@app.route('/stop')
def stop_stream():

    try:
        
        p_thread.terminate()
        p_thread.wait()
        print("stoped thread")

        global is_running
        is_running = False
    except:
        pass

    if stream_t1 != None:
        return f"{stream_t1.is_alive()}"

    else:
        return f"False"  

    



if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve(port=5000)
    print("server starting...")
    app.run(host="0.0.0.0", port=5000)
  
