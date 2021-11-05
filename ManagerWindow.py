from BookingApp import *

class ManagerWindow(View):

    def __init__(self, app: BookingApp):
        super().__init__()

        self.app = app
        self.window = self.app.getWindow()

        # Banner initialization
        title = Text(Point(400, 50), "Manager Mode")
        title.setStyle('bold')
        title.setStyle('italic')

        title.setSize(28)
        titleV = DrawableView(title, self.window)
        self.addSubView(titleV)

        # Generating all buttons
        delDataButton = Button(self.window, "Delete all flight data", 16, Point(150, 200), 200, 100, clickHandler=self.deleteButtonCallback)
        self.addSubView(delDataButton)

        genReportButton = Button(self.window, "Generate flight report", 16, Point(150, 325), 200, 100, clickHandler=self.genReportButton)
        self.addSubView(genReportButton)

        backButton = Button(self.window, "Back", 12, Point(720, 740), 100, 60, clickHandler=self.backButtonCallback)
        self.addSubView(backButton)

        # Generating labels for managerReport
        self.numPassengersText = Text(Point(550, 250), "")
        self.numPassengersText.setSize(18)
        numPassengersTextV = DrawableView(self.numPassengersText, self.window)
        self.addSubView(numPassengersTextV)

        self.averageScoreText = Text(Point(550, 300), "")
        self.averageScoreText.setSize(18)
        averageScoreTextV = DrawableView(self.averageScoreText, self.window)
        self.addSubView(averageScoreTextV)

    def deleteButtonCallback(self, b: Button, p: Point):
        # Delete data when pressed
        self.app.deleteData()
        print("Data deleted...")

    def genReportButton(self, b: Button, p: Point):
        # Creating the report and updating the labels with the values
        numPassengers, averageScore = self.app.managerReport()
        self.numPassengersText.setText("Number of passengers = " + str(numPassengers))
        self.averageScoreText.setText("Average satisfaction score = " + str(averageScore))

    def backButtonCallback(self, b: Button, p: Point):
        # Switch back to the intro window
        introWin = self.app.strToWin("IntroWindow")
        self.app.switchWindow(self, introWin)
