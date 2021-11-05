#!/usr/bin/env python3

# ----------------------------------------------------------------------
# RadioButtons.py
# Dave Reed
# 09/29/2020

# Keaton Dove
# 11/12/2020
# ----------------------------------------------------------------------

from typing import Dict
from ToggleButton import *

class RadioButtons(View):

    _selectedToggle: ToggleButton
    _titleToToggle: Dict[str, ToggleButton]

    # ------------------------------------------------------------------

    def __init__(self, window: GraphWin, titles: List[str], selectedTitle: str, center: Point, width: float,
                 height: float, flipVertically: bool = False, clickHandler=None):
        """
        :param window: window to draw the RadioButton in
        :param titles: list of strings for the titles of the buttons
        :param selectedTitle: which button to select initial (must be one of strings in titles)
        :param center: center Point for RadioButtons
        :param width: width of each individual ToggleButton
        :param height: height of each individual ToggleButton
        :param flipVertically: whether or not to flip label and circle vertically
        :param clickHandler: function/method to call when Radio button is selected; must have parameters
            radioButton: RadioButtons, selected: ToggleButton, prev: ToggleButton, pt: Point
        """
        
        super().__init__()

        self._titles = titles
        self._toggleButtons = []
        self._titleToToggle: Dict[str, ToggleButton] = {}
        self._clickHandler = clickHandler

        amountOfButtons = len(titles)
        halfWidth = width / 2

        # Loop to construct all of the tButtons
        for i in range(len(titles)):
            tButtonX = center.getX() + halfWidth * ((-amountOfButtons + 1) + (2 * i))
            tButtonCenter = Point(tButtonX, center.getY())

            tButton = ToggleButton(window, titles[i], tButtonCenter, width, height, flipVertically)
            # Adding the new button to the subviews
            self.addSubView(tButton)
            # Mapping the title of each button to its button object
            self._titleToToggle[tButton.title()] = tButton
            self._toggleButtons.append(tButton)

        # Setting the selectedToggle to the newly constructed toggle button
        self._selectedToggle = self._titleToToggle.get(selectedTitle)
        self._selectedToggle.setSelected()

    # ------------------------------------------------------------------

    def clicked(self, pt: Point) -> bool:
        # Checking all the toggle buttons to find which one was clicked
        for tb in self._toggleButtons:
            if tb.clicked(pt):
                # If one was clicked, the previous button is the old selected button
                prevTb = self._selectedToggle
                # The button clicked is now the selected button
                self._selectedToggle = tb

                # Calling _buttonSelected()
                self._buttonSelected()

                # Click handler
                if self._clickHandler is not None:
                    self._clickHandler(self, self._selectedToggle, prevTb, pt)

                return True

    # ------------------------------------------------------------------

    def _buttonSelected(self):

        # Setting the selected toggle button to be selected
        if not self._selectedToggle.isSelected():
            self._selectedToggle.setSelected(True)

        # Deselecting all the other buttons
        for tb in self._toggleButtons:
            # If they don't share the same title.\
            if tb.title() != self._selectedToggle.title():
                tb.setSelected(False)

    # ------------------------------------------------------------------
