#!/usr/bin/env python3
import gui
import threading

gui_thread = threading.Thread(target=gui.start)
gui_thread.start()
