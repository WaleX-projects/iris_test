
import webview


HTML = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">

    <style>
        * {
            box-sizing: border-box;
        }

        html,
        body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }

        body {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #orb {
            width: 64px;
            height: 64px;

            border-radius: 50%;

            background: #111;

            position: relative;

            cursor: grab;

            box-shadow:
                0 4px 18px rgba(0, 0, 0, 0.35);

            transition:
                transform 0.15s ease;
        }

        #orb:active {
            cursor: grabbing;
        }

        #core {
            position: absolute;

            width: 12px;
            height: 12px;

            border-radius: 50%;

            background: white;

            left: 50%;
            top: 50%;

            transform: translate(-50%, -50%);
        }

        /*
        ============================================================
        LISTENING
        ============================================================
        */

        #orb.listening {
            animation: pulse 1.2s infinite ease-in-out;
        }

        #orb.listening #core {
            animation: corePulse 1.2s infinite ease-in-out;
        }

        @keyframes pulse {

            0% {
                transform: scale(1);

                box-shadow:
                    0 4px 18px rgba(0, 0, 0, 0.35),
                    0 0 0 0 rgba(255, 255, 255, 0.35);
            }

            50% {
                transform: scale(1.10);

                box-shadow:
                    0 4px 24px rgba(0, 0, 0, 0.40),
                    0 0 0 12px rgba(255, 255, 255, 0);
            }

            100% {
                transform: scale(1);

                box-shadow:
                    0 4px 18px rgba(0, 0, 0, 0.35),
                    0 0 0 0 rgba(255, 255, 255, 0);
            }
        }

        @keyframes corePulse {

            0% {
                transform: translate(-50%, -50%) scale(1);
            }

            50% {
                transform: translate(-50%, -50%) scale(1.35);
            }

            100% {
                transform: translate(-50%, -50%) scale(1);
            }
        }
    </style>
</head>

<body>

    <div id="orb">
        <div id="core"></div>
    </div>


    <script>

        const orb = document.getElementById("orb");

        let listening = false;

        let dragging = false;
        let moved = false;

        let startMouseX = 0;
        let startMouseY = 0;

        let startWindowX = 0;
        let startWindowY = 0;


        /*
        ============================================================
        MOUSE DOWN
        ============================================================
        */

        orb.addEventListener("mousedown", async (event) => {

            if (event.button !== 0) {
                return;
            }

            dragging = true;
            moved = false;

            startMouseX = event.screenX;
            startMouseY = event.screenY;

            const position =
                await pywebview.api.get_position();

            startWindowX = position.x;
            startWindowY = position.y;

            event.preventDefault();
        });


        /*
        ============================================================
        MOUSE MOVE
        ============================================================
        */

        document.addEventListener("mousemove", async (event) => {

            if (!dragging) {
                return;
            }

            const dx =
                event.screenX - startMouseX;

            const dy =
                event.screenY - startMouseY;


            if (
                Math.abs(dx) > 3 ||
                Math.abs(dy) > 3
            ) {
                moved = true;
            }


            await pywebview.api.move_window(
                Math.round(startWindowX + dx),
                Math.round(startWindowY + dy)
            );
        });


        /*
        ============================================================
        MOUSE UP
        ============================================================
        */

        document.addEventListener("mouseup", (event) => {

            if (!dragging) {
                return;
            }

            dragging = false;


            /*
                If the mouse didn't move,
                this was a CLICK rather than a drag.
            */

            if (!moved) {
                toggleListening();
            }
        });


        /*
        ============================================================
        LISTENING STATE
        ============================================================
        */

        async function toggleListening() {

            listening = !listening;

            setListeningVisual(listening);

            await pywebview.api.set_listening(
                listening
            );
        }


        function setListeningVisual(value) {

            if (value) {

                orb.classList.add("listening");

            } else {

                orb.classList.remove("listening");
            }
        }


        /*
        Python can call this later.
        */

        function setListening(value) {

            listening = value;

            setListeningVisual(value);
        }

    </script>

</body>
</html>
"""


class IrisAPI:

    def __init__(self):
        self.window = None


    def get_position(self):

        return {
            "x": self.window.x,
            "y": self.window.y
        }


    def move_window(self, x, y):

        self.window.move(
            int(x),
            int(y)
        )


    def set_listening(self, listening):

        print(
            "Iris listening:",
            listening
        )

        # Later:
        #
        # if listening:
        #     start_whisper()
        # else:
        #     stop_whisper()

        return listening


    def close(self):

        self.window.destroy()


api = IrisAPI()


window = webview.create_window(

    "Iris",

    html=HTML,

    width=84,
    height=84,

    frameless=True,

    transparent=True,

    on_top=True,

    resizable=False,

    js_api=api
)


api.window = window


webview.start(
    debug=True
)
