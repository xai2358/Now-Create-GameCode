import os,sys, random
import pygame
import json
import time
#import GameManager
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.GameScene import CurrentGameScene
from SystemMain.BaseClass import basescene
from tkinter import messagebox

# 最初に画像を登録しておくクラス。
# 読み込まれた画像は辞書型で格納
class BasePicture:
    # 初期化
    def __init__(self) : 
        self.Data : dict = {}

    # 画像の登録。辞書に追加しておく、この時、画像の名前を一緒に登録しておくことで、
    # 呼び出しを容易にしておく
    def Picutre_Append(self, PictureName : list[str], Picture_Data : list[str]) :
        self.Data[PictureName] = pygame.image.load(Picture_Data).convert_alpha()

    # 画像のデータを返す関数
    def get_Picture_Data(self, PictureName : list[str]) : 
        return self.Data[PictureName]
    
# 画像を表示させるためのバッファークラス
# 表示画像の登録や再配置、削除、描画などの関数がある。
# 一度登録されているかどうかも確認できるようにすれば、いいのかな？
class BackgroundPicture:
    # 初期化
    def __init__(self):
        #self.Pictuer_Order : list = []
        self.Data = None
        self.Rect = None
        self.Coordinate = None
        self.Alpha = 0
        self.Fade = "Nomal"

    # 表示画像登録関数
    def Regist_order_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface,  Coordinate : tuple, FadeCode : str = "Nomal") :
        self.Data = Picture_Data
        self.Rect = Picture_Data.get_rect()
        self.Coordinate = Coordinate
        self.FadeCode = FadeCode

    def change_Picture_Size(self, size: tuple):
        self.Data = pygame.transform.scale(self.Data,size)
        self.Rect = self.Data.get_rect()

    # 画像の描画
    def draw(self, Screen :pygame.surface.Surface):
        Screen.fill((0, 0, 0))

        if(self.Data != None):
            if(self.FadeCode != "Nomal"):
                Alpha = 0 if self.FadeCode=="IN" else 255
                Alpha = Fader.Fade(Screen, self.FadeCode, self.Data,self.Coordinate, Alpha)
                self.Data.set_alpha(Alpha)
                self.FadeCode = "Nomal"
    
            Screen.blit(self.Data, dest=self.Coordinate, area=self.Rect)
            
# テキストウィンドウクラス
# 決め打ち♡　必要があれば拡張性を増やす
class TextWindowPicture :
    # 初期化
    def __init__(self) : 
        self.TextWindowData = pygame.image.load("./Data/image/Test_message_box.png").convert_alpha()
        self.AutoButton = pygame.image.load("./Data/image/Save_data_Next.png").convert_alpha()
        self.TextWindowRect = self.TextWindowData.get_rect()
        self.TextWindowCoor = (40,500)
        self.Swicher : str = "ON"

    # 表示のオンオフの切り替え
    def change_Display(self, OnOff : str):
        self.str = OnOff

    # 描画
    def draw(self, Screen :pygame.surface.Surface):
        if(self.Swicher == "ON"):
            Screen.blit(self.TextWindowData, dest=self.TextWindowCoor, area=self.TextWindowRect)

# ネームプレートクラス
# 位置などは調整中
class NamePlatePicture :
    # 初期化
    def __init__(self) : 
        self.NamePlateData = {}
        self.NamePlateRect = {}
        self.NamePlatePosition = (50, 480)

    # データの切り替え
    def Change_NamePlate(self, Picture_Data : pygame.surface.Surface, Position) :
        self.NamePlateData = Picture_Data
        self.NamePlateRect = self.NamePlateData.get_rect()
        if Position == "left":
            self.NamePlatePosition = (50,480)
        elif Position == "middle":
            self.NamePlatePosition = (480, 480)
        elif Position == "right":
            self.NamePlatePosition = (1050,480)

    # 表示のオンオフの切り替え
    def change_Display(self, OnOff : str):
        return

    # 描画
    def draw(self, Screen : pygame.surface.Surface):
        if(self.NamePlateData != None):
            Screen.blit(self.NamePlateData, dest=self.NamePlatePosition, area=self.NamePlateRect)

class Multiple_Picture:
    # 初期化
    def __init__(self):
        #self.Pictuer_Order : list = []
        self.Data : list = []
        self.Rect : list = []
        self.Coordinate : list = []
        self.Alpha : list = []
        self.FadeCodelist : list = []

    def clear_Picture(self):
        self.Data = []
        self.Rect = []
        self.Coordinate = []
        self.Alpha = []
        self.FadeCodelist = []

    # 表示画像登録関数
    # 過去の登録の有無に限らず一旦画像を消して
    # 再登録させる。
    def Regist_order_Picture(self, Picture_Name: list[str], Picture_Data : pygame.surface.Surface, Position : list[str], Fadecode :str = "Nomal") :
        pict_height = Picture_Data.get_height()
        pict_width = Picture_Data.get_width()
        self.Data.append(Picture_Data)
        self.Rect.append(Picture_Data.get_rect())
        self.FadeCodelist.append(Fadecode)
        if Fadecode == "IN":
            self.Alpha.append(0)
        else :
            self.Alpha.append(255)
        #self.FadeCodelist.append(Fadecode)
        #キャラごとに下駄を履かせられるよい方法を探す
        if Picture_Name[0:3] != "mio" :
            pict_height += 160

        if Position == "left":
            self.Coordinate.append((280-pict_width//2,720+660-pict_height))
        elif Position == "m_left":
            self.Coordinate.append((460-pict_width//2,720+660-pict_height))
        elif Position == "middle":
            self.Coordinate.append((640-pict_width//2, 720+660-pict_height))
        elif Position == "m_right":
            self.Coordinate.append((820-pict_width//2,720+660-pict_height))
        elif Position == "right":
            self.Coordinate.append((1000-pict_width//2,720+660-pict_height))
        
    
    def Regist_Pictures(self, PicturName: list[str], Picture_Data : pygame.surface.Surface, Coordinate : tuple, Fadecode : str = "Nomal"):
        self.Data.append(Picture_Data)
        self.Rect.append(Picture_Data.get_rect())
        self.Coordinate.append(Coordinate)
        self.Alpha.append(255)
        self.FadeCodelist.append(Fadecode)

    # 画像の描画
    def draw(self, Screen :pygame.surface.Surface):
        if(len(self.Data) != 0):
            for i in reversed(range(len(self.Data))) :
                if self.FadeCodelist[i] != "Nomal":
                    self.Alpha[i] = Fader.Fade(Screen, self.FadeCodelist[i], self.Data[i],self.Coordinate[i], self.Alpha[i])
                    self.Data[i].set_alpha(self.Alpha[i])
                    
                    self.FadeCodelist[i] = "Nomal"
                Screen.blit(self.Data[i], dest=self.Coordinate[i], area=self.Rect[i])

class TextPicture :
    
    MAX_COL = 35 # 1行の最大文字数
    MAX_ROW = 3 # 1回の表示で表示できる最大行数

    def __init__(self):
        self.font_kinds = pygame.font.Font("./Data/font/ShipporiMincho-Regular.ttf", 32)
        self.TextData : list[pygame.surface.Surface] = []
        self.TextRect : list[pygame.rect.Rect] = []
        self.TextCoor : list[tuple] = []

    def set_font(self, font_dir:list[str], font_size) :
        self.font_kinds = pygame.font.Font(font_dir, font_size)

    def set_Text_Picture(self, text:list[str]):
        self.TextData = []
        self.TextRect = []
        self.TextCoor = []
        text_index = 0
        x = 0
        y = 0
        while text_index < len(text):
            if text_index + 2 < len(text):
                if (text[text_index] == "/") & (text[text_index+1] == "b") & (text[text_index+2] == "r"):
                    y += 1
                    x = 0
                    text_index = text_index + 3
            
            self.TextData.append(self.font_kinds.render(text[text_index], True, (0,0,0)))
            self.TextRect.append(self.TextData[-1].get_rect())
            self.TextCoor.append((60+32*x, 520+47*y))

            text_index += 1
            x += 1

            if x % TextPicture.MAX_COL == 0 : 
                y += 1
                x = 0
        
    def draw(self, Screen : pygame.surface.Surface):
        if(len(self.TextData) != 0):
            for i in range(len(self.TextData)) :
                Screen.blit(self.TextData[i], dest=self.TextCoor[i], area=self.TextRect[i])

class GameSound :
    CurrentVoice = ""

    def __init__(self, game_config : dict , file_dir : dict):
        self.game_config : dict = game_config
        self.file_dir : dict = file_dir
        self.BGM_Channel = pygame.mixer.Channel(0)
        self.Voice_Channel = pygame.mixer.Channel(1)
        self.Effect_Channel = pygame.mixer.Channel(2)

    def start_BGM(self, BGMData : str):
        if not self.BGM_Channel.get_busy():
            self.BGM_Channel.set_volume(self.game_config["SoundVolume"])
            self.BGM_Channel.play(pygame.mixer.Sound(BGMData), -1)
    
    def stop_BGM(self):
        if self.BGM_Channel.get_busy():
            self.BGM_Channel.stop()

    def start_EffectSound(self, EffectData : str):
        if not self.Effect_Channel.get_busy():
            self.Effect_Channel.set_volume(self.game_config["EffectVolume"])
            self.Effect_Channel.play(pygame.mixer.Sound(EffectData))

    def stop_EffectSound(self):
        if self.Effect_Channel.get_busy():
            self.Effect_Channel.stop()

    def voice_play(self, VoiceData : str):
        if VoiceData != self.CurrentVoice:
            self.Voice_Channel.set_volume(self.game_config["VoiceVolume"])
            self.Voice_Channel.play(pygame.mixer.Sound(VoiceData))
            self.CurrentVoice = VoiceData

    def voice_Stop(self):
        if self.Voice_Channel.get_busy():
            self.Voice_Channel.stop()

class Fader:
    def Fade(Screen :pygame.Surface, state : str , picture : pygame.Surface, Coordinate : tuple, Alpha : int):
        clock = pygame.time.Clock()
        running = True

        screen_copy = Screen.copy()

        while running :
            for event in pygame.event.get():
                if(event.type == pygame.MOUSEBUTTONUP):
                    if state == "IN":
                        Alpha = 255
                    elif state == "OUT":
                        Alpha = 0
            
            Screen.blit(screen_copy, (0,0))

            # フェードイン処理
            if state == "IN":
                if Alpha < 255:
                    Alpha = min(Alpha + 5, 255)
                else:
                    running = False # フェードイン完了
            # フェードアウト処理
            elif state == "OUT":
                if Alpha > 0:
                    Alpha = max(Alpha-5, 0)
                else:
                    running = False # フェードアウト完了
            
            # アルファ値を適用して画像を描画
            picture.set_alpha(Alpha)
            Screen.blit(picture, Coordinate)

            # 描画処理
            pygame.display.update()
            clock.tick(30)

        return Alpha
    
class Timer : 
    def __init__(self):
        self.Now_Time : float = 0
        self.finish_time : int = 0 #second
        self.totalTime : int = 0
        self.game_clock = pygame.time.Clock()
        self.OnOff : str = "OFF"
        self.fps = 30

    def set_timer(self, finish_time : int):
        self.finish_time = finish_time
        self.totalTime = finish_time * 1000 # millisecond -> second

    def Turn_Timer(self, OnOff : str = "ON"):
        self.OnOff = OnOff
        self.totalTime =  self.finish_time * 1000 # millisecond -> second

    def timer_start(self):
        self.game_clock.tick(self.fps)
        self.start = self.game_clock.get_time()

    def update(self):
        if(self.OnOff == "ON"):
            self.game_clock.tick(self.fps)
            self.Now_Time = self.game_clock.get_time()
            self.totalTime = max(self.totalTime - self.Now_Time, 0)
        
        print("totalTime:" + str(self.totalTime) + "  end:" + str(self.Now_Time))

    def check_time(self):
        if(self.totalTime == 0): # millisecond -> second
            self.totalTime = self.finish_time * 1000 # 再設定
            return True
        else:
            return False
        
    def reset(self):
        self.totalTime = self.finish_time * 1000