from flask import Flask, render_template
import threading

import requests

import os
import subprocess
import time
import shlex

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

        
url = "https://pull-f5-tt03.tiktokcdn.com/game/stream-3287574732312150917_uhd.flv?_session_id=053-2025040717132867A9607E97ABF21C98EB.1744046104554&_webnoredir=1&expire=1745255609&sign=c1ce004ad4972a900bfdfdb4d07f8711"

twitch_rtmp_url = "rtmp://live-lax.twitch.tv/app/live_1072101235_ztWGwxq7oMHGHkVmsrbqDIGvTV5DW2"

p_thread = None

stream_t1 = None

is_running = True

def miki():

        try:
            subprocess.run(["apt", "update"], check=True)

            # sudo apt-get install build-essential    # 
            # subprocess.run(["apt", "install", "build-essential"], check=True)    

        
            # Update package lists heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
            #subprocess.run(["heroku", "buildpacks:add", "https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git"], check=True)

            # Install FFmpeg (with -y to avoid manual confirmation)
            # subprocess.run(["apt", "install", "-y", "ffmpeg"], check=True)
            # subprocess.run(["apt", "install", "-y", "ffmpeg", "libavcodec-dev","libavformat-dev","libavutil-dev","libswscale-dev"], check=True)    

            # subprocess.run(["g++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) class_demo.cpp -o mymodule$(python3-config --extension-suffix) -lavformat -lavcodec -lavutil"], check=True)

            py_includes = subprocess.getoutput("python3 -m pybind11 --includes")
            extension_suffix = subprocess.getoutput("python3-config --extension-suffix")
                
            # Build command as list
            compile_cmd = [
                    "g++",
                    "-O3", "-Wall", "-shared", "-std=c++11", "-fPIC",
                    *shlex.split(py_includes),  # Split includes into separate arguments
                    "class_demo.cpp",
                    "-o", f"mymodule{extension_suffix}",
                    "-lavformat", "-lavcodec", "-lavutil"
                ]
                
            try:
                    subprocess.run(compile_cmd, check=True)
            except subprocess.CalledProcessError as e:
                    print(f"Compilation failed with exit code {e.returncode}")
            except FileNotFoundError:
                    print("g++ compiler not found. Install with: sudo apt-get install build-essential")    
                
                
            from mymodule import Stream_demo

                
            global p_thread
            global stream_t1
            global is_running
            
            input_url = "https://pull-f5-tt03.tiktokcdn.com/game/stream-3287621823810241413_uhd.flv?_session_id=053-20250416205527E95B5C7A732B3437FDBA.1744808133923&_webnoredir=1&expire=1746017727&sign=55d1bbc1ab6c45779cd90b883d7bc036"
            output_url = "rtmp://live-lax.twitch.tv/app/live_1072101235_ztWGwxq7oMHGHkVmsrbqDIGvTV5DW2"
                
            frame_count = 0

            
            while is_running:
                
                print("started streaming...")
                
                app = Stream_demo(input_url, output_url)
                
                while is_running:
                
                    try:
                        result = app.send_stream()
                                
                        if result == -1:  # End of stream
                            print("End of stream reached")
                            break
                        elif result == 1:  # Video frame 
                            self.frame_count += 1
                            if self.frame_count % 100 == 0:
                                print(f"Sent {self.frame_count} frames")
                    
                        
                    except Exception as e:
                            print(f"Error during streaming: {e}")
                            break



            # if is_running == False:

                # p_thread = subprocess.Popen(["python", "test_thread2.py"])

                # p_thread = subprocess.Popen(["ffmpeg",
                #     "-i", url,
                #     "-c", "copy",
                #     "-f", "flv",
                #     "-fflags", "nobuffer",
                #     "-flags", "low_delay",
                #     twitch_rtmp_url])


                # p_thread = subprocess.Popen(
                #                     [
                #                         "ffmpeg",
                #                         "-i", url,
                #                         "-c", "copy",
                #                         "-f", "flv",
                #                         "-fflags", "nobuffer",
                #                         "-flags", "low_delay",
                #                         "-loglevel", "error",  # Only show errors
                #                         "-reconnect", "1",
                #                         "-reconnect_at_eof", "1",
                #                         "-reconnect_streamed", "1",
                #                         "-reconnect_delay_max", "5",
                #                         twitch_rtmp_url
                #                     ],
                #                     stderr=subprocess.PIPE,  # Capture stderr
                #                     universal_newlines=True
                #                 )



                # is_running = True

                

            

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
        return render_template('app.html', is_streaming=is_running)

    else:        

        return render_template('app.html', is_streaming=is_running)
    
    # return f"miki streaming app is {stream_t1.is_alive()}"

@app.route('/start')
def start_stream():

    global stream_t1
    global is_running

    if is_running == False:

            is_running = True

            stream_t1 = threading.Thread(target=miki)
            stream_t1.start()
            # return f"{is_running}"  
       
    
    return f"{is_running}"
                

@app.route('/stop')
def stop_stream():

    # try:
        
    #     if p_thread:
        
    #         p_thread.terminate()
    #         p_thread.wait()
    #         print("stoped thread")

    #         global is_running
    #         is_running = False
    # except:
    #     pass
    
    global stream_t1
    global is_running
    
    if is_running == True:
        is_running = False
        stream_t1.join()
        
        
        # if stream_t1.is_alive() == False:
        

    # if stream_t1 != None:
    #     return f"{stream_t1.is_alive()}"

    # else:
    return f"{is_running}"  

    



if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve(port=5000)
    print("server starting...")
    app.run(host="0.0.0.0", port=5000)
  
