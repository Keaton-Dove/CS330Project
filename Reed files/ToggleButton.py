#!/usr/bin/env python3

# ----------------------------------------------------------------------
# ToggleButton.py
# Dave Reed
# 09/29/2020
# ----------------------------------------------------------------------

from View import *

class ToggleButton(RectangularClickableView):

    _isSelected: bool
    _text: DrawableView
    _innerCircle: DrawableView
    _clickChangesSelection: bool

    # ------------------------------------------------------------------

    def __init__(self, window: GraphWin, title: str, center: Point, width: float, height: float,
                 selected: bool = False, flipVertically: bool = False, clickHandler=None,
                 clickChangesSelection: bool = True):
        """
        a circular Toggle button with on/off states
        :param window: window to create the ToggleButton in
        :param title: _text title for the ToggleButton
        :param center: center Point of the ToggleButton
        :param width: width of the ToggleButton
        :param height: height of the ToggleButton
        :param selected: whether or not the ToggleButton is initially selected
        :param flipVertically: whether or not to reverse the Circle and Text label vertically
        :param clickHandler: function/method to call when ToggleButton is clicked; the function/method must have the signature
        that takes parameters with the ToggleButton, whether or not it was just selected, and the Point of the click
        :param clickChangesSelection: if True, when a ToggleButton is clicked, the selection status is toggled and it is re-rendered
        """

        super().__init__(center, width, height, clickHandler)
        self._isSelected = selected
        self._clickChangesSelection = clickChangesSelection

        oneThirdHeight = height / 3.0

        outerCircleRadius = 0.5 * 0.8 * oneThirdHeight
        innerCircleRadius = 0.6 * outerCircleRadius

        oneThirdY = self._yMin + oneThirdHeight
        twoThirdY = self._yMin + 2.0 * oneThirdHeight

        if flipVertically:
            textCenterY = oneThirdY
            circleCenterY = twoThirdY
        else:
            textCenterY = twoThirdY
            circleCenterY = oneThirdY

        halfWidth = 0.5 * width
        halfHeight = 0.5 * height
        p1 = center.clone()
        p2 = center.clone()
        p1.move(-halfWidth, -halfHeight)
        p2.move(halfWidth, halfHeight)

        r = Rectangle(p1, p2)
        r.setFill("white")
        self.addSubView(DrawableView(r, window))

        self._text = DrawableView(Text(Point(center.getX(), textCenterY), title), window)
        self.addSubView(self._text)

        outerCircle = Circle(Point(center.getX(), circleCenterY), outerCircleRadius)
        self.addSubView(DrawableView(outerCircle, window))

        self._innerCircle = DrawableView(Circle(Point(center.getX(), circleCenterY), innerCircleRadius), window)
        self.addSubView(self._innerCircle)

        self._render()

    # ------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def title(self):
        return self._text.graphicsObject().getText()

    # ------------------------------------------------------------------

    def isSelected(self) -> bool:
        return self._isSelected

    # ------------------------------------------------------------------

    def setSelected(self, selected: bool = True):
        self._isSelected = selected
        self._render()

    # ------------------------------------------------------------------

    # noinspection PyUnresolvedReferences
    def _render(self):
        if not self._isHidden:
            if self._isSelected:
                self._text.graphicsObject().setStyle("bold")
                self._innerCircle.graphicsObject().setFill("black")
            else:
                self._text.graphicsObject().setStyle("normal")
                self._innerCircle.graphicsObject().setFill("white")

    # ------------------------------------------------------------------

    def show(self):
        super().show()
        self._render()

    # ------------------------------------------------------------------

    def clicked(self, pt: Point) -> bool:
        """
        :param pt: coordinate of mouse click
        :return: True if click is inside the button and False otherwise
        :post: if button is clicked and clickChangesSelection parameter to constructor was True, it toggles the state of the Toggle button;
        if button is clicked the clickHandler specified in constructor is called before returning True
        """
        didClick = super()._hitTest(pt)
        if didClick:
            if self._clickChangesSelection:
                self._isSelected = not self._isSelected
                self._render()
            if self._clickHandler is not None:
                self._clickHandler(self, self._isSelected, pt)
        return didClick

# ----------------------------------------------------------------------
