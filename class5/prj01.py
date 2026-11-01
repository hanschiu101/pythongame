###################### 載入套件 ######################
import pygame  # 載入 pygame 套件，用來製作遊戲
import sys     # 載入 sys 套件，用來處理系統相關功能

###################### 物件類別 ######################
# 定義遊戲中會使用到的物件類別
# 例如：主角、敵人、障礙物等
class Player:
    def __init__(self, x, y,width, height, color):
        self.rect = pygame.Rect(x, y, width, height)  # 設定主角的矩形範圍
        self.color = color  # 設定主角的顏色
        self.speed = 5  # 設定主角的移動速度
    def draw(self,display_area):
        pygame.draw.rect(display_area, self.color, self.rect)
          # 在指定的顯示區域上繪製主角
    def move(self, direction,bg_x):
        self.rect.x += direction * self.speed  # 根據方向移動主角的 x 座標
        if self.rect.right < 0:  # 如果主角超出左邊界
            self.rect.left = bg_x  # 將主角的 x 座標設為左邊界
        elif self.rect.left > bg_x:  # 如果主角超出右邊界
            self.rect.right = 0 # 將主角的 x 座標設為右邊界
###################### 初始化設定 ######################
pygame.init()  # 初始化 pygame 所有模組
FPS = pygame.time.Clock()  # 建立時鐘物件，用來控制遊戲更新速度

###################### 遊戲視窗設定 ######################
# 設定遊戲視窗的大小、標題與背景顏色
bg_x=400
bg_y=600
bg_size=(bg_x,bg_y)
pygame.display.set_caption("Doodle Jump")  # 設定遊戲視窗標題
screen = pygame.display.set_mode(bg_size)  # 設定遊戲視窗大小
###################### 主角設定 ######################
# 設定主角的外觀、位置、移動速度等屬性
player_w=30
player_h=30
player_x=(bg_x-player_w)//2
player_y=bg_y-player_h-50
player=Player(player_x,player_y,player_w,player_h,(0,255,0))  # 建立主角物件，設定位置、大小與顏色
###################### 主程式 ######################
# 撰寫遊戲主要執行內容
# 例如：遊戲迴圈、事件偵測、畫面更新等
while True:
    FPS.tick(60)  # 設定遊戲更新速度為每秒 60 次
    screen.fill((0, 0, 0))  # 將遊戲視窗填滿黑色背景
    keys = pygame.key.get_pressed()  # 取得目前按下的按鍵狀態
    if keys[pygame.K_LEFT]:  # 如果按下左方向鍵
        player.move(-1,bg_x)  # 主角向左移動
    if keys[pygame.K_RIGHT]:  # 如果按下右方向鍵
        player.move(1,bg_x)  # 主角向右移動
    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:  # 如果事件類型是退出遊戲
            sys.exit()  # 結束程式
    player.draw(screen)  # 在遊戲視窗上繪製主角
    pygame.display.update()  # 更新遊戲視窗顯示內容