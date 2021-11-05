from BookingApp import *

from EventLoop import *
from IntroWindow import IntroWindow
from MainWindow import MainWindow
from BookingWindow import BookingWindow
from SeatingWindow import SeatingWindow
from ManagerWindow import ManagerWindow
from ExitWindow import ExitWindow

AMOUNT_SEATS = 120

class MainApp(EventLoop):

    def __init__(self):

        super().__init__("Flight Booking", 800, 800)
        self.window = self.window()
        self.window.setBackground("light grey")

        self.app = BookingApp(AMOUNT_SEATS, self.window)

        self.app.loadData()

        introWin = IntroWindow(self.app)
        self.addSubView(introWin)

        mainWin = MainWindow(self.app)
        self.addSubView(mainWin)

        bookingWin = BookingWindow(self.app)
        self.addSubView(bookingWin)

        seatingWin = SeatingWindow(self.app)
        self.addSubView(seatingWin)

        managerWin = ManagerWindow(self.app)
        self.addSubView(managerWin)

        exitWin = ExitWindow(self.app)
        self.addSubView(exitWin)

        self.app.addStrToWin(["IntroWindow", introWin])
        self.app.addStrToWin(["MainWindow", mainWin])
        self.app.addStrToWin(["BookingWindow", bookingWin])
        self.app.addStrToWin(["SeatingWindow", seatingWin])
        self.app.addStrToWin(["ManagerWindow", managerWin])
        self.app.addStrToWin(["ExitWindow", exitWin])
        self.app.switchWindow(None, introWin)


        exitButton = Button(self.window, " X ", 12, Point(775, 15), 50, 30, clickHandler=self.exitButtonCallback)
        self.addSubView(exitButton)
        exitButton.show()

    def exitButtonCallback(self, b: Button, p: Point):
        self.app.exit()

def main():
    mainApp = MainApp()
    mainApp.run()

if __name__ == '__main__':
    main()