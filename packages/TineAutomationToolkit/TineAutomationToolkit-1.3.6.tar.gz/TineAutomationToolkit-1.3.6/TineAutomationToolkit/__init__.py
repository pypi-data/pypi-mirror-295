# -*- coding: utf-8 -*-
from TineAutomationToolkit.keywords import *

class TineAutomationToolkit(
    ToolkitsTest,
    WaitingElement,
    ConnectionManagement,
    ControlElement,
    Scroll,
    CaptureScreenShot,
    KeyEvent,
    Touch,
    ConvertObject,
    ImageProcessing
    ):

    def __init__(self):
        self._screenshot_indexs = 0
        self._status_mode = 'FLUTTER'

    def main(self):
        print("This Main นี้คือ เมน")