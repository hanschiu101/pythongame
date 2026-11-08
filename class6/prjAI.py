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

    def move(self, direction, bg_x, wrap_edges=True):
        self.rect.x += direction * self.speed  # 根據方向移動主角的 x 座標
        if not wrap_edges:
            self.rect.left = max(0, min(self.rect.left, bg_x - self.rect.width))
        elif self.rect.right < 0:  # 如果主角超出左邊界
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


class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.collected = False

    def draw(self, display_area):
        if not self.collected:
            center = self.rect.center
            pygame.draw.circle(display_area, (255, 220, 0), center, 9)
            pygame.draw.circle(display_area, (255, 255, 180), center, 4)


###################### 初始化設定 ######################
pygame.init()  # 初始化 pygame 所有模組
FPS = pygame.time.Clock()  # 建立時鐘物件，用來控制遊戲更新速度
game_font = pygame.font.SysFont("Microsoft JhengHei", 24)
title_font = pygame.font.SysFont("Microsoft JhengHei", 42)

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
stars = []
platform_count = random.randint(8, 10)+10 # 隨機生成平台數量
score = 0
bridge_blocks = 0
last_block_time = 0
block_cooldown = 350
mc_bridge_y = 0
mc_forward_speed = 2
mc_distance = 0
mc_lane = 0
mc_blocks = []
current_mode = "jump"
game_started = False
mc_start_time = 0
respawn_button = pygame.Rect(10, bg_y - 48, 120, 36)
menu_jump_button = pygame.Rect(100, 220, 200, 55)
menu_mc_button = pygame.Rect(100, 295, 200, 55)
menu_exit_button = pygame.Rect(100, 370, 200, 55)


def create_platforms(mode):
    new_platforms = []
    new_stars = []
    color = (120, 75, 35) if mode == "mc" else (255, 255, 255)
    first_platform = Platform(
        (bg_x - platform_w) // 2,
        bg_y - platform_h - 10,
        platform_w,
        platform_h,
        color
    )
    new_platforms.append(first_platform)
    new_stars.append(Star(first_platform.rect.centerx - 9, first_platform.rect.top - 28))

    if mode == "mc":
        return new_platforms, new_stars

    for i in range(platform_count):
        x = random.randint(0, bg_x - platform_w)
        y = (bg_y - 100) - (i * 60)
        platform = Platform(x, y, platform_w, platform_h, color)
        new_platforms.append(platform)
        new_stars.append(Star(platform.rect.centerx - 9, platform.rect.top - 28))

    return new_platforms, new_stars


def respawn():
    global mc_distance, mc_lane, mc_blocks
    player.rect.x = (bg_x - player_w) // 2
    player.rect.y = bg_y - player_h - 50
    player.velocity_y = 0
    player.on_platform = False
    mc_distance = 0
    mc_lane = 0
    mc_blocks = []


def start_game(mode):
    global current_mode, game_started, platforms, stars, score
    global bridge_blocks, mc_start_time, last_block_time, mc_bridge_y
    current_mode = mode
    game_started = True
    score = 0
    bridge_blocks = 0
    last_block_time = 0
    platforms, stars = create_platforms(mode)
    mc_bridge_y = platforms[0].rect.top
    respawn()
    mc_start_time = pygame.time.get_ticks()


def place_bridge_block():
    global bridge_blocks, last_block_time, score, mc_blocks

    current_time = pygame.time.get_ticks()
    if current_time - last_block_time < block_cooldown:
        return

    keys = pygame.key.get_pressed()
    lane = mc_lane
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        lane = max(-2, lane - 1)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        lane = min(2, lane + 1)
    block_position = (mc_distance + 1, lane)
    if block_position in mc_blocks:
        return
    mc_blocks.append(block_position)
    bridge_blocks += 1
    score += 1
    last_block_time = current_time


def draw_mc_view():
    screen.fill((115, 190, 235))
    pygame.draw.rect(screen, (80, 175, 85), (0, bg_y // 2, bg_x, bg_y // 2))
    horizon_y = bg_y // 2

    for distance, lane in mc_blocks:
        relative_distance = distance - mc_distance
        if -8 <= relative_distance <= 12:
            depth = max(0, relative_distance / 12)
            block_y = horizon_y + int((1 - depth) * 210)
            block_width = int(38 + (1 - depth) * 58)
            block_height = max(8, int(8 + (1 - depth) * 14))
            block_x = bg_x // 2 + lane * 42 - block_width // 2
            pygame.draw.rect(
                screen,
                (150, 95, 45),
                (block_x, block_y, block_width, block_height)
            )
            pygame.draw.rect(
                screen,
                (90, 55, 30),
                (block_x, block_y, block_width, block_height),
                2
            )

    pygame.draw.line(screen, (255, 255, 255), (bg_x // 2 - 10, horizon_y), (bg_x // 2 + 10, horizon_y), 2)
    pygame.draw.line(screen, (255, 255, 255), (bg_x // 2, horizon_y - 10), (bg_x // 2, horizon_y + 10), 2)


def draw_button(button, text, color):
    pygame.draw.rect(screen, color, button)
    pygame.draw.rect(screen, (255, 255, 255), button, 2)
    button_text = game_font.render(text, True, (255, 255, 255))
    screen.blit(button_text, button_text.get_rect(center=button.center))


def draw_menu():
    screen.fill((25, 35, 60))
    title = title_font.render("遊戲模式選擇", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(bg_x // 2, 135)))
    draw_button(menu_jump_button, "跳台冒險", (40, 120, 70))
    draw_button(menu_mc_button, "MC 速建練習場", (120, 75, 35))
    draw_button(menu_exit_button, "離開遊戲", (130, 45, 45))


platforms, stars = create_platforms(current_mode)

 ###################### 自訂程式 ######################
def update_camera():
    screen_middle = bg_y // 2
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        for platform in platforms:
            platform.rect.y += camera_move
        for star in stars:
            star.rect.y += camera_move

        y_min=bg_y
        for platform in platforms[:]:
            if platform.rect.top>bg_y:
                platforms.remove(platform)
                for star in stars[:]:
                    if star.rect.top > bg_y:
                        stars.remove(star)
            if platform.rect.top<y_min:
                y_min=platform.rect.top
        if current_mode == "mc":
            return

        if len(platforms)<platform_count:
            x = random.randint(0, bg_x - platform_w)  # 隨機生成平台的 x 座標
            y = y_min - 60  # 計算平台的 y 座標，讓平台間隔一定距離
            color = (120, 75, 35) if current_mode == "mc" else (255, 255, 255)
            platform = Platform(x, y, platform_w, platform_h, color)

            platforms.append(platform)  # 將平台物件加入平台列表
            stars.append(Star(platform.rect.centerx - 9, platform.rect.top - 28))
###################### 主程式 ######################
# 撰寫遊戲主要執行內容
# 例如：遊戲迴圈、事件偵測、畫面更新等
while True:
    FPS.tick(60)  # 設定遊戲更新速度為每秒 60 次

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if menu_jump_button.collidepoint(event.pos):
                    start_game("jump")
                elif menu_mc_button.collidepoint(event.pos):
                    start_game("mc")
                elif menu_exit_button.collidepoint(event.pos):
                    sys.exit()
            elif respawn_button.collidepoint(event.pos):
                respawn()
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and game_started
            and current_mode == "mc"
        ):
            place_bridge_block()

    if not game_started:
        draw_menu()
        pygame.display.update()
        continue

    if current_mode == "mc":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            mc_distance += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            mc_lane = max(-2, mc_lane - 1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            mc_lane = min(2, mc_lane + 1)

        draw_mc_view()
        draw_button(respawn_button, "重生", (45, 100, 150))
        score_text = game_font.render(
            f"速疊方塊：{bridge_blocks}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_text, (10, 10))
        elapsed = (pygame.time.get_ticks() - mc_start_time) // 1000
        mode_text = game_font.render(
            f"第一人稱倒退速疊　距離：{mc_distance}　時間：{elapsed}秒",
            True,
            (255, 255, 255)
        )
        screen.blit(mode_text, (10, 42))
        help_text = game_font.render(
            "S/↓ 倒退　A/D 左右調整　空白鍵在身後放方塊",
            True,
            (255, 220, 100)
        )
        screen.blit(help_text, (10, 72))
        pygame.display.update()
        continue

    screen.fill((0, 0, 0))  # 將遊戲視窗填滿黑色背景
    update_camera()  # 更新攝影機位置，讓主角保持在畫面中間
    keys = pygame.key.get_pressed()  # 取得目前按下的按鍵狀態
    if keys[pygame.K_LEFT]:  # 如果按下左方向鍵
        player.move(-1, bg_x)  # 主角向左移動
    if keys[pygame.K_RIGHT]:  # 如果按下右方向鍵
        player.move(1, bg_x)  # 主角向右移動

    player.apply_gravity()  # 應用重力影響主角
    player.check_platform_collision(platforms)  # 檢查主角是否與平台碰

    if player.rect.top > bg_y:
        respawn()

    for star in stars:
        if not star.collected and player.rect.colliderect(star.rect):
            star.collected = True
            score += 1

    for platform in platforms:
        platform.draw(screen)  # 在遊戲視窗上繪製平台
    for star in stars:
        star.draw(screen)
    player.draw(screen)  # 在遊戲視窗上繪製主角

    draw_button(respawn_button, "重生", (45, 100, 150))
    score_text = game_font.render(f"星星：{score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()  # 更新遊戲視窗顯示內容
