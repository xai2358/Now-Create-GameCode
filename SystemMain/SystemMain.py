import os
import json
import pygame
from pygame.locals import *
from SystemMain.TitleScene import TitleScene
from SystemMain.GameScene import GameScene, CurrentGameScene
from SystemMain.GameMenu import GameMenu
from SystemMain.LoadScene import LoadScene
from SystemMain.BaseClass import basescene
from SystemMain.SaveScene import SaveScene
from SystemMain.SystemLib import *
from SystemMain.Stack import stack
from tkinter import messagebox

ROOTPATH = os.path.dirname(os.path.abspath(__file__))
CFGPATH = os.path.dirname(ROOTPATH)

class SystemMain:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        
    def __del__(self):
        return 
    
    def initialize(self):
        with open('./Setting.json', encoding='utf-8') as jsonfile:
            self.game_config = json.load(jsonfile)
        with open('./File.json', encoding='utf-8') as jsonfile2:
            self.file_dir = json.load(jsonfile2)

        self.screen = pygame.display.set_mode((self.game_config["WindowWidth"],
                                               self.game_config["WindowHeight"]))  # 画面サイズ設定
        pygame.display.set_caption(self.game_config["TitleName"])                   # ウィンドウタイトル設定
        
        self.NowGameState : CurrentGameScene.GameState = CurrentGameScene.GameState.NOMAL


        # 親クラスのシーンの変数をインスタンス
        self.game_state : basescene = None
        self.game_stack : stack.MyStack = stack.MyStack()

        # 子クラスを親クラスのインスタンスに代入。
        # これにより、子クラスを入れ替えることが可能。
        self.game_state = TitleScene.TitleScene(self.game_config, self.file_dir)
        self.game_state.initialize()
        return True

    def main_loop(self):
        self.running = True
        self.current_game_scene = CurrentGameScene.CurrentGameScene.TITLE_SCENE
        self.next_game_scene = CurrentGameScene.CurrentGameScene.NONE_SCENE
        while(self.running):
            self.clock.tick(30)
            if self.NowGameState == CurrentGameScene.GameState.NOMAL:
                self.game_state.update(self.screen, self.current_game_scene, self.Changer_Scene, self.finalize)
            else:
                1+1
            
            #self.screen.fill((0,0,0,))                          # 背景色(ここをうまくやればフェードイン、フェードアウト作れる?)
            self.game_state.draw(self.screen)
            #print(self.clock.get_fps())

            pygame.display.flip()                             # 画面更新 必ず必要

        pygame.quit()

    def finalize(self, Finish : bool = True):
        self.running = Finish

    
    def Changer_Scene(self, next_scene : CurrentGameScene.CurrentGameScene = CurrentGameScene.CurrentGameScene.NONE_SCENE,now_scene: CurrentGameScene.CurrentGameScene = CurrentGameScene.CurrentGameScene.NONE_SCENE):
        
        if(next_scene ==CurrentGameScene.CurrentGameScene.TITLE_SCENE): # タイトルシーンの処理
            self.game_state = TitleScene.TitleScene(self.game_config, self.file_dir)
            self.game_state.initialize()
            self.game_stack.all_remove()
        elif(next_scene ==CurrentGameScene.CurrentGameScene.INTRO): # タイトルシーンの処理
            self.game_stack.push(self.game_state)
            self.game_state = GameScene.GameScene(self.game_config, self.file_dir)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.LOAD) :
            self.game_stack.push(self.game_state)
            self.game_state = LoadScene.LoadScene(self.game_config, self.file_dir)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.SAVE) :
            self.game_stack.push(self.game_state)
            self.game_state = SaveScene.SaveScene(self.game_config, self.file_dir)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.SETTING) :
            self.game_stack.push(self.game_state)
            self.game_state = GameMenu.GameMenu(self.game_config, self.file_dir)
            self.game_state.initialize()
        elif(next_scene == CurrentGameScene.CurrentGameScene.RETURN) :
            self.game_state = self.game_stack.pop()
        elif(next_scene == CurrentGameScene.CurrentGameScene.QUIT) :
            self.running = not(messagebox.askyesno("確認", "セーブしていない場合はデータは保存されません。終了いたしますか。"))