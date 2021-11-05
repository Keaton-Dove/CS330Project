from BookingApp import *

class MainWindow(View):

    def __init__(self, app: BookingApp):
        super().__init__()

        self.app = app
        self.window = self.app.getWindow()

        # Drawing buttons
        bookingWinButton = Button(self.window, "Book Seats", 20, Point(400, 250), 300, 125, clickHandler=self.bookingWinButtonCallback)
        self.addSubView(bookingWinButton)

        seatingWinButton = Button(self.window, "View Seating", 20, Point(400, 550), 300, 125, clickHandler=self.seatingWinButtonCallback)
        self.addSubView(seatingWinButton)

    def bookingWinButtonCallback(self, b: Button, p: Point):
        bookingWin = self.app.strToWin("BookingWindow")

        groupID = self.app.getActiveGroupID()

        if groupID == -1:
            bookingWin._initNew()
        else:
            bookingWin._initGroup()

        self.app.switchWindow(self, bookingWin)

    def seatingWinButtonCallback(self, b: Button, p: Point):
        seatingWin = self.app.strToWin("SeatingWindow")
        seatingWin._initSeats()
        self.app.switchWindow(self, seatingWin)
