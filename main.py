import webview

COLLAPSED_SIZE = (64, 64)
EXPANDED_SIZE = (360, 540)
START_X, START_Y = 1500, 700   # pick a starting position on your screen

class Api:
    def __init__(self):
        self.window = None
        self.x = START_X
        self.y = START_Y
        self.size = COLLAPSED_SIZE

    def set_window(self, window):
        self.window = window

    def expand_window(self):
        self._resize_anchored(EXPANDED_SIZE)

    def collapse_window(self):
        self._resize_anchored(COLLAPSED_SIZE)

    def _resize_anchored(self, new_size):
        old_w, old_h = self.size
        new_w, new_h = new_size
        self.x -= (new_w - old_w)   # keep the bottom-right corner fixed
        self.y -= (new_h - old_h)
        self.window.move(self.x, self.y)
        self.window.resize(new_w, new_h)
        self.size = new_size

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
        'Iris', 'iris_ui.html',
        js_api=api,
        frameless=True, transparent=True, on_top=True,
        x=START_X, y=START_Y,
        width=COLLAPSED_SIZE[0], height=COLLAPSED_SIZE[1],
        easy_drag=False,
    )
    api.set_window(window)
    webview.start(gui='edgechromium')