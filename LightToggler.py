import sys
import RPi.GPIO as GPIO

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from functools import partial

import UI


class LightToggler(QtWidgets.QMainWindow, UI.Ui_MainWindow):
    
    RED = 11
    YELLOW = 13
    BLUE = 15
    
    current_light = None
    
    
    def __init__(self, parent=None):
        super(LightToggler, self).__init__(parent)
        self.setupUi(self)

        self.btnRed.clicked.connect(partial(self.handle_light_selection, "red"))
        self.btnYellow.clicked.connect(partial(self.handle_light_selection, "yellow"))
        self.btnBlue.clicked.connect(partial(self.handle_light_selection, "blue"))
        self.btnExit.clicked.connect(self.handle_exit)
        
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.YELLOW, GPIO.OUT)
        GPIO.setup(self.BLUE, GPIO.OUT)


    def handle_light_selection(self, light):
        if light is self.current_light:
            return
        
        self.turn_off_lights()
        
        if light is "red":
            GPIO.output(self.RED, GPIO.HIGH)
        elif light is "yellow":
            GPIO.output(self.YELLOW, GPIO.HIGH)
        elif light is "blue":
            GPIO.output(self.BLUE, GPIO.HIGH)
            
        self.current_light = light
        
            
    def turn_off_lights(self):
        for light in [self.RED, self.YELLOW, self.BLUE]:            
            GPIO.output(light, GPIO.LOW)
            
            
    def cleanup(self):
        self.turn_off_lights()
        GPIO.cleanup()


    def closeEvent(self, event):
        self.cleanup()
        event.accept()
            
            
    def handle_exit(self):
        self.cleanup()
        self.close()


def main():
    GPIO.setmode(GPIO.BOARD)
    app = QApplication(sys.argv)
    form = LightToggler()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
