###################### 載入套件 ######################
import pygame  # 載入 pygame 套件，用來製作遊戲
import sys  # 載入 sys 套件，用來處理系統相關功能
import random  # 載入 random 套件，用來產生隨機數


###################### 物件類別 ######################
# 定義遊戲中會使用到的物件類別
# 例如：主角、敵人、障礙物等
class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)  # 設定主角的矩形範圍
        self.color = color  # 設定主角的顏色
        self.speed = 5  # 設定主角的移動速度
        self.velocity_y = 0  # 設定主角的垂直速度
        self.jump_power = -12  # 設定主角的跳躍力量
        self.gravity = 0.5  # 設定重力加速度
        self.on_platform = False  # 設定主角是否在平台上

    def draw(self, display_area):
        pygame.draw.rect(display_area, self.color, self.rect)
        # 在指定的顯示區域上繪製主角

    def move(self, direction, bg_x):
        self.rect.x += direction * self.speed  # 根據方向移動主角的 x 座標
        if self.rect.right < 0:  # 如果主角超出左邊界
            self.rect.left = bg_x  # 將主角的 x 座標設為左邊界
        elif self.rect.left > bg_x:  # 如果主角超出右邊界
            self.rect.right = 0  # 將主角的 x 座標設為右邊界

    def apply_gravity(self):
        self.velocity_y += self.gravity  # 將重力加速度加到垂直速度上
        self.rect.y += self.velocity_y  # 根據垂直速度更新主角的 y 座標

    def check_platform_collision(self, platforms):
        if self.velocity_y > 0:
            cheak_points = max(1, int(abs(self.velocity_y) / 5))
            step_y = self.velocity_y / cheak_points
            for platform in platforms:
                for i in range(cheak_points):
                    test_rect = self.rect.copy()
                    test_rect.y += i *step_y 
                    if (
                         test_rect.bottom >= platform.rect.top
                        and  test_rect.bottom <= platform.rect.bottom
                        and  test_rect.right >= platform.rect.left
                        and  test_rect.left <= platform.rect.right
                    ):
                        self.rect.bottom = (
                            platform.rect.top
                        )  # 將主角的底部設為平台的頂部
                        self.velocity_y = self.jump_power  # 將垂直速度設為 0
                        self.on_platform = True  # 設定主角在平台上
                        return True
        return False


class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)  # 設定平台的矩形範圍
        self.color = color  # 設定平台的顏色

    def draw(self, display_area):
        pygame.draw.rect(display_area, self.color, self.rect)
        # 在指定的顯示區域上繪製平台


###################### 初始化設定 ######################
pygame.init()  # 初始化 pygame 所有模組
FPS = pygame.time.Clock()  # 建立時鐘物件，用來控制遊戲更新速度

###################### 遊戲視窗設定 ######################
# 設定遊戲視窗的大小、標題與背景顏色
bg_x = 400
bg_y = 600
bg_size = (bg_x, bg_y)
pygame.display.set_caption("Doodle Jump")  # 設定遊戲視窗標題
screen = pygame.display.set_mode(bg_size)  # 設定遊戲視窗大小
###################### 主角設定 ######################
# 設定主角的外觀、位置、移動速度等屬性
player_w = 30
player_h = 30
player_x = (bg_x - player_w) // 2
player_y = bg_y - player_h - 50
player = Player(player_x, player_y, player_w, player_h, (0, 255, 0))
###################### 平台設定 ######################
platform_w = 60
platform_h = 10
platforms = []
platform_x = (bg_x - platform_w) // 2
platform_y = bg_y - platform_h - 10
platform = Platform(
    platform_x, platform_y, platform_w, platform_h, (255, 255, 255)
)  # 建立平台物件，設定位置、大小與顏色
platforms.append(platform)  # 將平台物件加入平台列表
platform_count = random.randint(8, 10)+10 # 隨機生成平台數量
for i in range(platform_count):
    x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
    y = (bg_y - 100) - (i * 60)  # 計算平台的 y 座標，讓平台間隔一定距離
    platform = Platform(
        x, y, platform_w, platform_h, (255, 255, 255)
    )  # 建立平台物件，設定位置、大小與顏色
    platforms.append(platform)  # 將平台物件加入平台列表
 ###################### 自訂程式 ######################
def update_camera():
    screen_middle = bg_y // 2
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        for platform in platforms:
            platform.rect.y += camera_move
        y_min=bg_y
        for platform in platforms:
            if platform.rect.top>bg_y:
                platforms.remove(platform)
            if platform.rect.top<y_min:
                y_min=platform.rect.top
        if len(platforms)<platform_count:
            x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
            y = y_min - 60  # 計算平台的 y 座標，讓平台間隔一定距離
            platform = Platform(
                x, y, platform_w, platform_h, (255, 255, 255)
            )  # 建立平台物件，設定位置、大小與顏色

            platforms.append(platform)  # 將平台物件加入平台列表
###################### 主程式 ######################
# 撰寫遊戲主要執行內容
# 例如：遊戲迴圈、事件偵測、畫面更新等
while True:
    FPS.tick(60)  # 設定遊戲更新速度為每秒 60 次
    screen.fill((0, 0, 0))  # 將遊戲視窗填滿黑色背景
    update_camera()  # 更新攝影機位置，讓主角保持在畫面中間
    keys = pygame.key.get_pressed()  # 取得目前按下的按鍵狀態
    if keys[pygame.K_LEFT]:  # 如果按下左方向鍵
        player.move(-1, bg_x)  # 主角向左移動
    if keys[pygame.K_RIGHT]:  # 如果按下右方向鍵
        player.move(1, bg_x)  # 主角向右移動

    player.apply_gravity()  # 應用重力影響主角
    player.check_platform_collision(platforms)  # 檢查主角是否與平台碰

    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:  # 如果事件類型是退出遊戲
            sys.exit()  # 結束程式

    for platform in platforms:
        platform.draw(screen)  # 在遊戲視窗上繪製平台
    player.draw(screen)  # 在遊戲視窗上繪製主角

    pygame.display.update()  # 更新遊戲視窗顯示內容
