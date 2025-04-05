from flask import Flask
import threading
import subprocess
import time
import logging
import signal
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stream configuration
INPUT_URL = "https://pull-f5-tt03.tiktokcdn.com/game/stream-3287562464610222981_hd.flv"
RTMP_URL = "rtmp://live-lax.twitch.tv/app/live_1072101235_ztWGwxq7oMHGHkVmsrbqDIGvTV5DW2"
STREAM_TIMEOUT = 60  # Timeout in seconds before restarting stream

# Global variable to control streaming thread
stream_active = True

def setup_ffmpeg():
    """Ensure FFmpeg is installed"""
    try:
        subprocess.run(["apt-get", "update"], check=True, timeout=60)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True, timeout=300)
        logger.info("FFmpeg installation/update completed")
    except subprocess.TimeoutExpired:
        logger.warning("Package installation timed out")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install FFmpeg: {e}")

def stream_with_ffmpeg():
    """Robust streaming function with error handling and auto-reconnect"""
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",  # Read input at native frame rate
        "-i", INPUT_URL,
        "-c", "copy",  # Stream copy (no re-encoding)
        "-f", "flv",
        "-flvflags", "no_duration_filesize",  # Prevent filesize header issues
        "-rtmp_buffer", "100",  # Smaller buffer for lower latency
        "-rtmp_live", "live",  # Live stream specifier
        "-headers", "User-Agent: Mozilla/5.0\r\n",  # Some servers require user agent
        "-analyzeduration", "0",  # Faster stream analysis
        "-probesize", "32",  # Faster probing
        "-fflags", "+genpts+discardcorrupt",  # Handle corrupt packets
        "-resend_headers", "1",  # Resend headers after timeout
        "-timeout", "5000000",  # 5 second timeout
        "-reconnect", "1",  # Enable reconnection
        "-reconnect_at_eof", "1",  # Reconnect at end of file
        "-reconnect_streamed", "1",  # Reconnect even for streamed inputs
        "-reconnect_delay_max", "5",  # Max 5 seconds between reconnects
        RTMP_URL
    ]

    while stream_active:
        try:
            logger.info("Starting FFmpeg stream...")
            process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor FFmpeg output
            for line in process.stderr:
                logger.info(line.strip())
                if "Connection timed out" in line:
                    logger.warning("Timeout detected, restarting stream...")
                    process.terminate()
                    break

            process.wait(timeout=STREAM_TIMEOUT)
            if process.returncode != 0:
                logger.warning(f"FFmpeg exited with code {process.returncode}, restarting...")

        except subprocess.TimeoutExpired:
            logger.warning("FFmpeg stream timeout, restarting...")
            process.terminate()
        except Exception as e:
            logger.error(f"Stream error: {e}")
        finally:
            if 'process' in locals():
                process.terminate()
            time.sleep(5)  # Wait before restarting

def start_stream():
    """Start streaming thread"""
    setup_ffmpeg()
    stream_thread = threading.Thread(target=stream_with_ffmpeg)
    stream_thread.daemon = True  # Thread will exit when main program exits
    stream_thread.start()

def stop_stream(signum, frame):
    """Handle shutdown gracefully"""
    global stream_active
    logger.info("Shutting down stream...")
    stream_active = False

@app.route('/')
def index():
    return "Streaming Server is Running"

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, stop_stream)
    signal.signal(signal.SIGTERM, stop_stream)

    start_stream()
    app.run(host="0.0.0.0", port=5000)