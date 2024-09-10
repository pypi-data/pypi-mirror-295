# OS Check
class modeOS():
    mode_Windows = 0
    mode_Linux = 1
    mode_Curr = mode_Linux


# Resource Folder Path
class DirPathDef():
    PATH_RESOURCE = 0
    PATH_IMAGE = 1


class enSoundType():
    EN_BUTTON_SOUND_TYPE = 0
    EN_START_SOUND_TYPE = 1
    EN_NOTICE_SOUND_TYPE = 2
    EN_SHUTDOWN_SOUND_TYPE = 3
    EN_ERROR_SOUND_TYPE = 3


class enPopupButton():
    Btn_None = 0
    Btn_Ok = 1
    Btn_Cancel = 2
    Btn_Ignore = 4
    Btn_OkCancel = 10
    Btn_OkCancelIgnore = 11
    Btn_ThreadEnd = 20
    Btn_ThreadCancel = 21
    Btn_YesNo = 30

class enNumpadMode():
    EN_MODE_NONE = 0
    EN_MODE_TIME = 1
    EN_MODE_TEMP = 2
    EN_MODE_SPEED = 3
    EN_MODE_VOLUME = 4
    EN_MODE_COLLECT = 5
    EN_MODE_CYCLE = 6

class styleSheet():
    #백그라운드 스타일
    BACKGROUND_STYLE_01 = """
                 QLabel {
                     color : black;
                     background-color: #F7F8F8;
                     border: 2px solid #A3A3A3;
                     border-radius: 0px;
                 }
             """
    BACKGROUND_STYLE_02 = """
                 QLabel {     
                     background-color: #F7F8F8;                
                     color : #A7A8A8;
                 }
             """
    #에디트박스 스타일
    EDIT_STYLE_01 = """
                 QLabel {
                     color : black;
                     background-color: white;
                     border: 2px solid black;
                     border-radius: 5px;
                 }
             """
    #원형 스타일
    CIRCLE_STYLE_01 = """
                 QLabel {
                     color : white;
                     background-color: #E7E8E8;
                     border-radius: 12px;
                 }
             """
    #키보드 스타일
    KEYBOARD_STYLE_01 = """
                 QLabel {
                     color : black;
                     background-color: #F2F2F2;
                     border: 1px solid #A3A3A3;
                     border-radius: 0px;
                 }
                 """
    KEYBOARD_STYLE_02 = """
                 QLabel {
                     color : black;
                     background-color: #e5ffff;
                     border: 1px solid #A3A3A3;
                     border-radius: 0px;
                 }
                 """