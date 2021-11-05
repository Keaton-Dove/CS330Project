from BookingApp import *

class ExitWindow(View):

    def __init__(self, app: BookingApp):
        super().__init__()

        self.app = app
        self.window = self.app.getWindow()

        instruction = Text(Point(400, 760), "You may now exit the program")
        instruction.setSize(22)
        instructionV = DrawableView(instruction, self.window)
        self.addSubView(instructionV)

        self.statusText = Text(Point(400, 100), "")
        self.statusText.setSize(24)
        statusTextV = DrawableView(self.statusText, self.window)
        self.addSubView(statusTextV)

    def _initChangeFailure(self):
        self.statusText.setText("You cannot change your booking any more.")

    def _initSeatFailure(self):
        self.statusText.setText("We're sorry, but we do not have enough seats for your group...")

    def _initSuccessful(self):
        self.statusText.setText("Booking complete! Your flight information is listed below:")

        # Getting groupID, seats, and rating to all be displayed
        groupID = self.app.getActiveGroupID()
        group = self.app.idToGroup(groupID)
        seats = group.getSeats()
        rating = group.getSatisfactionRating()

        #Create background for information to be displayed on
        bgRectangle = Rectangle(Point(200, 200), Point(600, 550))
        bgRectangle.setFill("white")
        bgRectangleV = DrawableView(bgRectangle, self.window)
        self.addSubView(bgRectangleV)

        # Creating labels to display all relevant group information
        idLabel = Text(Point(400, 310), "Group ID = " +  str(groupID))
        idLabel.setSize(20)
        idLabelV = DrawableView(idLabel, self.window)
        self.addSubView(idLabelV)

        seatsText = ""
        for s in seats:
            seatsText += s.getName() + " "

        seatsLabel = Text(Point(400, 375), "Seats = " +  seatsText)
        seatsLabel.setSize(20)
        seatsLabelV = DrawableView(seatsLabel, self.window)
        self.addSubView(seatsLabelV)

        ratingLabel = Text(Point(400, 440), "Satisfaction rating = " +  str(rating))
        ratingLabel.setSize(20)
        ratingLabelV = DrawableView(ratingLabel, self.window)
        self.addSubView(ratingLabelV)

    def seatingWinButtonCallback(self, b: Button, p: Point):
        seatingWin = self.app.strToWin("SeatingWindow")
        seatingWin._initSeats()
        self.app.switchWindow(self, seatingWin)