###################### 載入套件 ######################
import pygame  # 載入 pygame 套件，用來製作遊戲
import sys  # 載入 sys 套件，用來處理系統相關功能
import random  # 載入 random 套件，用來產生隨機數
import os  # 載入 os 套件，用來處理檔案與目錄相關功能

os.chdir(sys.path[0])  # 設定工作目錄為程式所在的目錄
###################### 全程變數 ######################
score = 0  # 記錄遊戲分數
highest_score = 0  # 記錄最高分數
game_over = False  # 記錄遊戲是否結束
initial_platform_y = 0
spring_chance = 0.2  # 記錄彈簧出現的機率
springs = []  # 記錄彈簧物件的列表


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

    def check_spring_collision(self, springs):
        if self.velocity_y > 0:
            cheak_points = max(1, int(abs(self.velocity_y) / 5))
            step_y = self.velocity_y / cheak_points
            for spring in springs:
                for i in range(cheak_points):
                    test_rect = self.rect.copy()
                    test_rect.y += i * step_y
                    if (
                        test_rect.bottom >= spring.rect.top
                        and test_rect.bottom <= spring.rect.bottom
                        and test_rect.right >= spring.rect.left
                        and test_rect.left <= spring.rect.right

    def check_platform_collision(self, platforms):
        if self.velocity_y > 0:
            cheak_points = max(1, int(abs(self.velocity_y) / 5))
            step_y = self.velocity_y / cheak_points
            for platform in platforms:
                for i in range(cheak_points):
                    test_rect = self.rect.copy()
                    test_rect.y += i * step_y
                    if (
                        test_rect.bottom >= platform.rect.top
                        and test_rect.bottom <= platform.rect.bottom
                        and test_rect.right >= platform.rect.left
                        and test_rect.left <= platform.rect.right
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


class Spring:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)  # 設定彈簧的矩形範圍
        self.color = color  # 設定彈簧的顏色

    def draw(self, display_area):
        pygame.draw.rect(display_area, self.color, self.rect)

    def move_with_platform(self, dy):
        # 在指定的顯示區域上繪製彈簧
        self.rect.y += dy  # 將彈簧的 y 座標加上 dy，讓彈簧跟著平台移動


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
platform_count = random.randint(8, 10) + 10  # 隨機生成平台數量
for i in range(platform_count):
    x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
    y = (bg_y - 100) - (i * 60)  # 計算平台的 y 座標，讓平台間隔一定距離
    platform = Platform(
        x, y, platform_w, platform_h, (255, 255, 255)
    )  # 建立平台物件，設定位置、大小與顏色
    platforms.append(platform)  # 將平台物件加入平台列表

######################字行設定 ######################
font = pygame.font.SysFont("Microsoft JhengHei", 24)  # 設定字型與大小


###################### 自訂程式 ######################
def update_camera():
    global score, initial_player_y, springs
    screen_middle = bg_y // 2
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        score += int(camera_move / 10)
        for platform in platforms:
            platform.rect.y += camera_move
        for spring in springs:
            spring.move_with_platform(camera_move)
        y_min = bg_y
        for platform in platforms[:]:
            if platform.rect.top > bg_y:
                platforms.remove(platform)
            if platform.rect.top < y_min:
                y_min = platform.rect.top
        for spring in springs[:]:
            if spring.rect.top > bg_y:
                springs.remove(spring)
        if len(platforms) < platform_count:
            x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
            y = y_min - 60  # 計算平台的 y 座標，讓平台間隔一定距離
            platform = Platform(
                x, y, platform_w, platform_h, (255, 255, 255)
            )  # 建立平台物件，設定位置、大小與顏色

            platforms.append(platform)  # 將平台物件加入平台列表
            if random.random() < spring_chance:  # 根據彈簧出現的機率決定是否生成彈簧
                spring_w = 20
                spring_h = 10
                spring_x = (
                    platform.rect.x + (platform_w - spring_w) // 2
                )  # 計算彈簧的 x 座標，讓彈簧置中於平台
                spring_y = platform.rect.y - spring_h  # 計算彈簧的 y
                spring = Spring(
                    spring_x, spring_y, spring_w, spring_h, (255, 215, 0)
                )  # 建立彈簧物件，設定位置、大小與顏色
                springs.append(spring)  # 將彈簧物件加入彈簧列表


def reset_game():
    global score, game_over, platforms, initial_player_y, highest_score, springs
    player.rect.x = (bg_x - player_w) // 2
    player.rect.y = bg_y - player_h - 50
    player.velocity_y = 0
    platforms.clear()
    springs.clear()
    platform_x = (bg_x - platform_w) // 2
    platform_y = bg_y - platform_h - 10
    platform = Platform(
        platform_x, platform_y, platform_w, platform_h, (255, 255, 255)
    )  # 建立平台物件，設定位置、大小與顏色
    platforms.append(platform)  # 將平台物件加入平台列表
    for i in range(platform_count - 1):
        x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
        y = (bg_y - 100) - (i * 60)
        platform = Platform(x, y, platform_w, platform_h, (255, 255, 255))
        platforms.append(platform)  # 將平台物件加入平台列表
    if random.random() < spring_chance:  # 根據彈簧出現的機率決定是否生成彈簧
        spring_w = 20
        spring_h = 10
        spring_x = (
            platform.rect.x + (platform_w - spring_w) // 2
        )  # 計算彈簧的 x 座標，讓彈簧置中於平台
        spring_y = platform.rect.y - spring_h  # 計算彈簧的 y 座標，讓彈簧置於平台上方
        spring = Spring(
            spring_x, spring_y, spring_w, spring_h, (255, 215, 0)
        )  # 建立彈簧物件，設定位置、大小與顏色
        springs.append(spring)  # 將彈簧物件加入彈簧列表
    score = 0
    game_over = False
    initial_player_y = player.rect.y


###################### 主程式 ######################
# 撰寫遊戲主要執行內容
# 例如：遊戲迴圈、事件偵測、畫面更新等
while True:
    FPS.tick(60)  # 設定遊戲更新速度為每秒 60 次
    screen.fill((0, 0, 0))  # 將遊戲視窗填滿黑色背景
    if not game_over:
        update_camera()  # 更新攝影機位置，讓主角保持在畫面中間
        keys = pygame.key.get_pressed()  # 取得目前按下的按鍵狀態
        if keys[pygame.K_LEFT]:  # 如果按下左方向鍵
            player.move(-1, bg_x)  # 主角向左移動
        if keys[pygame.K_RIGHT]:  # 如果按下右方向鍵
            player.move(1, bg_x)  # 主角向右移動

        player.apply_gravity()  # 應用重力影響主角
        player.check_platform_collision(platforms)  # 檢查主角是否與平台碰
        if player.rect.top > bg_y:  # 如果主角超出下邊界
            game_over = True  # 設定遊戲結束
            if score > highest_score:
                highest_score = score  # 更新最高分數
    for event in pygame.event.get():  # 取得所有事件
        if event.type == pygame.QUIT:  # 如果事件類型是退出遊戲
            sys.exit()  # 結束程式
        elif (
            event.type == pygame.KEYDOWN and game_over
        ):  # 如果事件類型是按鍵按下且遊戲結束
            reset_game()  # 重置遊戲

    for platform in platforms:
        platform.draw(screen)  # 在遊戲視窗上繪製平台
    for spring in springs:
        spring.draw(screen)  # 在遊戲視窗上繪製彈簧
    player.draw(screen)  # 在遊戲視窗上繪製主角
    score_text = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # 在遊戲視窗上顯示分數
    if game_over:
        game_over_text = font.render(
            "遊戲結束，按任意鍵重新開始", True, (255, 255, 255)
        )
        highest_score_text = font.render(
            f"最高分數: {highest_score}", True, (255, 255, 255)
        )
        text_rect = game_over_text.get_rect(center=(bg_x / 2, bg_y / 2))
        score_rect = highest_score_text.get_rect(center=(bg_x / 2, bg_y / 2 + 40))
        screen.blit(game_over_text, text_rect)  # 在遊戲視窗上顯示遊戲結束訊息
        screen.blit(highest_score_text, score_rect)  # 顯示最高分數
    pygame.display.update()  # 更新遊戲視窗顯示內容
