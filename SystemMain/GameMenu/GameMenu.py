import os
import json
import pygame
from pygame.locals import *
from SystemMain.TitleScene import TitleScene
from SystemMain.GameScene import GameScene, CurrentGameScene
from SystemMain.LoadScene import LoadScene
from SystemMain.BaseClass import basescene
from SystemMain.Stack import stack
from tkinter import messagebox

class GameMenu(basescene) : 
    def __init__(self, game_config : dict , file_dir : dict):
        self.game_config : dict = game_config
        self.file_dir : dict = file_dir
        self.MenuBar : pygame.Surface.Surface = None
        return
    
    def initialize(self):
        self.MenuBar = pygame.image.load("./Data/image/Option.png").convert_alpha()
        self.MenuBar = pygame.transform.scale(self.MenuBar, (1280,720))
        return 
    
    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
               return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))
        
        return
    
    def draw(self, Screen :pygame.surface.Surface):
        Screen.blit(self.MenuBar, dest=(0,0), area=self.MenuBar.get_rect())
        return
    
    def mouse_event(self, pos):
        return
    