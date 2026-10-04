######################載入套件/ import packages######################

import random
# random 是用來生成隨機數的套件

import pygame
# pygame 是製作遊戲和多媒體程式的套件

import sys
# sys 可以用來結束程式


######################物件類別/ object class######################

class Brick:
    # 建立一個磚塊類別

    def __init__(self, x, y, width, height, color):
        # 建立磚塊時設定磚塊的資料
        # x、y 是磚塊的位置
        # width、height 是磚塊的寬度和高度
        # color 是磚塊的顏色

        self.rect = pygame.Rect(x, y, width, height)
        # 建立磚塊的矩形
        # pygame.Rect 可以設定物件的位置和大小

        self.color = color
        # 設定磚塊的顏色

        self.hit = False
        # 設定磚塊一開始沒有被打到
        # False 表示還沒有被打到

    def draw(self, display_area):
        # 建立繪製磚塊的函式
        # display_area 代表要繪製磚塊的畫面

        if not self.hit:
            # 判斷磚塊是否還沒有被打到
            # 如果 hit 是 False，就會繪製磚塊

            pygame.draw.rect(display_area, self.color, self.rect)
            # 將磚塊繪製到遊戲畫面上
            # 使用 self.color 作為磚塊的顏色
            # 使用 self.rect 作為磚塊的位置和大小


class Ball:
    # 建立一個球的類別

    def __init__(self, x, y, radius, color):
        # 建立球時設定球的資料
        # x、y 是球的位置
        # radius 是球的半徑
        # color 是球的顏色

        self.x = x
        # 設定球的 X 座標

        self.y = y
        # 設定球的 Y 座標

        self.radius = radius
        # 設定球的半徑

        self.color = color
        # 設定球的顏色

        self.speed_x = 5
        # 設定球的水平速度

        self.speed_y = -5
        # 設定球的垂直速度

        self.is_moving = False
        # 設定球一開始沒有移動

    def draw(self, display_area):
        # 建立繪製球的函式
        # display_area 代表要繪製球的畫面

        pygame.draw.circle(
            display_area,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )
        # 將球繪製到遊戲畫面上
        # 使用圓形來表示球
        # int(self.x)、int(self.y) 是球的中心位置
        # self.radius 是球的半徑

    def move(self):
        # 建立移動球的函式

        if self.is_moving:
            # 判斷球是否在移動

            self.x += self.speed_x
            # 將球的 X 座標加上水平速度

            self.y += self.speed_y
            # 將球的 Y 座標加上垂直速度

    def check_collision(self, bg_x, bg_y, bricks,pad):
        # 建立碰撞檢查球的函式
        if self.x - self.radius <= 0 or self.x + self.radius >= bg_x:
            self.speed_x = -self.speed_x
        if self.y-self.radius<=0:
            self.speed_y=-self.speed_y
        if self.y+self.radius>=bg_y:
            self.is_moving=False
        if(
            self.y+self.radius>=pad.rect.y 
            and self.x-self.radius<=pad.rect.y+pad.rect.width
            and self.x>=pad.rect.x
            and self.x<=pad.rect.x+pad.rect.width
        ):
            self.speed_y=-abs(self.speed_y)
        for brick in bricks:
            if not brick.hit:
                dx=abs(self.x-(brick.rect.x+brick.rect.width/2))
                dy=abs(self.y-(brick.rect.y+brick.rect.height/2))
                if dx<=(self.radius+brick.rect.width/2) and dy<=(self.radius+brick.rect.height/2):
                     brick.hit=True

                     if self.x<brick.rect.x or self.x>brick.rect.x+brick.rect.width:
                         self.speed_x=-self.speed_x
                     else:
                            self.speed_y=-self.speed_y
######################定義函式區/ define functions######################

# 這個區域用來放置其他需要使用的函式
# 目前沒有另外建立函式


######################初始化設定/ initialize settings######################

pygame.init()
# 開始使用 pygame 的功能

FPS = pygame.time.Clock()
# 建立一個 Clock 物件
# 用來控制遊戲執行的速度


######################載入圖片/ load images######################

# 這個區域用來載入遊戲需要的圖片
# 目前沒有使用圖片


######################遊戲視窗設定/ game window settings######################

bg_x = 800
# 設定遊戲視窗的寬度
# 寬度為 800 像素

bg_y = 600
# 設定遊戲視窗的高度
# 高度為 600 像素

bg_size = (bg_x, bg_y)
# 設定遊戲視窗的大小
# bg_size 會是 (800, 600)

pygame.display.set_caption("打磚塊遊戲")
# 將遊戲視窗的標題設定為打磚塊遊戲

screen = pygame.display.set_mode(bg_size)
# 建立遊戲視窗並使用設定好的大小
# screen 代表遊戲畫面


######################磚塊設定/ brick settings######################

bricks_row = 9
# 設定磚塊的列數
# 一共有 9 列

bricks_col = 11
# 設定磚塊的行數
# 一共有 11 行

brick_w = 58
# 設定每個磚塊的寬度
# 寬度為 58 像素

brick_h = 16
# 設定每個磚塊的高度
# 高度為 16 像素

bricks_gap = 2
# 設定磚塊之間的間隔
# 每個磚塊之間相隔 2 像素

bricks = []
# 建立空的磚塊列表，用來存放磚塊

for col in range(bricks_col):
    # 依照磚塊的行數重複執行
    # 這裡會執行 11 次

    for row in range(bricks_row):
        # 依照磚塊的列數重複執行
        # 每一次會執行 9 次

        x = col * (brick_w + bricks_gap) + 70
        # 計算每個磚塊的 X 座標
        # col 越大，磚塊的位置越往右

        y = row * (brick_h + bricks_gap) + 60
        # 計算每個磚塊的 Y 座標
        # row 越大，磚塊的位置越往下

        color = (
            random.randint(20, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        # 隨機產生磚塊的顏色
        # RGB 三個數值分別代表紅、綠、藍
        # 每個磚塊的顏色可能都不一樣

        brick = Brick(x, y, brick_w, brick_h, color)
        # 建立一個磚塊物件
        # 使用計算好的位置、大小和顏色

        bricks.append(brick)
        # 將建立好的磚塊加入磚塊列表


######################顯示文字設定/ text display settings######################

# 這個區域用來設定遊戲中的文字
# 目前沒有設定文字


######################底板設定/ paddle settings######################

pad = Brick(0, bg_y - 48, brick_w, brick_h, (255, 255, 255))
# 建立遊戲中的底板
# 使用 Brick 類別建立底板
# 底板的顏色是白色


######################球設定/ ball settings######################

ball_radius = 10
# 設定球的半徑
# 球的半徑為 10 像素

ball_color = (255, 255, 0)
# 設定球的顏色
# RGB(255, 255, 0) 代表黃色

ball = Ball(
    pad.rect.x + pad.rect.width // 2,
    pad.rect.y - ball_radius,
    ball_radius,
    ball_color
)
# 建立一個球物件
# 球的 X 座標設定在底板的中央
# 球的 Y 座標設定在底板上方
# 使用 ball_radius 設定球的半徑
# 使用 ball_color 設定球的顏色


######################遊戲結束設定/ game over settings######################

# 這個區域用來設定遊戲結束相關內容
# 目前沒有設定遊戲結束條件


######################主程式/ main program######################

while True:
    # 持續執行遊戲主程式
    # while True 會讓遊戲一直執行

    FPS.tick(60)
    # 控制遊戲速度
    # 遊戲最多每秒執行 60 次

    screen.fill((0, 0, 0))
    # 清除背景
    # 使用黑色填滿整個遊戲畫面

    mos_x, mos_y = pygame.mouse.get_pos()
    # 取得滑鼠的座標
    # mos_x 是滑鼠的 X 座標
    # mos_y 是滑鼠的 Y 座標

    pad.rect.x = mos_x - pad.rect.width // 2
    # 將底板的 X 座標設定為滑鼠的 X 座標
    # 減去底板寬度的一半
    # 讓滑鼠位於底板的中央

    if pad.rect.x < 0:
        # 判斷底板是否超出遊戲畫面的左邊

        pad.rect.x = 0
        # 如果超出左邊，就將底板放回最左邊

    if pad.rect.x + pad.rect.width > bg_x:
        # 判斷底板是否超出遊戲畫面的右邊

        pad.rect.x = bg_x - pad.rect.width
        # 如果超出右邊，就將底板放回遊戲畫面內
    if not ball.is_moving:
        # 判斷球是否沒有在移動
        # 如果球沒有在移動，就將球放在底板上方

        ball.x = pad.rect.x + pad.rect.width // 2
        # 將球的 X 座標設定為底板的中央

        ball.y = pad.rect.y - ball_radius
    else:
        ball.move()
        # 如果球正在移動，就呼叫 move() 函式讓球移動

        ball.check_collision(bg_x, bg_y, bricks,pad)
        # 呼叫 check_collision() 函式檢查球是否碰到邊界或磚塊
        # bg_x、bg_y 是遊戲畫面的寬度和高度
        # bricks 是磚塊列表
        # pad 是底板物件

    # 將球的 Y 座標設定為底板上方

    for event in pygame.event.get():
        # 取得所有遊戲事件
        # 檢查遊戲中發生的事件
        # 例如關閉視窗、鍵盤或滑鼠事件

        if event.type == pygame.QUIT:
            # 判斷是否按下關閉視窗

            sys.exit()
            # 結束遊戲程式
        if event.type==pygame.MOUSEBUTTONDOWN:
            # 判斷是否按下滑鼠按鈕

            if not ball.is_moving:
                # 判斷球是否沒有在移動
                # 如果球沒有在移動，就讓球開始移動

                ball.is_moving=True
                # 將球的 is_moving 設定為 True
                # 讓球開始移動  

    for brick in bricks:
        # 逐一取得磚塊列表中的磚塊
        # 每次取得一個磚塊

        brick.draw(screen)
        # 將每一個磚塊畫到遊戲畫面上

    pad.draw(screen)
    # 將底板畫到遊戲畫面上

    ball.draw(screen)
    # 將球畫到遊戲畫面上

    pygame.display.update()
    # 更新遊戲視窗
    # 將這一幀畫好的內容顯示出來
