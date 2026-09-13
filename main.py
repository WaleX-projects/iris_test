import sys, os
import webview

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Api:
    def send_command(self, text):
        print("Command:", text)
    def start_listening(self):
        print("Listening...")
    def pause(self):
        print("Paused")
    def stop(self):
        print("Stopped")

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Iris',
        resource_path('iris_ui.html'),
        js_api=api,
        frameless=True,
        transparent=True,
        on_top=True,
        width=400,
        height=560,
        easy_drag=False,
    )
    webview.start(gui='edgechromium')   # <-- this line matters on Windows