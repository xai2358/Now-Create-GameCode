import os
import json
import math
import pygame
import datetime
from tkinter import messagebox
from pygame.locals import *
from SystemMain.GameScene import CurrentGameScene
from SystemMain.MouseClass import MouseClass
from SystemMain.BaseClass import basescene
from SystemMain.SystemLib import *

class SaveScene(basescene) :

    _PREVIEW : int = -1
    _NEXT : int = 1
    _MAX_DISPLAY_SAVE_DATA :int = 4

    def __init__(self, game_config : dict , file_dir : dict) :
        ############################################ 変数初期化 #############################################################
        self.game_config : dict = game_config
        self.file_dir : dict = file_dir

        self.Background : BackgroundPicture = BackgroundPicture()
        self.Background.Regist_order_Picture("Save", pygame.image.load("./Data/image/Load_Scene.png").convert_alpha(), (0,0))

        # ################################## #
        # ボタン用変数                        #
        # 0 : Next Button                    #
        # 1 : Preview Button                 #
        # 2 : Home Button                    #
        # ################################## #
        self.Button : Multiple_Picture = Multiple_Picture()

        self.story_len : list[int] = []
        self.date : list[str] = []
        self.Save_data_Name : list[pygame.surface.Surface] = []
        self.nextState : CurrentGameScene.SaveState = None
        self.story_len_buffer : list[pygame.surface.Surface] = []
        self.date_buffer : list[pygame.surface.Surface] = []
        self.page_Num : pygame.surface.Surface = None
        self.font_kinds = pygame.font.Font("./Data/font/ShipporiMincho-Regular.ttf", 32)
        ######################################################################################################################    

    def initialize(self) :

        self.Background.change_Picture_Size((self.game_config["WindowWidth"],self.game_config["WindowHeight"]))

        self.Button.Regist_Pictures("Next", pygame.image.load("./Data/image/Save_data_Next.png").convert_alpha(), (980,660))
        self.Button.Regist_Pictures("Preview", pygame.image.load("./Data/image/Save_data_preview.png").convert_alpha(), (120,660))
        self.Button.Regist_Pictures("Home", pygame.image.load("./Data/image/return_to_Home.png").convert_alpha(), (1100,5))

        with open('./Data/save/savedata.json', encoding='utf-8') as jsonfile:
            self.save_data_constellation = json.load(jsonfile)

        self.save_position = 0
        self.data_position = 0

        self.page_Num = self.font_kinds.render(str(self.save_position+1) + "/4", True, (0,0,0))

        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA):
            self.story_len.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Scene_ID"])
            self.date.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Save_Date"])  

        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA):
            self.Save_data_Name.append(self.font_kinds.render("Save Data" + str(4*self.save_position + i + 1), True, (0,0,0)))
            if self.date[i] == "yyyy-mm-dd" :
                self.date_buffer.append(self.font_kinds.render("No Data", True, (0,0,0)))
            else:
                self.date_buffer.append(self.font_kinds.render(self.date[i], True, (0,0,0)))

    def update(self, Screen : pygame.surface.Surface, next_game_scene ,  changer, callback_Quit) :
        ############################################### セーブ内容の表示 #####################################################
        self.date_buffer.clear()
        self.Save_data_Name.clear()

        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA):
            self.Save_data_Name.append(self.font_kinds.render("Save Data" + str(4*self.save_position + i + 1), True, (0,0,0)))
            if self.date[i] == "yyyy-mm-dd" :
                self.date_buffer.append(self.font_kinds.render("No Data", True, (0,0,0)))
            else:
                self.date_buffer.append(self.font_kinds.render(self.date[i], True, (0,0,0)))

        self.page_Num = self.font_kinds.render(str(self.save_position+1) + "/4", True, (0,0,0))
        #####################################################################################################################

        ############################################### マウスの挙動 #####################################################
        for event in pygame.event.get():
            button = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP:
                self.nextState = self.mouse_event(pygame.mouse.get_pos)
                if(self.nextState == CurrentGameScene.SaveState.RETRUN):
                    changer(CurrentGameScene.CurrentGameScene.RETURN)
                    return
                elif(self.nextState == CurrentGameScene.SaveState.PREVIEWTOSAVEDATA):
                    self.load_anothor_savedata(SaveScene._PREVIEW)
                    return
                elif(self.nextState == CurrentGameScene.SaveState.NEXTTOSAVEDATA):
                    self.load_anothor_savedata(SaveScene._NEXT)
                    return
                elif(self.nextState == CurrentGameScene.SaveState.SAVE):
                    self.Saveing_Data()
                    return
                else:
                    return
            elif event.type == QUIT:                          # 終了ボタンを押した場合終了 セーブ警告あり
                callback_Quit(not(messagebox.askyesno("確認", "終了いたしますか。")))
        #####################################################################################################################

        return 0
    
    def draw(self, Screen:pygame.surface.Surface) : 
        ############################### 背景とボタンの描画 ###################################################
        self.Background.draw(Screen)
        self.Button.draw(Screen)

        Screen.blit(self.page_Num, dest=(630,660), area=self.page_Num.get_rect())
        #####################################################################################################
        
        ####################################### 文字の描画 ###################################################
        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA//2):
            for j in range(SaveScene._MAX_DISPLAY_SAVE_DATA//2):
                Screen.blit(self.Save_data_Name[i*2+j], dest=(290+j*540, 150+i*320), area=self.Save_data_Name[i*2+j].get_rect())
                Screen.blit(self.date_buffer[i*2+j], dest=(320+j*540, 250+i*320), area=self.date_buffer[i*2+j].get_rect())
        #####################################################################################################
        return 0   

    def mouse_event(self, pos):

        if(MouseClass.MouseClass.isMousePositionChecker(pos,1100,5,1271,38)):
            # Title画面に戻る
            print("戻るんです")
            return CurrentGameScene.SaveState.RETRUN
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,120,660,376,710)):
            # 前へ
            print("前へ戻る")
            return CurrentGameScene.SaveState.PREVIEWTOSAVEDATA
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,980,660,1236,710)):
            # 次へ
            print("次へ進む")
            return CurrentGameScene.SaveState.NEXTTOSAVEDATA
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,164,56,607,306)):
            self.data_position = 1
            print("セーブデータ" + str(4*self.save_position + self.data_position))
            return CurrentGameScene.SaveState.SAVE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,696,56,1142, 306)):
            self.data_position = 2
            print("セーブデータ" + str(4*self.save_position + self.data_position))
            return CurrentGameScene.SaveState.SAVE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,164,379, 608,626)):
            self.data_position = 3
            print("セーブデータ" + str(4*self.save_position + self.data_position))
            return CurrentGameScene.SaveState.SAVE
        elif(MouseClass.MouseClass.isMousePositionChecker(pos,698,379,1142,626)):
            self.data_position = 4
            print("セーブデータ" + str(4*self.save_position + self.data_position))
            return CurrentGameScene.SaveState.SAVE
        else:
            return CurrentGameScene.CurrentGameScene.NONE_SCENE
    
    def load_anothor_savedata(self, IncrementAndDecrease : int) :
        self.story_len.clear()
        self.date.clear()

        self.save_position += IncrementAndDecrease

        if (self.save_position >= 4) : 
            self.save_position = 3
        elif(self.save_position <= -1):
            self.save_position = 0

        ############################################ セーブデータ表示の更新 #########################################################
        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA):
            self.story_len.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Scene_ID"])
            self.date.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Save_Date"])  
       ######################################################################################################################

        return
    
    def Saveing_Data(self):

        if self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Save_Date"]  == "yyyy-mm-dd" :
            if messagebox.askyesno("確認", "セーブデータ"+ str(4*self.save_position + self.data_position) + "に保存しますか。") :
                self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Save_Date"] = format(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST')), '%Y-%m-%d')
                self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Scene_ID"] = self.file_dir["tmp_Save"]["Scene_ID"]

                save_data_num = 0
                for i in range(self.save_data_constellation["Fandamental_data"]["MAX_SAVE_DATA"]):
                    if self.save_data_constellation["save_data" + str(i+1)]["Save_Date"] != "yyyy-mm-dd":
                        save_data_num += 1
        
                self.save_data_constellation["Fandamental_data"]["save_data_num"] = save_data_num

                with open('./Data/save/savedata.json', encoding="utf-8", mode="w") as jsonfile:
                    json.dump(self.save_data_constellation, jsonfile, indent=2, ensure_ascii=False)    

                messagebox.showinfo('セーブ完了', "セーブデータ"+ str(4*self.save_position + self.data_position) + "に保存しました。")
        else :
            if messagebox.askyesno("確認", "セーブデータ"+ str(4*self.save_position + self.data_position) + "には既にデータが保存されています。\n 保存しますか。") :
                self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Save_Date"] = format(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST')), '%Y-%m-%d')
                self.save_data_constellation["save_data"+ str(4*self.save_position + self.data_position)]["Scene_ID"] = self.file_dir["tmp_Save"]["Scene_ID"]

                save_data_num = 0
                for i in range(self.save_data_constellation["Fandamental_data"]["MAX_SAVE_DATA"]):
                    if self.save_data_constellation["save_data" + str(i+1)]["Save_Date"] != "yyyy-mm-dd":
                        save_data_num += 1
        
                self.save_data_constellation["Fandamental_data"]["save_data_num"] = save_data_num

                with open('./Data/save/savedata.json', encoding="utf-8", mode="w") as jsonfile:
                    json.dump(self.save_data_constellation, jsonfile, indent=2, ensure_ascii=False)    

                messagebox.showinfo('セーブ完了', "セーブデータ"+ str(4*self.save_position + self.data_position) + "に保存しました。")

        with open('./Data/save/savedata.json', encoding='utf-8') as jsonfile:
            self.save_data_constellation = json.load(jsonfile)

        self.story_len.clear()
        self.date.clear()

        for i in range(SaveScene._MAX_DISPLAY_SAVE_DATA):
            self.story_len.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Scene_ID"])
            self.date.append(self.save_data_constellation["save_data" + str(4*self.save_position + i + 1)]["Save_Date"])  