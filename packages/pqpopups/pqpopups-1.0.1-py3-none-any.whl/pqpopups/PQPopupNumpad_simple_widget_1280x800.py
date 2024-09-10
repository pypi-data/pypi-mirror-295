from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import QRect, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont

from pqwidgets.PQImage import PQImage
from pqwidgets.PQLabel import PQLabel
from pqwidgets.PQButton import PQButton
from PQPopupDef import modeOS, DirPathDef, enSoundType, enPopupButton, styleSheet, enNumpadMode

WIN_W = 1280
WIN_H = 800
KEYSIZE = (52,52)
Rect_1 = QRect(24, 146, 52, 52)
Rect_0_key = QRect(24, 326, 52, 52)
Rect_Back = QRect(24 + 8 + 52, 326, 52, 52)
Rect_OK = QRect(84 + 8 + 52, 326, 52, 52)
POPUP_NUMKEYPAD_W = 226
POPUP_NUMKEYPAD_H = 400
ARRAY_NUBER = ['1','2','3','4','5','6','7','8','9']

class popupNumberKeypadWidgetSignals(QObject):
    # SIGNALS
    CLOSE = pyqtSignal()

class PQPopupNumpad_simple_widget_1280x800(QWidget):
    def __init__(self, parent, maxlen, mode=enNumpadMode.EN_MODE_NONE, rect = QRect(0,0,WIN_W,WIN_H)):
        super(PQPopupNumpad_simple_widget_1280x800, self).__init__(parent)
        self.parent = parent
        self.result = ""
        self.maxLen = maxlen
        self.retKey = enPopupButton.Btn_Cancel
        self.move(rect.x(),rect.y())
        self.resize(rect.width(),rect.height())
        # 기본, 시간, 온도, 스피드, 볼륨 (스피드, 볼륨은 입력값이 최대값 이상일 경우 최대값으로 리턴하기 위함)
        self.numMode = mode


        #self.Disp_CenterWindow()
        self.Disp_Background()
        self.Disp_Init()

        # 시간, 온도값 입력 시 입력 데이터가 기본 데이터(00:00 or 00.00)를 대체 하기 위함
        if self.numMode == enNumpadMode.EN_MODE_TIME or self.numMode == enNumpadMode.EN_MODE_TEMP:
            self.Disp_Underscore()
            self.insertPos = 0
            self.setUnderscore(self.insertPos)

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
        self.lbKeyPadBG_Edit.move(keypadX+26, keypadY+64)
        self.lbKeypadVal.move(keypadX + 28, keypadY + 64)
        self.btnClose.move(keypadX + 172, keypadY + 22)
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

        # 입력 위치 표시 _ (Time, Temperature 용)
        if self.numMode == enNumpadMode.EN_MODE_TIME or self.numMode == enNumpadMode.EN_MODE_TEMP:
            if self.numMode == enNumpadMode.EN_MODE_TIME:
                nX, nY = 75, 120
            elif self.numMode == enNumpadMode.EN_MODE_TEMP:
                nX, nY = 83, 120

            for i in range(int(len(self.lbUnderscore))):
                if i == 2:
                    nX += 7
                self.lbUnderscore[i].move(keypadX + nX, keypadY + nY)
                nX += 16


    def Disp_Background(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.SIGNALS = popupNumberKeypadWidgetSignals()

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

        self.lbKeyPadBG_Edit = PQLabel(self, QRect(0, 0, 170, 60))
        self.lbKeyPadBG_Edit.setStyleSheet(styleSheet.EDIT_STYLE_01)

        self.btnNUMBER = [PQLabel for i in range(len(ARRAY_NUBER))]
        for item in range(0, len(ARRAY_NUBER)):
            self.btnNUMBER[item] = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), ARRAY_NUBER[item], 18, False)
            self.btnNUMBER[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_02)
            self.btnNUMBER[item].clicked.connect(lambda r=item + 1: self.KeypadInputClicked_Number(r))

        self.btn0Key = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), "0", 18, False)
        self.btn0Key.setStyleSheet(styleSheet.KEYBOARD_STYLE_02)
        self.btn0Key.clicked.connect(lambda : self.KeypadInputClicked_Number(0))

        self.btnBack = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), "←", 18, True)
        self.btnBack.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnBack.clicked.connect(self.KeypadInputClicked_Back)

        self.btnOK = PQLabel(self, QRect(0, 0, KEYSIZE[0], KEYSIZE[1]), "OK", 18, False)
        self.btnOK.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnOK.clicked.connect( self.KeypadInputClicked_OK)

        if self.numMode == enNumpadMode.EN_MODE_NONE or self.numMode == enNumpadMode.EN_MODE_SPEED or \
                self.numMode == enNumpadMode.EN_MODE_VOLUME or self.numMode == enNumpadMode.EN_MODE_COLLECT or \
                self.numMode == enNumpadMode.EN_MODE_CYCLE:
            self.lbKeypadVal = PQLabel(self, QRect(26, 74, 168, 56), "", 20)
        elif self.numMode == enNumpadMode.EN_MODE_TIME:
            self.lbKeypadVal = PQLabel(self, QRect(26, 74, 168, 56), "00:00", 20)
        elif self.numMode == enNumpadMode.EN_MODE_TEMP:
            self.lbKeypadVal = PQLabel(self, QRect(26, 74, 168, 56),"00.0", 20)

        self.btnClose = PQLabel(self,QRect(0, 0, 24, 24),'X',18)
        self.btnClose.setStyleSheet(styleSheet.BACKGROUND_STYLE_02)
        self.btnClose.move(172, 32)
        self.btnClose.clicked.connect(self.onBtnClickKeypadPopupClose)

    # 입력 위치 표시 _ (Time, Temperature 용)
    def Disp_Underscore(self):
        self.lbUnderscore = [PQLabel, PQLabel, PQLabel, PQLabel]

        if self.numMode == enNumpadMode.EN_MODE_TIME:
            nX, nY = 75, 120
        elif self.numMode == enNumpadMode.EN_MODE_TEMP:
            nX, nY = 83, 120

        nW, nH = 14, 5
        for i in range(int(len(self.lbUnderscore))):
            if i == 2:
                nX += 7
            self.lbUnderscore[i] = PQLabel(self, QRect(nX, nY, nW, nH))
            self.lbUnderscore[i].setVisible(False)
            nX += 16

    def KeypadInputClicked_Back(self):
        self.InputValCal(False, "")


    def KeypadInputClicked_OK(self):
        self.retKey = enPopupButton.Btn_Ok
        self.SIGNALS.CLOSE.emit()

    def KeypadInputClicked_Number(self, item):
        strTemp = self.lbKeypadVal.text()
        nLen = len(strTemp)

        if self.numMode == enNumpadMode.EN_MODE_NONE or self.numMode == enNumpadMode.EN_MODE_SPEED or \
                self.numMode == enNumpadMode.EN_MODE_VOLUME or self.numMode == enNumpadMode.EN_MODE_COLLECT or \
                self.numMode == enNumpadMode.EN_MODE_CYCLE:
            if nLen >= self.maxLen:      return
        self.InputValCal(True, str(item))

    def InputValCal(self, Add, Val):
        strVal = self.lbKeypadVal.text()
        if self.numMode == enNumpadMode.EN_MODE_NONE or self.numMode == enNumpadMode.EN_MODE_SPEED or \
                self.numMode == enNumpadMode.EN_MODE_VOLUME or self.numMode == enNumpadMode.EN_MODE_COLLECT or \
                self.numMode == enNumpadMode.EN_MODE_CYCLE:
            if Add == True:
                strText = strVal + Val
                self.lbKeypadVal.setText(strText)
            else: #Substrction
                nLen = len(strVal)
                if nLen > 0:
                    strText = strVal[:nLen - 1]
                    self.lbKeypadVal.setText(strText)
        else:   # Time, Temperature 처리
            if Add == True:
                #10분 단위, 10초 단위가 6이상일 겨우 처리 입력 제한
                if self.numMode == enNumpadMode.EN_MODE_TIME and int(Val) > 5 and (self.insertPos == 0 or self.insertPos == 2):
                    return

                # ':' or '.' 값 때문에 앞 2자리와 뒷 자리 처리 방법을 달리 함
                if self.insertPos < 2:
                    strText = strVal[:self.insertPos] + Val + strVal[self.insertPos + 1:]
                    self.lbKeypadVal.setText(strText)
                else:
                    strText = strVal[:self.insertPos + 1] + Val + strVal[self.insertPos + 2:]
                    self.lbKeypadVal.setText(strText)

                # 길이 초과 시 입력 제한
                if self.numMode == enNumpadMode.EN_MODE_TIME:
                    if self.insertPos < 3:
                        self.insertPos += 1
                elif self.numMode == enNumpadMode.EN_MODE_TEMP:
                    if self.insertPos < 2:
                        self.insertPos += 1

            else:
                # ':' or '.' 값 때문에 앞 2자리와 뒷 자리 처리 방법을 달리 함
                if self.insertPos < 2:
                    strText = strVal[:self.insertPos] + "0" + strVal[self.insertPos + 1:]
                    self.lbKeypadVal.setText(strText)
                else:
                    strText = strVal[:self.insertPos + 1] + "0" + strVal[self.insertPos + 2:]
                    self.lbKeypadVal.setText(strText)

                # 첫번째 자리 처리
                if self.insertPos > 0:
                    self.insertPos -= 1

            self.setUnderscore(self.insertPos)

    def setUnderscore(self, pos):
        for i in range(int(len(self.lbUnderscore))):
            self.lbUnderscore[i].setVisible(False)

        self.lbUnderscore[pos].setVisible(True)

    def GetValue(self):
        self.result = self.lbKeypadVal.text()

        if len(self.result) > 0:    # 값 미입력 시 result 변수 int 반환 에러 관련 처리
            # 온도 80도 이상 입력 시 80도로 고정
            if self.numMode == enNumpadMode.EN_MODE_TEMP:
                if int(self.result[:2]) <= 45:
                    self.result = "45.0"

            # 스피드 200 이상 입력 시 200으로 고정
            if self.numMode == enNumpadMode.EN_MODE_SPEED:
                if int(self.result) >= 200:
                    self.result = "200"

            if self.numMode == enNumpadMode.EN_MODE_VOLUME:
                if int(self.result) >= 1000:
                    self.result = "1000"

            if self.numMode == enNumpadMode.EN_MODE_CYCLE:
                if int(self.result) >= 5:
                    self.result = "5"

        return self.retKey, self.result

    # ------------------------------------------------------------------------------------------------------------------------
    # Button Event
    # ------------------------------------------------------------------------------------------------------------------------
    def onBtnClickKeypadPopupClose(self):
        self.retKey = enPopupButton.Btn_Cancel
        self.SIGNALS.CLOSE.emit()


