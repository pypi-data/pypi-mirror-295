import os
import math
from qtpy import QtCore
from qtpy.QtCore import Signal, Qt
from qtpy.QtGui import QPainter, QIcon
from qtpy.QtWidgets import QComboBox, QLineEdit
from .countries import countries


class CountryDropdown(QComboBox):

    # Events
    show_popup = Signal()
    hide_popup = Signal()
    geometry_changed = Signal()

    def __init__(self, parent=None):
        """Create a new CountryDropdown instance

        :param parent: the parent widget
        """

        super(CountryDropdown, self).__init__(parent)

        # Connected LineEdit used to display phone code
        self.__phone_code_line_edit = None

        # Initial values
        self.__icon_size = 0
        self.__border_width = 0
        self.__popup_open = False
        self.__current_country_code = ''

        # Initial settings
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.currentTextChanged.connect(self.__handle_current_item_changed)

        # Add all countries to dropdown
        self.__directory = os.path.dirname(os.path.realpath(__file__))
        for country in countries:
            self.addItem(
                QIcon(self.__directory + '/flag_icons/{}.png'.format(country)),
                '{} ({})'.format(countries[country][0], countries[country][1]))

        # Handle initial country
        self.__handle_current_item_changed()

    def paintEvent(self, event):
        """Method that gets called every time the widget needs to be updated.
        Everything related to widget graphics happens here.

        :param event: event sent by PyQt
        """

        painter = QPainter(self)

        if self.count() > 0:
            icon_start = math.ceil((self.height() - self.__icon_size) / 2)

            # Draw country flag icon
            painter.drawPixmap(icon_start, icon_start, self.itemIcon(
                self.currentIndex()).pixmap(self.__icon_size, self.__icon_size))

    def showPopup(self):
        """Method that gets called when the dropdown is opened"""

        super().showPopup()
        self.__popup_open = True
        self.show_popup.emit()
        
    def hidePopup(self):
        """Method that gets called when the dropdown is closed"""

        super().hidePopup()
        self.__popup_open = False
        self.hide_popup.emit()

    def resizeEvent(self, event):
        """Method that gets called when the widget is resized

        :param event: event sent by PyQt
        """

        self.__calculate_geometry()

    def getPhoneCodeLineEdit(self) -> QLineEdit:
        """Get the current phone code LineEdit

        :return: phone code LineEdit
        """

        return self.__phone_code_line_edit

    def setPhoneCodeLineEdit(self, line_edit: QLineEdit):
        """Set the phone code LineEdit

        :param line_edit: new phone code LineEdit
        """

        self.__phone_code_line_edit = line_edit

    def getCountry(self) -> str:
        """Get the current country

        :return: country code (i.e. 'us')
        """

        current_country_name = self.currentText().split(' (')[0]

        for country in countries:
            if countries[country][0] == current_country_name:
                return country

    def getCountryPhoneCode(self) -> str:
        """Get the phone code of the current country

        :return: phone code (i.e. '+1')
        """

        return self.__current_country_code

    def setCountry(self, new_country: str):
        """Set the country

        :param new_country: new country
        """

        new_country = new_country.lower()

        index = 0
        for country in countries:
            if country == new_country:
                self.setCurrentIndex(index)
                break
            index += 1

    def getBorderWidth(self) -> int:
        """Get the current border width

        :return: border width
        """

        return self.__border_width

    def setBorderWidth(self, width: int):
        """Set the border width

        :param width: new border width
        """

        self.__border_width = width
        self.__calculate_geometry()
        self.update()

    def isDropdownOpen(self) -> bool:
        """Gets whether the dropdown is currently opened

        :return: whether the dropdown is currently opened
        """

        return self.__popup_open

    def __calculate_geometry(self):
        """Calculates everything related to widget geometry"""

        self.__icon_size = int((self.height() - self.__border_width * 2) * 0.7)
        icon_start = math.ceil((self.height() - self.__icon_size) / 2)
        text_start = icon_start + (icon_start - self.__border_width) // 5 + self.__icon_size

        if self.__phone_code_line_edit:
            if self.__phone_code_line_edit.text() != self.__current_country_code:
                self.__phone_code_line_edit.setText(self.__current_country_code)

            w = self.__phone_code_line_edit.fontMetrics().tightBoundingRect(self.__phone_code_line_edit.text()).width() + 8 + self.__border_width * 2
            if self.__phone_code_line_edit.width() != w:
                self.__phone_code_line_edit.setFixedWidth(w)

            if self.__phone_code_line_edit.x() != text_start:
                self.__phone_code_line_edit.move(text_start, 0)

            self.setFixedWidth(text_start + self.__phone_code_line_edit.width())
            self.geometry_changed.emit()
            self.update()

    def __update_country_code(self):
        """Updates the country code"""

        if self.count() > 0:
            self.__current_country_code = self.currentText().split('(')[1].split(')')[0]

    def __handle_current_item_changed(self):
        """Handles change of selected dropdown item"""

        self.__update_country_code()
        self.__calculate_geometry()
