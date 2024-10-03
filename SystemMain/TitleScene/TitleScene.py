import os
import math
import pygame
from pygame.locals import *
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.GameScene import GameScene,CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.SystemLib import *
from tkinter import messagebox

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
FFGPATH = os.path.dirname(ROOTPATH)
CFGPATH = os.path.dirname(os.path.dirname(ROOTPATH))

class TitleScene(basescene) :
    def __init__(self, game_config : dict , file_dir : dict):
        self.game_config : dict = game_config
        self.file_dir : dict = file_dir
        self.time :list = []
        self.Button_Data : list = []
        self.rects_Button : list = []
        self.Next_Scene_Instance : basescene = None
        self.Background : BackgroundPicture = BackgroundPicture()
        self.Button : Multiple_Picture = Multiple_Picture()

    def initialize(self):
        self.Background.Regist_order_Picture("TitleScene", pygame.image.load(self.file_dir["Title_Scene"]["Title"]).convert_alpha(), (0,0))
        self.Background.change_Picture_Size((self.game_config["WindowWidth"],self.game_config["WindowHeight"]))

        i = 0
        for data in ["Start", "load", "config", "end"]:
            self.Button.Regist_Pictures(data, pygame.image.load(self.file_dir["Title_Scene"][data]).convert_alpha(), (34 ,382+60*i), "Nomal")
            i += 1
        
        pygame.mixer.music.load(self.file_dir["Title_Scene"]["BGM"]) # BGM読み込み
        pygame.mixer.music.set_volume(self.game_config["SoundVolume"])

    def draw(self, Screen :pygame.surface.Surface):
        if(not pygame.mixer.music.get_busy()) :             #これでBGMがなっているかの判定
                pygame.mixer.music.play(-1)

        self.Background.draw(Screen)
        self.Button.draw(Screen)

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        
        for event in pygame.event.get():
            button = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP:
               #nanka = self.mouse_event(pygame.mouse.get_pos)
               changer(self.mouse_event(pygame.mouse.get_pos))
               return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))
        return 
    
    def trans_update(self, Now_game_State:CurrentGameScene.GameState):
        if Now_game_State == CurrentGameScene.GameState.SCENE_FADEIN:
            2+2
        elif Now_game_State == CurrentGameScene.GameState.SCENE_FADEOUT:
            2+2

    def mouse_event(self, pos):
        if(MouseClass.MouseClass.isMousePositionChecker(pos,34,382,355,415)):
            print("Selected Start Button")
            pygame.mixer.music.stop()
            return CurrentGameScene.CurrentGameScene.INTRO
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,34,442,355,475)):
            print("Selected load Button")
            return CurrentGameScene.CurrentGameScene.LOAD
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,34,502,355,535)):
            print("Selected Config Button")
            return CurrentGameScene.CurrentGameScene.SETTING
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,34,562,355,595)):
            print("Selected end Button")
            return CurrentGameScene.CurrentGameScene.QUIT
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE