import textwrap

from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import QRect, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from pqwidgets.PQImage import PQImage
from pqwidgets.PQLabel import PQLabel
from pqwidgets.PQButton import PQButton
from PQPopupDef import modeOS, DirPathDef, enSoundType, enPopupButton, styleSheet, enPopupIcon

WIN_W = 1280
WIN_H = 800
POPUP_MESSAGE_W = 640
POPUP_MESSAGE_H = 300
POPUP_MESSAGE_H_430 = 430

class popupMessageWidgetSignals(QObject):
    # SIGNALS
    CLOSE = pyqtSignal()

class PQPopupMessage_widget_1280x800(QWidget):
    def __init__(self, parent, sMsg = "",msgType = enPopupIcon.Icon_Working,  btnType = enPopupButton.Btn_Ok, rect = QRect(0,0,WIN_W,WIN_H)):
        super(PQPopupMessage_widget_1280x800, self).__init__(parent)
        self.parent = parent
        self.msgType = msgType      #    Icon_Check = 0    Icon_Question = 1    Icon_Warning = 2    Icon_Working = 3
        self.strMsg = sMsg
        self.BtnType = btnType      #    Btn_None = 0    Btn_Ok = 1    Btn_Cancel = 2    Btn_OkCancel = 10    Btn_YesNo = 30
        self.retKey = enPopupButton.Btn_Cancel
        self.move(rect.x(),rect.y())
        self.resize(rect.width(),rect.height())

        self.Disp_Background()
        self.Disp_Init()
        self.BtnDisp_show(self.BtnType)

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
        popupX = x - (POPUP_MESSAGE_W / 2)
        popupY = y - (POPUP_MESSAGE_H / 2)
        self.lbPopupBG.move(popupX, popupY)
        self.lbPopupBG_OutSymbol.move(popupX+270, popupY-48)
        self.lbPopupBG_InSymbol.move(popupX+280, popupY-38)
        if self.msgType == enPopupIcon.Icon_Working:
            self.lbPopupBG_InSymbolKeyPad.move(popupX+293, popupY-14)
            self.lbPopupBG_InSymbolLine.move(popupX+319, popupY-28)
            posx = popupX+297
            for item in range(0, 7):
                self.lbPopupBG_InSymbolKeyPad1Line[item].move(posx, popupY-8)
                posx = posx + 7
            posx = popupX + 300
            for item in range(0, 6):
                self.lbPopupBG_InSymbolKeyPad2Line[item].move(posx, popupY)
                posx = posx + 7
            posx = popupX + 297
            for item in range(0, 3):
                self.lbPopupBG_InSymbolKeyPad3Line[item].move(posx, popupY+8)
                if item == 1:
                    posx = posx + 36
                else:
                    posx = posx + 6
        elif self.msgType == enPopupIcon.Icon_Check:
            self.lbPopupBG_InSymbol_Sub.move(popupX+300, popupY-22)
        self.lbPopupMsg.move(popupX, popupY-15)
        self.BtnDispMove()

    def Variable_Init(self):
        self.DefaultFont = enFontInfo.DEF_FONT
        self.DefaultFont.setBold(True)

    def Disp_Background(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.fillColor = QColor(30, 30, 30, 120)
        self.penColor = QColor("#333333")

        self.SIGNALS = popupMessageWidgetSignals()

    def Disp_CenterWindow(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - CommonDef.Win_W) / 2
        y = (screen.height() - CommonDef.Win_H) / 2

        if modeOS.mode_Curr == modeOS.mode_Windows:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((CommonDef.Win_W - POPUP_MESSAGE_W) / 2), y + ((CommonDef.Win_H - POPUP_MESSAGE_H) / 2), CommonDef.popup_Prog_W, POPUP_MESSAGE_H)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.setGeometry(x + ((CommonDef.Win_W - POPUP_MESSAGE_W) / 2), y + ((CommonDef.Win_H - POPUP_MESSAGE_H) / 2), CommonDef.popup_Prog_W, POPUP_MESSAGE_H)

    def Disp_Init(self):
        self.lbPopupBG = PQLabel(self, QRect(0, 0, POPUP_MESSAGE_W, POPUP_MESSAGE_H))
        self.lbPopupBG.setStyleSheet(styleSheet.BACKGROUND_STYLE_03_RADIUS)
        self.lbPopupBG_OutSymbol = PQLabel(self, QRect(0, 0, 100, 100),styleSheet= "background-color:#F7F8F8;border-radius: 50px;")
        if self.msgType == enPopupIcon.Icon_Check:
            self.lbPopupBG_InSymbol = PQLabel(self, QRect(0, 0, 80, 80), text="V", fontSize=40, fontBold=True,styleSheet="color:white;background-color:#009844;border-radius: 40px;")
            self.lbPopupBG_InSymbol_Sub = PQLabel(self, QRect(0, 0, 20, 20), text="", fontSize=40, fontBold=True,styleSheet="color:white;background-color:#009844;border-radius: 40px;")
        elif self.msgType == enPopupIcon.Icon_Warning:
            self.lbPopupBG_InSymbol = PQLabel(self, QRect(0, 0, 80, 80), text="!", fontSize=40, fontBold=True,styleSheet="color:white;background-color:#FC0054;border-radius: 40px;")
        elif self.msgType == enPopupIcon.Icon_Question:
                self.lbPopupBG_InSymbol = PQLabel(self, QRect(0, 0, 80, 80),text="?",fontSize= 40, fontBold = True , styleSheet= "color:white;background-color:#FBB03B;border-radius: 40px;")
        elif self.msgType == enPopupIcon.Icon_Working:
            self.lbPopupBG_InSymbol = PQLabel(self, QRect(0, 0, 80, 80), text="", fontSize=40, fontBold=True,styleSheet="color:white;background-color:#32B7E0;border-radius: 40px;")
            self.lbPopupBG_InSymbolKeyPad = PQLabel(self, QRect(0, 0, 56, 34),styleSheet="color:#32B7E0;background-color:white;border-radius: 8px;")
            self.lbPopupBG_InSymbolLine = PQLabel(self, QRect(0, 0, 3, 15),styleSheet="color:#32B7E0;background-color:white;border-radius: 2px;")
            self.lbPopupBG_InSymbolKeyPad1Line = [PQLabel for i in range(7)]
            self.lbPopupBG_InSymbolKeyPad2Line = [PQLabel for i in range(6)]
            self.lbPopupBG_InSymbolKeyPad3Line = [PQLabel for i in range(3)]
            for item in range(0, 7):
                self.lbPopupBG_InSymbolKeyPad1Line[item] = PQLabel(self, QRect(0, 0, 5, 5),styleSheet="color:#32B7E0;background-color:#32B7E0;border-radius: 2px;")
            for item in range(0, 6):
                self.lbPopupBG_InSymbolKeyPad2Line[item] = PQLabel(self, QRect(0, 0, 5, 5),styleSheet="color:#32B7E0;background-color:#32B7E0;border-radius: 2px;")
            for item in range(0, 3):
                if item == 1:
                    self.lbPopupBG_InSymbolKeyPad3Line[item] = PQLabel(self, QRect(0, 0, 35, 5),styleSheet="color:#32B7E0;background-color:#32B7E0;border-radius: 2px;")
                else:
                    self.lbPopupBG_InSymbolKeyPad3Line[item] = PQLabel(self, QRect(0, 0, 5, 5),styleSheet="color:#32B7E0;background-color:#32B7E0;border-radius: 2px;")
        
        self.lbPopupMsg = PQLabel(self, QRect(0, 0, POPUP_MESSAGE_W, POPUP_MESSAGE_H),self.getMsgTextWrap(self.strMsg))

        self.btnX, self.btnY, self.btnW, self.btnH = 356, 390, 150, 50
        self.btnOk = PQButton(self, QRect(0, 0, self.btnW, self.btnH),fontBold = True,ColorNormal= QColor(29, 49, 75) , ColorPress= QColor(38, 97, 145), ColorText = QColor(255, 255, 255), radius= 25)
        self.btnOk.move(self.btnX, self.btnY)
        self.btnOk.clicked.connect(self.onBtnClickedOk)

        self.btnX, self.btnY = 518, 390
        self.btnCancel = PQButton(self, QRect(0, 0, self.btnW, self.btnH),fontBold = True,ColorNormal= QColor(29, 49, 75) , ColorPress= QColor(38, 97, 145), ColorText = QColor(255, 255, 255), radius= 25)
        self.btnCancel.move(self.btnX, self.btnY)
        self.btnCancel.clicked.connect(self.onBtnClickedCancel)

    def BtnDisp_show(self, btnType):
        self.BtnType = btnType
        self.btnOk.hide()
        self.btnCancel.hide()

        if self.BtnType == enPopupButton.Btn_Ok:
            self.btnOk.setText("OK")
            self.btnOk.show()
        elif self.BtnType == enPopupButton.Btn_Cancel:
            self.btnCancel.setText("CANCEL")
            self.btnCancel.show()
        elif self.BtnType == enPopupButton.Btn_OkCancel:
            self.btnOk.setText("OK")
            self.btnCancel.setText("CANCEL")
            self.btnOk.show()
            self.btnCancel.show()
        elif self.BtnType == enPopupButton.Btn_YesNo:
            self.btnOk.setText("YES")
            self.btnCancel.setText("NO")
            self.btnOk.show()
            self.btnCancel.show()

    def BtnDispMove(self):
        if self.BtnType == enPopupButton.Btn_Ok or self.BtnType == enPopupButton.Btn_Cancel:
            self.btnCancel.move(565, 480)
            self.btnOk.move(565, 480)

        elif self.BtnType == enPopupButton.Btn_OkCancel or self.BtnType == enPopupButton.Btn_YesNo:
            self.btnOk.move(484, 480)
            self.btnCancel.move(646, 480)

    def setMsgText(self, sMsg):
        self.strMsg = self.getMsgTextWrap(sMsg)
        self.lbPopupMsg.setText(self.strMsg)

    def GetValue(self):
        return self.retKey

    def onBtnClickedOk(self):
        self.retKey = enPopupButton.Btn_Ok
        self.SIGNALS.CLOSE.emit()

    def onBtnClickedCancel(self):
        self.retKey = enPopupButton.Btn_Cancel
        self.SIGNALS.CLOSE.emit()

    # 자동 줄바꿈 함수 (언어별 wrapWidth 값 조절이 관건인데...)
    def getMsgTextWrap(self,sMsg, wVal=0):
        if sMsg == "":
            return ""
        else:
            if int(wVal) <= 0:
                isKOR = 0
                isJAP = 0
                for c in sMsg:
                    if ord('\uAC00') <= ord(c) <= ord('\uD7A3'):    # AC00..D7A3  Hangul Syllables  한글
                        isKOR += 1
                    elif ord('\u3040') <= ord(c) <= ord('\u30FF'):  # 3040..309F  Hiragana  일본어 히라가나, 30A0..30FF  Katakana  일본어 카타카나
                        isJAP += 1

                if isKOR == 0 and isJAP == 0:
                    wrapWidth = 30
                else:
                    wrapWidth = 20
            else:
                wrapWidth = wVal
            strMsg = textwrap.wrap(sMsg, width=wrapWidth)
            return '\n'.join(strMsg)