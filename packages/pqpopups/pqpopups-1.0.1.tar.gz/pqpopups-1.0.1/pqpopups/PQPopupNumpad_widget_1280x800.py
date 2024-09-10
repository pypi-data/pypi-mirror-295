import itertools
import string
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import QRect, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont

from pqwidgets.PQImage import PQImage
from pqwidgets.PQLabel import PQLabel
from pqwidgets.PQButton import PQButton
from PQPopupDef import modeOS, DirPathDef, enSoundType, enPopupButton, styleSheet, enNumpadMode
import math

WIN_W = 1280
WIN_H = 800
KEYSIZE = (52,52)
Rect_1 = QRect(24, 146, 52, 52)
Rect_0_key = QRect(24, 326, 52, 52)
Rect_IntReal = QRect(24 + ((52 + 8) * 1), 326, 52, 52)
Rect_Point = QRect(24 + ((52 + 8) * 2), 326, 52, 52)
Rect_Back = QRect(24 + ((52 + 8) * 3), 146, 52, 112)
Rect_OK = QRect(24 + ((52 + 8) * 3), 266, 52, 112)
Rect_Close = QRect(232, 32, 24, 24)
POPUP_NUMKEYPAD_W = 280
POPUP_NUMKEYPAD_H = 400
ARRAY_NUBER = ['1','2','3','4','5','6','7','8','9']

class popupNumberKeypad2WidgetSignals(QObject):
    # SIGNALS
    CLOSE = pyqtSignal()

class PQPopupNumpad_widget_1280x800(QWidget):
    def __init__(self, parent, maxlenInt, maxlenDec, rect = QRect(0,0,WIN_W,WIN_H)):
        super(PQPopupNumpad_widget_1280x800, self).__init__(parent)
        self.parent = parent
        self.result = ""
        self.maxLenInt = maxlenInt
        self.maxLenDec = maxlenDec
        self.retKey = enPopupButton.Btn_Cancel
        self.move(rect.x(),rect.y())
        self.resize(rect.width(),rect.height())

        self.bInt = True

        #self.Disp_CenterWindow()
        self.Disp_Background()
        self.Disp_Init()

    def paintEvent(self, event):
        screen = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, screen.width(), screen.height())
        qp.end()

        # resize
        x = screen.width() / 2
        y = screen.height() / 2
        keypadX = x - (POPUP_NUMKEYPAD_W / 2)
        keypadY = y - (POPUP_NUMKEYPAD_H / 2)
        self.lbKeyPadBG.move(keypadX, keypadY)
        self.lbKeyPadBG_Edit.move(keypadX+24, keypadY+64)
        self.lbKeypadVal.move(keypadX + 24, keypadY + 62)
        txtlen = len(self.lbKeypadVal.text())
        # self.lbMinus.move(keypadX + 40, keypadY + 105)
        self.lbMinus.move(keypadX + 120 - (txtlen * 8), keypadY + 95)
        self.btnClose.move(keypadX + 232, keypadY + 22)
        posX = Rect_1.x() + keypadX
        posY = Rect_1.y() + keypadY
        for i in range(3):
            for j in range(3):
                self.btnNUMBER[i * 3 + j].move(posX, posY)
                posX = posX +60
            posX = Rect_1.x() + keypadX
            posY = posY +60
        self.btn0Key.move(Rect_0_key.x() + keypadX, Rect_0_key.y() + keypadY)
        self.btnBack.move(Rect_Back.x() + keypadX, Rect_Back.y() + keypadY)
        self.btnOK.move(Rect_OK.x() + keypadX, Rect_OK.y() + keypadY)
        self.btnIntReal.move(Rect_IntReal.x() + keypadX, Rect_IntReal.y() + keypadY)
        self.btnPoint.move(Rect_Point.x() + keypadX, Rect_Point.y() + keypadY)

    def Disp_Background(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.SIGNALS = popupNumberKeypad2WidgetSignals()

    def Disp_CenterWindow(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - WIN_W) / 2
        y = (screen.height() - WIN_H) / 2

        if modeOS.mode_Curr == modeOS.mode_Windows:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((WIN_W - POPUP_NUMKEYPAD_W) / 2), y + ((WIN_H - POPUP_NUMKEYPAD_H) / 2), POPUP_NUMKEYPAD_W, POPUP_NUMKEYPAD_H)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((WIN_W - POPUP_NUMKEYPAD_W) / 2), y + ((WIN_H - POPUP_NUMKEYPAD_H) / 2), POPUP_NUMKEYPAD_W, POPUP_NUMKEYPAD_H)

    def Disp_Init(self):
        self.lbKeyPadBG = PQLabel(self, QRect(0, 0, POPUP_NUMKEYPAD_W, POPUP_NUMKEYPAD_H))
        self.lbKeyPadBG.setStyleSheet(styleSheet.BACKGROUND_STYLE_01)

        self.lbKeyPadBG_Edit = PQLabel(self, QRect(0, 0, 232, 60))
        self.lbKeyPadBG_Edit.setStyleSheet(styleSheet.EDIT_STYLE_01)

        self.lbKeypadVal = PQLabel(self, QRect(24, 72, 232, 60),  "", 20)
        self.lbMinus = PQLabel(self, QRect(100, 105, 10, 3),  "", 10,True)
        self.lbMinus.setStyleSheet(styleSheet.EDIT_STYLE_01)
        self.lbMinus.hide()

        self.btnNUMBER = [PQLabel for i in range(len(ARRAY_NUBER))]
        for item in range(0, len(ARRAY_NUBER)):
            self.btnNUMBER[item] = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), ARRAY_NUBER[item], 18, False)
            self.btnNUMBER[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_02)
            self.btnNUMBER[item].clicked.connect(lambda r=item + 1: self.KeypadInputClicked_Number(r))
        self.btn0Key = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), "0", 18, False)
        self.btn0Key.setStyleSheet(styleSheet.KEYBOARD_STYLE_02)
        self.btn0Key.clicked.connect(lambda : self.KeypadInputClicked_Number(0))

        self.btnBack = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1] * 2 + 8), "←", 18, True)
        self.btnBack.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnBack.clicked.connect(self.KeypadInputClicked_Back)

        self.btnOK = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1] * 2 + 8), "OK", 18, False)
        self.btnOK.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnOK.clicked.connect(self.KeypadInputClicked_OK)

        self.btnIntReal = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), "-", 18, True)
        self.btnIntReal.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnIntReal.clicked.connect(self.KeypadInputClicked_IntReal)

        self.btnPoint = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), ".", 18, False)
        self.btnPoint.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnPoint.clicked.connect(self.KeypadInputClicked_Point)

        self.btnClose = PQLabel(self,QRect(0, 0, 24, 24),'X',18)
        self.btnClose.setStyleSheet(styleSheet.BACKGROUND_STYLE_02)
        self.btnClose.move(172, 32)
        self.btnClose.clicked.connect(self.onBtnClickKeypadPopupClose)

    def KeypadInputClicked_Back(self):
        self.InputValCal(False, "")

    def KeypadInputClicked_OK(self):
        self.retKey = enPopupButton.Btn_Ok
        self.SIGNALS.CLOSE.emit()

    def KeypadInputClicked_Number(self, item):
        if self.lbKeypadVal.text().find('.') > 0:
            strTemp = self.lbKeypadVal.text().split(".")[1]
            nLen = len(strTemp)
            if nLen >= self.maxLenDec:
                return
        else:
            strTemp = self.lbKeypadVal.text()
            nLen = len(strTemp)
            if nLen >= self.maxLenInt:
                return
        self.InputValCal(True, str(item))

    def KeypadInputClicked_Close(self):
        self.retKey = enPopupButton.Btn_Cancel
        self.SIGNALS.CLOSE.emit()

    def KeypadInputClicked_Point(self):
        if len(self.lbKeypadVal.text()) > 0 and self.lbKeypadVal.text().find('.') < 0:
            self.InputValCal(True, ".")

    def KeypadInputClicked_IntReal(self):
        self.bInt = not self.bInt
        if self.bInt:
            self.lbMinus.hide()
            self.btnIntReal.setText("-")
        else:
            self.lbMinus.show()
            self.btnIntReal.setText("+")

    def InputValCal(self, Add, Val):
        strVal = self.lbKeypadVal.text()
        if Add:
            strText = strVal + Val
            self.lbKeypadVal.setText(strText)
        else: #Substrction
            nLen = len(strVal)
            if nLen > 0:
                strText = strVal[:nLen - 1]
                self.lbKeypadVal.setText(strText)


    def GetValue(self):
        self.result = self.lbKeypadVal.text()

        # 마이너스 일 경우
        if not self.bInt:
            self.result = "-" + self.result

        # 마지막 글자가 '.' 일 경우 제거 해서 return
        if self.lbKeypadVal.text().find('.') == len(self.lbKeypadVal.text()) - 1:
            self.result = self.lbKeypadVal.text()[:len(self.lbKeypadVal.text()) - 1]

        return self.retKey, self.result

    # ------------------------------------------------------------------------------------------------------------------------
    # Button Event
    # ------------------------------------------------------------------------------------------------------------------------
    def onBtnClickKeypadPopupClose(self):
        self.retKey = enPopupButton.Btn_Cancel
        self.SIGNALS.CLOSE.emit()


