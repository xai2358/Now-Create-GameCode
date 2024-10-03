import os,sys, random
import pygame
import json
import concurrent.futures
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.GameScene import CurrentGameScene
from SystemMain.BaseClass import basescene
from SystemMain.SystemLib import * 
from tkinter import messagebox

class GameScene(basescene) :

    MAX_COL = 35 # 1行の最大文字数
    MAX_ROW = 3 # 1回の表示で表示できる最大行数

    def __init__(self, game_config : dict , file_dir : dict) :
        # ここら辺の変数をまとめたい(希望)
        self.game_config : dict = game_config
        self.file_dir : dict = file_dir

        self.MainPictureDict : BasePicture = BasePicture() # データクラス格納用変数 メインクラスの保存をする
        self.Background : BackgroundPicture = BackgroundPicture() # 表示のためのバッファー変数
        self.TextWindow : TextWindowPicture = TextWindowPicture() # テキストウィンドウクラス
        self.NamePlate : NamePlatePicture = NamePlatePicture() # ネームプレート
        self.StandingPicture : Multiple_Picture = Multiple_Picture() # キャラの立ち絵
        self.Text : TextPicture = TextPicture() # 表示用ピクチャ
        self.textdata : list = [] # テキストデータ群。
        self.Now_read_line : str = '' # 現在読み込んだテキストデータのラインデータ
        self.current_line : int = 0 # 読み込んだテキストデータの行数
        self.textlog : list = [] # 今まで読んだセリフのログ
        self.logline : int = 0 # ログの行数
        self.pressedButton = (False,False,False) # ボタン押し状態
        self.GameSoundData : GameSound = GameSound(game_config, file_dir)
        self.NowSceneStatus : CurrentGameScene = CurrentGameScene.CurrentGameStatus.WAITTING
        #クラス固有の変数にするとシナリオ読み切ったときに再度初めからにできない
        #インスタンス変数にして対応
        self.scenario = []
        self.scene_id = self.file_dir["tmp_Save"]["Scene_ID"]
        self.draw_functions = []
        self.Timer : Timer = Timer()

        # 暫定セーブデータを初期化
        self.file_dir["tmp_Save"]["Scene_ID"] = 0

        # フォントのインスタンスを初期化
        if not(pygame.font.get_init()):
            pygame.font.init()

        return
    
    def __del__(self):
        return
    
    def initialize(self) :
        with open('./File.dat','r', encoding='utf-8') as f:
            line : str = f.readline()
            while line:
                words = line[:-1].split(',')
                self.MainPictureDict.Picutre_Append(words[0],words[1])
                line = f.readline()
        
        with open('./Data/text/Scenario_Data.json', encoding='utf-8') as f:
            self.scenario = json.load(f)

        if self.scene_id == 0:
            self.scene_id += 1
        
        self.current_scene = self.scenario[self.scene_id]
        self.Text_Analyser(self.current_scene)
        self.Timer.set_timer(self.game_config["Automatic_Character_Feed"]) # 5秒にセット
        #self.Timer.timer_start()
        return 0
    
    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        ev = pygame.event.get()
        for event in ev:
            if(((event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[0])):
                self.GameSoundData.voice_Stop()
                self.scene_id += 1
                if self.scene_id >= len(self.scenario):
                    pygame.quit()
                else:
                    self.current_scene = self.scenario[self.scene_id]
                    self.Text_Analyser(self.current_scene)
                    self.Timer.reset()
            elif (event.type == pygame.MOUSEBUTTONUP) and self.pressedButton[2]:
                self.file_dir["tmp_Save"]["Scene_ID"] = self.scene_id
                changer(CurrentGameScene.CurrentGameScene.SAVE)
            elif event.type == QUIT:    
                callback_Quit(not(messagebox.askyesno("確認", "セーブしていない場合はデータは保存されません。終了いたしますか。")))
            self.pressedButton = pygame.mouse.get_pressed() # ここでマウスの状態を保存しているはず…。

        if(self.Timer.check_time()):
            self.GameSoundData.voice_Stop()
            self.scene_id += 1
            if self.scene_id >= len(self.scenario):
                pygame.quit()
            else:
                self.current_scene = self.scenario[self.scene_id]
                self.Text_Analyser(self.current_scene)

        if 'END' in self.current_scene.keys():
            self.GameSoundData.stop_BGM()
            changer(CurrentGameScene.CurrentGameScene.TITLE_SCENE)

        self.Timer.update()
            

    def draw(self, Screen :pygame.surface.Surface) :
        for i in range(len(self.draw_functions)):
                self.draw_functions[i](Screen)

    def Text_Analyser(self, scenario_scene):
        #描画する関数の順番を初期化
        self.draw_functions = []
        # シーンのフェードアウト処理
        FadeOut = False

        if 'background' in scenario_scene.keys():
            word = scenario_scene['background']
            if 'bgFade' in scenario_scene.keys():
                fade = scenario_scene['bgFade']
                if fade == 'OUT':
                    FadeOuter = True
            else:
                fade = "Nomal"
                FadeOuter = False
            self.Background.Regist_order_Picture(word,self.MainPictureDict.get_Picture_Data(word), (0, 0), fade)
            self.draw_functions.append(self.Background.draw)

        if 'Standing_Picture' in scenario_scene.keys():
            self.StandingPicture.clear_Picture()
            word = scenario_scene['Standing_Picture']
            position = scenario_scene["Standing_Position"]
            if 'SP1Fade' in scenario_scene.keys():
                fade = scenario_scene['SP1Fade']
            elif FadeOuter:
                fade = "OUT"
            else:
                fade = "Nomal"
            self.StandingPicture.Regist_order_Picture(word,self.MainPictureDict.get_Picture_Data(word), position, fade)
            
            if 'Standing_Picture2' in scenario_scene.keys():
                word = scenario_scene['Standing_Picture2']
                position = scenario_scene["Standing_Position2"]
                if 'SP2Fade' in scenario_scene.keys():
                    fade = scenario_scene['SP2Fade']
                elif FadeOuter:
                    fade = "OUT"
                else:
                    fade = "Nomal"
                self.StandingPicture.Regist_order_Picture(word,self.MainPictureDict.get_Picture_Data(word), position, fade)

            if 'Standing_Picture3' in scenario_scene.keys():
                word = scenario_scene['Standing_Picture3']
                position = scenario_scene["Standing_Position3"]
                if 'SP3Fade' in scenario_scene.keys():
                    fade = scenario_scene['SP3Fade']
                elif FadeOuter:
                    fade = "OUT"
                else:
                    fade = "Nomal"
                self.StandingPicture.Regist_order_Picture(word,self.MainPictureDict.get_Picture_Data(word), position, fade)
            self.draw_functions.append(self.StandingPicture.draw)
            

        if 'message_box' in scenario_scene:
            word = scenario_scene['message_box_onoff']
            if (word == "OFF" or FadeOut):
                self.TextWindow.change_Display("OFF")
            self.draw_functions(self.TextWindow.draw)

        if 'message' in scenario_scene.keys():
            self.TextWindow.change_Display("ON")
            self.draw_functions.append(self.TextWindow.draw)

            
        if 'name' in scenario_scene.keys():
            word = scenario_scene['name']
            position = scenario_scene['position']
            self.NamePlate.Change_NamePlate(self.MainPictureDict.get_Picture_Data(word), position)
            self.draw_functions.append(self.NamePlate.draw)

        if 'message' in scenario_scene.keys():
            word = scenario_scene['message']
            self.Text.set_Text_Picture(word)
            self.draw_functions.append(self.Text.draw)

        if 'voice' in scenario_scene.keys():
            voice = scenario_scene['voice']
            self.GameSoundData.voice_play(voice)

        if 'BGM' in scenario_scene.keys():
            BGM = scenario_scene['BGM']
            self.GameSoundData.start_BGM(BGM)

        if 'stop_BGM' in scenario_scene.keys():
            self.GameSoundData.stop_BGM()

        if 'SE' in scenario_scene.keys():
            SE = scenario_scene['SE']
            self.GameSoundData.start_EffectSound(SE)

        if 'stop_SE' in scenario_scene.keys():
            self.GameSoundData.stop_EffectSound()

    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,1100,5,1271,38)):
            2+2
        else:
            4+2