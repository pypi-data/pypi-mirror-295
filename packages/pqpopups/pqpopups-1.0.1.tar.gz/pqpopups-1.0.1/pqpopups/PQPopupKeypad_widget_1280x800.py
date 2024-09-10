from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import QRect, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont

from pqwidgets.PQImage import PQImage
from pqwidgets.PQLabel import PQLabel
from pqwidgets.PQButton import PQButton
from PQPopupDef import modeOS, DirPathDef, enSoundType, enPopupButton, styleSheet

G_POPUP_KEY_INTERVAL = 8
POPUP_KEYPAD_W = 948
POPUP_KEYPAD_H = 400
WIN_W = 1280
WIN_H = 800
nX = 0
nY = 0
KEYSIZE = (52,52)
Rect_1 = QRect(nX + 24, nY + 86, 52, 52)
Rect_Back = QRect(nX + 804, nY + 86, 110, 52)
Rect_2 = QRect(nX + 114, nY + 146, 52, 52)
Rect_3 = QRect(nX + 130, nY + 206, 52, 52)
Rect_LeftCaps = QRect(nX + 26, nY + 266, 124, 52)
Rect_4 = QRect(nX + 158, nY + 266, 52, 52)
Rect_RightCaps = QRect(nX + 758, nY + 266, 156, 52)
Rect_Space = QRect(nX + 204, nY + 326, 530, 52)
ARRAY_NUBER = ['','1','2','3','4','5','6','7','8','9','0','-','='],['','1','2','3','4','5','6','7','8','9','0','_','+']
ARRAY_QWERT = ['Q','W','E','R','T','Y','U','I','O','P','[',']'],['q','w','e','r','t','y','u','i','o','p','{','}']
ARRAY_ASDFG = ['A','S','D','F','G','H','J','K','L','',''],['a','s','d','f','g','h','j','k','l','','']
ARRAY_ZXCVB = ['Z','X','C','V','B','N','M',',','',''],['z','x','c','v','b','n','m',',','','']
LENGTH_NUMBER=13
LENGTH_QWERT=12
LENGTH_ASDFG=11
LENGTH_ZXCVB = 10

# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# UI UiKeypad
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

class popupNumberKeypadWidgetSignals(QObject):
    # SIGNALS
    CLOSE = pyqtSignal()


class UiKeypad_widget(QWidget):
    def __init__(self, parent):
        super(UiKeypad_widget, self).__init__(parent)
        self.Variable_Init()
        self.Disp_Background()
        self.Disp_Init()
        self.Disp_Keyboard()
        # self.Disp_CenterWindow()

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
        keypadX = x - (POPUP_KEYPAD_W / 2)
        keypadY = y - (POPUP_KEYPAD_H / 2)
        self.lbKeyPadBG.move(keypadX, keypadY)
        self.lbKeyPadBG_Edit.move(keypadX + 160, keypadY + 15)
        self.lbKeypadVal.move(keypadX + 175, keypadY + 20)
        self.btnAllClear.move(keypadX + 715, keypadY + 32)
        self.btnClose.move(keypadX + 882, keypadY + 10)
        self.btnDone.move(keypadX + 744, keypadY + 326)
        posX = Rect_1.x() + keypadX
        for i in range(LENGTH_NUMBER):
            self.btnNUMBER[i].move(posX, Rect_1.y() + keypadY)
            posX = posX +60
        posX = Rect_2.x() + keypadX
        for i in range(LENGTH_QWERT):
            self.btnQWERT[i].move(posX, Rect_2.y() + keypadY)
            posX = posX +60
        posX = Rect_3.x() + keypadX
        for i in range(LENGTH_ASDFG):
            self.btnASDFG[i].move(posX, Rect_3.y() + keypadY)
            posX = posX +60
        posX = Rect_4.x() + keypadX
        for i in range(LENGTH_ZXCVB):
            self.btnZXCVB[i].move(posX, Rect_4.y() + keypadY)
            posX = posX +60
        self.btnSpace.move(Rect_Space.x()+keypadX,Rect_Space.y()+keypadY)
        self.btnBackSpace.move(Rect_Back.x() + keypadX, Rect_Back.y() + keypadY)
        self.btnLeftCaps.move(Rect_LeftCaps.x() + keypadX, Rect_LeftCaps.y() + keypadY)
        self.btnRightCaps.move(Rect_RightCaps.x() + keypadX, Rect_RightCaps.y() + keypadY)

    def Variable_Init(self):
        self.btnNUMBER = [PQLabel for i in range(LENGTH_NUMBER)]
        self.btnQWERT = [PQLabel for i in range(LENGTH_QWERT)]
        self.btnASDFG = [PQLabel for i in range(LENGTH_ASDFG)]
        self.btnZXCVB = [PQLabel for i in range(LENGTH_ZXCVB)]

    def Disp_Background(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.SIGNALS = popupNumberKeypadWidgetSignals()

    def Disp_Init(self):
        self.lbKeyPadBG = PQLabel(self, QRect(0, 0, POPUP_KEYPAD_W, POPUP_KEYPAD_H))
        self.lbKeyPadBG.setStyleSheet(styleSheet.BACKGROUND_STYLE_01)

        self.lbKeyPadBG_Edit = PQLabel(self, QRect(0, 0, 600, 60))
        self.lbKeyPadBG_Edit.setStyleSheet(styleSheet.EDIT_STYLE_01)

        self.lbKeypadVal = PQLabel(self, QRect(146 + 10, 15 + 5, 596 - 70, 60 - 15))

        self.btnAllClear = PQLabel(self, QRect(0, 0, 24, 24), "X",18,False)
        # QLabel에 스타일 적용
        self.btnAllClear.setStyleSheet(styleSheet.CIRCLE_STYLE_01)
        self.btnAllClear.move(695, 32)
        self.btnAllClear.clicked.connect(self.onBtnClickKeypadPopupAllClear)

        self.btnClose = PQLabel(self, QRect(0, 0, 50, 50),'X',40,False)
        self.btnClose.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.btnClose.setStyleSheet(styleSheet.BACKGROUND_STYLE_02)
        # QFont를 사용하여 폰트 변경
        font = QFont('Gothic', 35, QFont.Bold)  # 폰트명, 크기, 굵기 설정
        self.btnClose.setFont(font)
        self.btnClose.move(892, 32)
        self.btnClose.clicked.connect(self.onBtnClickKeypadPopupClose)

        self.btnDone = PQButton(self, QRect(0, 0, 170, 52),'Done',18,False,QColor(109, 209, 207),QColor(69, 179, 176),QColor(255, 255, 255),0)
        self.btnDone.move(744, 326)
        self.btnDone.clicked.connect(self.onBtnClickKeypadDone)

    def Disp_Keyboard(self):
        #NUMPAD
        for item in range(0, LENGTH_NUMBER):
            self.btnNUMBER[item] = PQLabel(self, QRect(0,0,KEYSIZE[0],KEYSIZE[1]),ARRAY_NUBER[0][item],18,False)#,QColor(230, 230, 230),QColor(210, 210, 210),QColor(0, 0, 0),0)
            if item < 11 and item > 0:
                self.btnNUMBER[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_02)
            else:
                self.btnNUMBER[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
            self.btnNUMBER[item].clicked.connect(lambda r=item: self.KeypadInputClicked_Number(r))
        # Q, W, E, R, T, Y, U, I, O, P, [, ]
        for item in range(0, LENGTH_QWERT):
            self.btnQWERT[item] = PQLabel(self, QRect(0,0,KEYSIZE[0],KEYSIZE[1]),ARRAY_QWERT[0][item],18,False)#,QColor(230, 230, 230),QColor(210, 210, 210),QColor(0, 0, 0),0)
            self.btnQWERT[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
            self.btnQWERT[item].clicked.connect(lambda r=item: self.KeypadInputClicked_QWERT(r))
        # A, S, D, F, G, H, J, K, L, ;, '
        for item in range(0, LENGTH_ASDFG):
            self.btnASDFG[item] = PQLabel(self, QRect(0,0,KEYSIZE[0],KEYSIZE[1]),ARRAY_ASDFG[0][item],18,False)#,QColor(230, 230, 230),QColor(210, 210, 210),QColor(0, 0, 0),0)
            self.btnASDFG[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
            self.btnASDFG[item].clicked.connect(lambda r=item: self.KeypadInputClicked_ASDFG(r))
        # Z, X, C, V, B, N, M, (,), (.), /
        for item in range(0, LENGTH_ZXCVB):
            self.btnZXCVB[item] = PQLabel(self, QRect(0,0,KEYSIZE[0],KEYSIZE[1]),ARRAY_ZXCVB[0][item],18,False)#,QColor(230, 230, 230),QColor(210, 210, 210),QColor(0, 0, 0),0)
            self.btnZXCVB[item].setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
            self.btnZXCVB[item].clicked.connect(lambda r=item: self.KeypadInputClicked_ZXCVB(r))
        # Space
        self.btnSpace = PQLabel(self, Rect_Space, '', 18, False)#, QColor(230, 230, 230), QColor(210, 210, 210),QColor(0, 0, 0), 0)
        self.btnSpace.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnSpace.clicked.connect(self.KeypadInputClicked_Space)
        # Backspace
        self.btnBackSpace = PQLabel(self, Rect_Back, 'Back', 18, False)#, QColor(230, 230, 230), QColor(210, 210, 210),QColor(0, 0, 0), 0)
        self.btnBackSpace.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnBackSpace.clicked.connect(self.KeypadInputClicked_Backspace)
        # Left Caps
        self.btnLeftCaps = PQLabel(self, Rect_LeftCaps, 'Shift', 18, False)#, QColor(230, 230, 230), QColor(210, 210, 210),QColor(0, 0, 0), 0)
        self.btnLeftCaps.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnLeftCaps.clicked.connect(self.KeypadInputClicked_Caps)
        # Right Caps
        self.btnRightCaps = PQLabel(self, Rect_RightCaps, 'Shift', 18, False)#, QColor(230, 230, 230), QColor(210, 210, 210),QColor(0, 0, 0), 0)
        self.btnRightCaps.setStyleSheet(styleSheet.KEYBOARD_STYLE_01)
        self.btnRightCaps.clicked.connect(self.KeypadInputClicked_Caps)

    def Disp_CenterWindow(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - WIN_W) / 2
        y = (screen.height() - WIN_H) / 2

        if modeOS.mode_Curr == modeOS.mode_Windows:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((WIN_W - POPUP_KEYPAD_W) / 2), y + ((WIN_H - POPUP_KEYPAD_H) / 2), POPUP_KEYPAD_W,
                             POPUP_KEYPAD_H)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((WIN_W - POPUP_KEYPAD_W) / 2), y + ((WIN_H - POPUP_KEYPAD_H) / 2), POPUP_KEYPAD_W,
                             POPUP_KEYPAD_H)

# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# popup popupKeypad
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
class PQPopupKeypad_widget_1280x800(UiKeypad_widget):
    def __init__(self, parent, keyVal=  "", rect = QRect(0,0,WIN_W,WIN_H)):
        super(PQPopupKeypad_widget_1280x800, self).__init__(parent)
        self.parent = parent
        self.result = ""
        self.keyVal = keyVal
        self.bCaps = False
        self.retKey = enPopupButton.Btn_Cancel
        self.lbKeypadVal.setText(self.keyVal)
        self.move(rect.x(),rect.y())
        self.resize(rect.width(),rect.height())

    def KeypadInputClicked_AllClear(self, x, y, rect):
        stX = rect.x()
        stY = rect.y()
        if stX <= x <= stX + rect.width() and stY <= y <= stY + rect.height():
            # _com.ComSound.play(enSoundType.EN_BUTTON_SOUND_TYPE)
            self.lbKeypadVal.setText("")
            return False
        return True

    def KeypadInputClicked_Space(self):
        self.InputValCal(True, ' ')

    def KeypadInputClicked_ZXCVB(self,item):
        if item == 0:
            self.inputCapsKey('Z', 'z')
        elif item == 1:
            self.inputCapsKey('X', 'x')
        elif item == 2:
            self.inputCapsKey('C', 'c')
        elif item == 3:
            self.inputCapsKey('V', 'v')
        elif item == 4:
            self.inputCapsKey('B', 'b')
        elif item == 5:
            self.inputCapsKey('N', 'n')
        elif item == 6:
            self.inputCapsKey('M', 'm')
        elif item == 7:
            self.inputCapsKey(',', '')  # (',', '<')
        elif item == 8:
            self.inputCapsKey('', '')  # ('.', '>')
        elif item == 9:
            self.inputCapsKey('', '')  # ('/', '?')

    def KeypadInputClicked_Caps(self):
        self.setKeypadCaps()

    def KeypadInputClicked_ASDFG(self, item):
        if item == 0:
            self.inputCapsKey('A', 'a')
        elif item == 1:
            self.inputCapsKey('S', 's')
        elif item == 2:
            self.inputCapsKey('D', 'd')
        elif item == 3:
            self.inputCapsKey('F', 'f')
        elif item == 4:
            self.inputCapsKey('G', 'g')
        elif item == 5:
            self.inputCapsKey('H', 'h')
        elif item == 6:
            self.inputCapsKey('J', 'j')
        elif item == 7:
            self.inputCapsKey('K', 'k')
        elif item == 8:
            self.inputCapsKey('L', 'l')
        elif item == 9:
            self.inputCapsKey('', '')  # (';', ':')
        elif item == 10:
            self.inputCapsKey('', '')  # ("'", '"')

    def KeypadInputClicked_QWERT(self, item):
        if item == 0:
            self.inputCapsKey('Q', 'q')
        elif item == 1:
            self.inputCapsKey('W', 'w')
        elif item == 2:
            self.inputCapsKey('E', 'e')
        elif item == 3:
            self.inputCapsKey('R', 'r')
        elif item == 4:
            self.inputCapsKey('T', 't')
        elif item == 5:
            self.inputCapsKey('Y', 'y')
        elif item == 6:
            self.inputCapsKey('U', 'u')
        elif item == 7:
            self.inputCapsKey('I', 'i')
        elif item == 8:
            self.inputCapsKey('O', 'o')
        elif item == 9:
            self.inputCapsKey('P', 'p')
        elif item == 10:
            self.inputCapsKey('[', '{')
        elif item == 11:
            self.inputCapsKey(']', '}')

    def KeypadInputClicked_Backspace(self):
        self.InputValCal(False, "")

    def KeypadInputClicked_Number(self, item):
        if item == 0:
            self.inputCapsKey('', '')  # ('`', '~')
        elif item == 1:
            self.inputCapsKey('1', '1')  # ('1', '!')
        elif item == 2:
            self.inputCapsKey('2', '2')  # ('2', '@')
        elif item == 3:
            self.inputCapsKey('3', '3')  # ('3', '#')
        elif item == 4:
            self.inputCapsKey('4', '4')  # ('4', '$')
        elif item == 5:
            self.inputCapsKey('5', '5')  # ('5', '%')
        elif item == 6:
            self.inputCapsKey('6', '6')  # ('6', '^')
        elif item == 7:
            self.inputCapsKey('7', '7')  # ('7', '&')
        elif item == 8:
            self.inputCapsKey('8', '8')  # ('8', '*')
        elif item == 9:
            self.inputCapsKey('9', '9')  # ('9', '(')
        elif item == 10:
            self.inputCapsKey('0', '0')  # ('0', ')')
        elif item == 11:
            self.inputCapsKey('-', '_')
        elif item == 12:
            self.inputCapsKey('=', '+')

    def setKeypadCaps(self):
        self.bCaps = not self.bCaps
        if self.bCaps:
            self.ChangeCapsKeyboard(1)
        else:
            self.ChangeCapsKeyboard(0)

    def InputValCal(self, Add, Val):
        strVal = self.lbKeypadVal.text()
        if Add == True:
            strText = strVal + Val
            self.lbKeypadVal.setText(strText)
        else:  # Substrction
            nLen = len(strVal)
            if nLen > 0:
                strText = strVal[:nLen - 1]
                self.lbKeypadVal.setText(strText)

    def GetValue(self):
        self.result = self.lbKeypadVal.text()
        return self.retKey, self.result

    def inputCapsKey(self, caps, nocaps):
        if not self.bCaps:
            self.InputValCal(True, caps)
        else:
            self.InputValCal(True, nocaps)

    def ChangeCapsKeyboard(self,Caps):
        #NUMPAD
        for item in range(0, 13):
            self.btnNUMBER[item].setText(ARRAY_NUBER[Caps][item])
        # Q, W, E, R, T, Y, U, I, O, P, [, ]
        for item in range(0, 12):
            self.btnQWERT[item].setText(ARRAY_QWERT[Caps][item])
        # A, S, D, F, G, H, J, K, L, ;, '
        for item in range(0, 11):
            self.btnASDFG[item].setText(ARRAY_ASDFG[Caps][item])
        # Z, X, C, V, B, N, M, (,), (.), /
        for item in range(0, 10):
            self.btnZXCVB[item].setText(ARRAY_ZXCVB[Caps][item])

    # ------------------------------------------------------------------------------------------------------------------------
    # Button Event
    # ------------------------------------------------------------------------------------------------------------------------
    def onBtnClickKeypadPopupClose(self):
        # _com.ComSound.play(enSoundType.EN_BUTTON_SOUND_TYPE)
        self.retKey = enPopupButton.Btn_Cancel
        self.SIGNALS.CLOSE.emit()

    def onBtnClickKeypadDone(self):
        # _com.ComSound.play(enSoundType.EN_BUTTON_SOUND_TYPE)
        self.retKey = enPopupButton.Btn_Ok
        self.SIGNALS.CLOSE.emit()

    def onBtnClickKeypadPopupAllClear(self):
        # _com.ComSound.play(enSoundType.EN_BUTTON_SOUND_TYPE)
        self.lbKeypadVal.setText("")

