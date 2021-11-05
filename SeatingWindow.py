from BookingApp import *

class SeatingWindow(View):

    def __init__(self, app: BookingApp):
        super().__init__()

        self.app = app
        self.window = self.app.getWindow()

        backButton = Button(self.window, "Back", 12, Point(720, 740), 100, 60, clickHandler=self.backButtonCallback)
        self.addSubView(backButton)

        # Header
        header = Text(Point(400, 25), "Seating overview")
        header.setStyle('bold')
        header.setSize(23)
        headerV = DrawableView(header, self.window)
        self.addSubView(headerV)

        self._initKey()

    def _initSeats(self):
        activeGroupID = self.app.getActiveGroupID()

        row = 0
        numInRow = 0

        for i in range(self.app.getAmntSeats()):

            seatObj = self.app.idToSeat(i)

            if numInRow < 3:
                tlPoint = Point(25 + (75 * numInRow), 50 + (37 * row))
                brPoint = Point(75 + (75 * numInRow), 80 + (37 * row))

            else:
                tlPoint = Point(235 + (75 * (numInRow - 2)), 50 + (37 * row))
                brPoint = Point(285 + (75 * (numInRow - 2)), 80 + (37 * row))

            rect = Rectangle(tlPoint, brPoint)

            textP = Point(tlPoint.getX() + 25, tlPoint.getY() + 15)
            text = Text(textP, seatObj.getName())
            text.setSize(9)

            if seatObj.getGroupID() == None:
                rect.setFill("white")
            elif seatObj.getGroupID() == activeGroupID:
                rect.setFill("lime green")
            else:
                rect.setFill("red")

            seatT = DrawableView(rect, self.window)
            seatV = DrawableView(text, self.window)

            numInRow += 1
            if numInRow == 6:
                numInRow = 0
                row += 1

            self.addSubView(seatT)
            self.addSubView(seatV)

    def _initKey(self):

        # Labeling the business select rows
        businessSelectText = Text(Point(610, 81), "Business select")
        businessSelectText.setStyle('italic')
        businessSelectTextV = DrawableView(businessSelectText, self.window)
        self.addSubView(businessSelectTextV)

        businessRowLine = Line(Point(540, 48), Point(540, 118))
        businessRowLineV = DrawableView(businessRowLine, self.window)
        self.addSubView(businessRowLineV)

        # Empty seat key
        emptyR = Rectangle(Point(540, 224), Point(580, 250))
        emptyR.setFill("white")
        emptyRV = DrawableView(emptyR, self.window)
        self.addSubView(emptyRV)

        emptyRText = Text(Point(645, 236), "= Available seat")
        emptyRTextV = DrawableView(emptyRText, self.window)
        self.addSubView(emptyRTextV)

        # Taken seat key
        redR = Rectangle(Point(540, 268), Point(580, 292))
        redR.setFill('red')
        redRV = DrawableView(redR, self.window)
        self.addSubView(redRV)

        redRText = Text(Point(654, 280), "= Unavailable seat")
        redRTextV = DrawableView(redRText, self.window)
        self.addSubView(redRTextV)

        # Your seat key
        blueR = Rectangle(Point(540, 310), Point(580, 334))
        blueR.setFill('lime green')
        blueRV = DrawableView(blueR, self.window)
        self.addSubView(blueRV)

        blueRText = Text(Point(630, 322), "= Your seat")
        blueRTextV = DrawableView(blueRText, self.window)
        self.addSubView(blueRTextV)

    def backButtonCallback(self, b: Button, p: Point):
        mainWin = self.app.strToWin("MainWindow")
        self.app.switchWindow(self, mainWin)
