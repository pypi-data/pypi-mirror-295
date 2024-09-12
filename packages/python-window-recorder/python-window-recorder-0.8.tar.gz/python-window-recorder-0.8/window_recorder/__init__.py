
import time, os
import cv2
from threading import Thread
import ctypes
import win32gui
from window_recorder.capture.d3dcapture import CaptureSession

class Recorder():
    def __init__(recorder, window_title, timeout=120):
        recorder.window_handle = recorder.get_window_handle(window_title)
        session = CaptureSession()
        recorder.state_box = [None, False, False] # frame, changed, stop

        def frame_callback(session):
            frame = session.get_frame()
            if frame is None:
                return
            recorder.state_box[0] = frame
            recorder.state_box[1] = True
        session.frame_callback = frame_callback
        recorder.session = session
        recorder.timeout = timeout
    
    def start(recorder, folder=None, filename=None):
        # Get the current timestamp for the filename
        timestamp = time.strftime('%Y-%m-%d %H-%M-%S')

        # Define the output filename with the timestamp
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)

            folder_path = folder + '/'
        else:
            folder_path = ''
        if filename:
            full_filename = f'{filename}_{timestamp}.mp4'
        else:
            full_filename = timestamp + '.mp4'
        recorder.output_file_path = folder_path + full_filename
        # print('recorder.output_file_path', recorder.output_file_path)

        # Define video codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        window_rect = win32gui.GetWindowRect(recorder.window_handle)
        width, height = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]
        recorder.video_output = cv2.VideoWriter(recorder.output_file_path, fourcc, 50, (width, height))

        # Check if the VideoWriter object is opened successfully
        if not recorder.video_output.isOpened():
            raise Exception('Failed to open the video writer')
        
        # Start window capture
        window_handle = recorder.window_handle
        recorder.session.start(window_handle, False)
        print(f'Starting recording as {recorder.output_file_path}')

        recorder.stop_flag = False
        recorder.timeout_at = time.time() + recorder.timeout
        def start_recorder(recorder):
            while not recorder.stop_flag:
                if recorder.state_box[1]:
                    recorder.state_box[1] = False
                    img = recorder.state_box[0]
                    recorder.video_output.write(img)
                
                if time.time() >= recorder.timeout_at:
                    print(f'Saving recording as {recorder.output_file_path} after timing out')
                    recorder.video_output.release()
                    # recorder.session.stop() # Causes exit
                    break

        recorder.thread = Thread(target=start_recorder, args=(recorder,), daemon=True) # Daemon otherwise won't be able to exit with Ctrl+C
        recorder.thread.start()
    
    def stop(recorder):
        recorder.stop_flag = True
        recorder.thread.join()

        recorder.video_output.release()
        recorder.session.stop()
        print(f'Recording saved as {recorder.output_file_path}')
        return recorder.output_file_path
    
    def get_window_handle(recorder, window_title):
        window_handles = []
        def callback(window_handle, window_handles):
            window_handles.append(window_handle)
            return True
            
        win32gui.EnumWindows(callback, window_handles)
        for current_window_handle in window_handles:
            current_window_title = win32gui.GetWindowText(current_window_handle)
            if window_title.lower() in current_window_title.lower(): # Get window handle with partial match
                return current_window_handle
        
        print(f'Window recorder: Window title "{window_title}" not found, window recorder will not work')
        # raise Exception(f'Window title "{window_title}" not found')