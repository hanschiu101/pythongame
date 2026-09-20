######################載入套件/ import packages######################
import pygame  # 匯入 pygame 模組
# pygame 是製作遊戲和多媒體程式的套件

import sys  # 匯入 sys 模組
# sys 可以用來結束程式

######################物件類別/ object class######################
class Brick:
    # 建立一個磚塊類別

    def __init__(self,x,y,width,height,color):
        # 建立磚塊時設定磚塊的資料

        self.rect=pygame.Rect(x,y,width,height)
        # 建立磚塊的矩形

        self.color = color
        # 設定磚塊的顏色

        self.hit=False
        # 設定磚塊一開始沒有被打到

    def draw(self,display_area):
        # 建立繪製磚塊的函式
        # display_area 代表要繪製磚塊的畫面

        if  not self.hit:
            # 判斷磚塊是否還沒有被打到

            pygame.draw.rect(display_area,self.color,self.rect)
            # 將磚塊繪製到遊戲畫面上

######################定義函式區/ define functions######################

######################初始化設定/ initialize settings######################
pygame.init()  # 初始化 pygame
# 開始使用 pygame 的功能

######################載入圖片/ load images######################

######################遊戲視窗設定/ game window settings######################
bg_x=800
# 設定遊戲視窗的寬度

bg_y=600
# 設定遊戲視窗的高度

bg_size=(bg_x,bg_y)
# 設定遊戲視窗的大小

pygame.display.set_caption("打磚塊遊戲")  # 設定視窗標題
# 將遊戲視窗的標題設定為打磚塊遊戲

screen = pygame.display.set_mode(bg_size)  # 建立遊戲視窗
# 建立遊戲視窗並使用設定好的大小

######################磚塊設定/ brick settings######################

######################顯示文字設定/ text display settings######################

######################底板設定/ paddle settings######################

######################球設定/ ball settings######################

######################遊戲結束設定/ game over settings######################

######################主程式/ main program######################
while True:
    # 持續執行遊戲主程式

    for event in pygame.event.get():  # 取得所有遊戲事件
        # 檢查遊戲中發生的事件

        if event.type == pygame.QUIT:  # 判斷是否按下關閉視窗
            # 如果按下關閉視窗

            sys.exit()  # 結束程式 
            # 結束遊戲程式

    pygame.display.update()  # 更新畫面
    # 更新遊戲畫面
