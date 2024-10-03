from enum import Enum

class CurrentGameScene(Enum):
    NONE_SCENE = 0
    TITLE_SCENE = 1
    INTRO = 100
    LOAD = 800
    SETTING = 801
    GAMEMENU = 802
    SAVE = 803
    QUIT = 900
    RETURN = 1000

class CurrentTitleStatus(Enum):
    WAIT_TIME = 0 # 入力待ち状態(待機状態)
    TRANSITION_STATE = 100 # 遷移状態(次のシーンに移行するための準備状態)
    GOTO_NEXT_SCENE = 200 # 次のシーンに飛ぶ

class CurrentGameStatus(Enum):
    WAITTING = 100  # 読んでない状態（文面を表示しているか、何も表示されていない状態、今後状態を分けるかも）
    READING = 200   # 読み発生状態 (文面表示中)
    LOADING = 300   # データ読み込み中

class LoadState(Enum):
    RETRUN = 100
    NEXTTOSAVEDATA = 200
    PREVIEWTOSAVEDATA = 300
    LOAD = 400

class SaveState(Enum):
    RETRUN = 100
    NEXTTOSAVEDATA = 200
    PREVIEWTOSAVEDATA = 300
    SAVE = 400

class GameState(Enum):
    NOMAL = 1
    SCENE_FADEOUT = 100
    SCENE_FADEIN = 200
