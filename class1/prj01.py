######################匯入模組######################
import pygame  # 匯入 pygame 模組
import sys  # 匯入 sys 模組

######################初始化######################
pygame.init()  # 初始化 pygame
width = 640  # 設定視窗寬度
height = 320  # 設定視窗高度

######################建立視窗及物件######################
screen = pygame.display.set_mode((width, height))  # 建立遊戲視窗
pygame.display.set_caption("My  Game")  # 設定視窗標題

######################建立畫布######################
bg=pygame.Surface((width, height))  # 建立背景畫布
bg.fill((79,149,218))  # 設定背景顏色

######################繪製圓形######################
pygame.draw.circle(bg, (0, 0, 255), (200, 100), 30, 0)  # 在背景上畫一個藍色圓形
pygame.draw.circle(bg, (0, 0, 255), (400, 100), 30, 0)  # 在背景上畫一個藍色圓形

pygame .draw.rect(bg, (0, 255, 0), [270, 130,60,40], 5)  # 在背景上畫一個綠色矩形

pygame.draw.ellipse(bg, (255, 0, 0), [130, 160,60,35], 5)  # 在背景上畫一個紅色橢圓形
pygame.draw.ellipse(bg, (255, 0, 0), [400, 160,60,35], 5)  # 在背景上畫一個紅色橢圓形

pygame.draw.line(bg, (255, 0, 255), (280, 220), (320, 220), 3)  # 在背景上畫一條黃色直線
######################循環偵測######################
while True:
    for event in pygame.event.get():  # 取得所有遊戲事件
        if event.type == pygame.QUIT:  # 判斷是否按下關閉視窗
            sys.exit()  # 結束程式

    screen.blit(bg, (0, 0))  # 將背景顯示到視窗上
    pygame.display.update()  # 更新畫面
 
