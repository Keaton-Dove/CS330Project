from BookingApp import *

from Button import Button

class BookingWindow(View):

    def __init__(self,app: BookingApp):
        super().__init__()
        self.app = app
        self.window = self.app.getWindow()

        backButton = Button(self.window, "Back", 12, Point(720, 740), 100, 60, clickHandler=self.backButtonCallback)
        self.addSubView(backButton)

        self._famSelectedNum = 0

        # Initializing an instruction label that will be empty until the window is initialized as new or returning group
        self.instructionText = Text(Point(400, 150), "")
        self.instructionText.setSize(22)
        instructionTextV = DrawableView(self.instructionText, self.window)
        self.addSubView(instructionTextV)

    def _initNew(self):

        # Setting instruction text accordingly
        self.instructionText.setText("Please select your group type: ")

        # Buttons for each type of group
        businessButton = Button(self.window, "Business (1)", 16, Point(175, 250), 150, 100, clickHandler=self.businessButtonCallback)
        self.addSubView(businessButton)

        touristButton = Button(self.window, "Tourists (2)", 16, Point(400, 250), 150, 100, clickHandler=self.touristButtonCallback)
        self.addSubView(touristButton)

        self.familyButton = Button(self.window, "Family (3-5)", 16, Point(625, 250), 150, 100, clickHandler=self.familyButtonCallback)
        self.addSubView(self.familyButton)

    def _initGroup(self):

        # Setting instruction text accordingly
        self.instructionText.setText("Please select action: ")

        # The group is already initialized, they can only change seats from here.
        rerollSeatsButton = Button(self.window, "Get new seats", 12, Point(400, 400), 150, 100, clickHandler=self.rerollSeatsButtonCallback)
        self.addSubView(rerollSeatsButton)

        # Creating label displaying how many changes to seating the current group can make
        id = self.app.getActiveGroupID()
        group = self.app.idToGroup(id)
        changes = group.getChangesLeft()

        amntChangesText = Text(Point(400, 325), "Changes left: " + str(changes))
        amntChangesTextV = DrawableView(amntChangesText, self.window)
        self.addSubView(amntChangesTextV)

    # ----------------------------------------------------------
    """ Button Callbacks """

    def backButtonCallback(self, b: Button, p: Point):
        mainWin = self.app.strToWin("MainWindow")
        self.app.switchWindow(self, mainWin)

    def businessButtonCallback(self, b: Button, p: Point):
        check = self.app.book(1)
        self._switchExitWin(check)

    def touristButtonCallback(self, b: Button, p: Point):
        check = self.app.book(2)
        self._switchExitWin(check)

    def familyButtonCallback(self, b: Button, p: Point):
        familyText = Text(Point(400, 475), "Select your family size.....")
        familyText.setSize(18)
        familyTextV = DrawableView(familyText, self.window)
        self.addSubView(familyTextV)
        familyTextV.show()

        # If choosing a family, creating radio buttons that allow user to select amount of members in family.
        amntButtons = RadioButtons(self.window, ["3 (1 Child)", "4 (2 Children)", "5 (3 Children)"], "3 (1 Child)", Point(400, 550), 150, 100, False, clickHandler=self.amntButtonsCallback)
        self._famSelectedNum = 3
        self.addSubView(amntButtons)
        amntButtons.show()

        # And an enter button to submit the num of fam members
        enterButton = Button(self.window, "Enter", 12, Point(400, 650), 90, 60, clickHandler=self.enterButtonCallback)
        self.addSubView(enterButton)
        enterButton.show()

        # Disabling the family button so these buttons cannot be recreated
        self.familyButton.disable()

    def amntButtonsCallback(self, radioButton: RadioButtons, selected: ToggleButton, prev: ToggleButton, pt: Point):
        # Setting the amount of members in the family to be the current val of the toggle buttons
        butNumber = selected.title()
        self._famSelectedNum = int(butNumber[0])

    def enterButtonCallback(self, b: Button, p: Point):
        check = self.app.book(self._famSelectedNum)
        self._switchExitWin(check)

    def rerollSeatsButtonCallback(self, b: Button, p: Point):
        groupID = self.app.getActiveGroupID()
        group = self.app.idToGroup(groupID)

        # If the group doesn't have any changes left, call the switchExitWin with a special condition
        if group.getChangesLeft() == 0:
            self._switchExitWin(False, "changeFailure")
        else:
            # Else just call the switch based on whether seats were booked or not
            check = self.app.changeBooking()
            self._switchExitWin(check)

    # ----------------------------------------------------------

    def _switchExitWin(self, check: bool, keyword: str = ""):

        exitWin = self.app.strToWin("ExitWindow")

        # If booking failed because of changes left, initChangeFailure
        if keyword == "changeFailure":
            exitWin._initChangeFailure()
        # Checking if the group was made during the booking process. Initializing the exit window accordingly
        elif check:
            exitWin._initSuccessful()
        else:
            exitWin._initSeatFailure()

        # Switching window
        self.app.switchWindow(self, exitWin)