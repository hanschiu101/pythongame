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
mc_world_blocks = {}
mc_state_stack = []
mc_player_x = 0.0
mc_hotbar = {
    1: "羊毛塊 (∞)",
    2: "橡木方塊 (∞)",
    3: "鑽石稿",
    4: "空手",
    5: "空手",
    6: "空手",
    7: "空手",
    8: "空手",
    9: "空手",
}
mc_selected_slot = 1
mc_message = ""
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
    global mc_world_blocks, mc_state_stack, mc_player_x
    global mc_selected_slot, mc_message
    player.rect.x = (bg_x - player_w) // 2
    player.rect.y = bg_y - player_h - 50
    player.velocity_y = 0
    player.on_platform = False
    mc_world_blocks = {(0, 0, 0): "基石方塊"}
    mc_state_stack = [("站立", 1.62, 4.3, False)]
    mc_player_x = 0.0
    mc_selected_slot = 1
    mc_message = "模擬器啟動成功！請按住 S 開始搭橋"


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


def update_mc_movement():
    global mc_player_x, mc_message, game_started

    state_name, _, speed, anti_fall = mc_state_stack[-1]
    move_distance = speed * 0.15
    next_x = mc_player_x + move_distance
    current_block_index = int(mc_player_x)
    next_block_index = int(next_x)

    if next_block_index > current_block_index:
        if (next_block_index, 0, 0) not in mc_world_blocks:
            if anti_fall:
                mc_player_x = float(current_block_index) + 0.95
                mc_message = "Shift 防墜保護：你停在方塊邊緣"
                return
            mc_message = "你在站立狀態踩空，請按重生重新開始"
            game_started = False
            return

    mc_player_x = next_x
    target_block = int(mc_player_x + 1.0)
    current_item = mc_hotbar[mc_selected_slot]
    if (target_block, 0, 0) not in mc_world_blocks:
        if "塊" in current_item:
            mc_world_blocks[(target_block, 0, 0)] = current_item
            mc_message = f"成功在身後生成方塊 ({target_block}, 0, 0)"
        else:
            mc_message = f"放置失敗：手上拿著「{current_item}」"
    else:
        mc_message = f"目前狀態：{state_name}"


def draw_mc_view():
    screen.fill((115, 190, 235))
    horizon_y = bg_y // 2
    pygame.draw.rect(screen, (35, 40, 65), (0, horizon_y, bg_x, bg_y // 2))
    center_x = bg_x // 2

    for (block_x, _, _), block_name in mc_world_blocks.items():
        relative_x = block_x - mc_player_x
        if -5 <= relative_x <= 12:
            screen_x = center_x + int(relative_x * 32)
            depth = max(0.35, 1 - max(relative_x, 0) / 14)
            width = max(16, int(48 * depth))
            height = max(10, int(24 * depth))
            block_y = horizon_y + int(120 * (1 - depth))
            block_rect = pygame.Rect(screen_x - width // 2, block_y, width, height)
            color = (80, 80, 80) if block_name == "基石方塊" else (150, 95, 45)
            pygame.draw.rect(screen, color, block_rect)
            pygame.draw.rect(screen, (45, 35, 25), block_rect, 2)

    player_y = horizon_y - 45
    pygame.draw.rect(screen, (0, 220, 80), (center_x - 12, player_y, 24, 40))
    pygame.draw.circle(screen, (255, 220, 170), (center_x, player_y - 8), 11)


def draw_mc_hotbar():
    slot_width = 40
    start_x = (bg_x - slot_width * 9) // 2
    y = bg_y - 88
    for slot in range(1, 10):
        rect = pygame.Rect(start_x + (slot - 1) * slot_width, y, slot_width, 38)
        color = (230, 190, 50) if slot == mc_selected_slot else (70, 70, 80)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        slot_text = game_font.render(str(slot), True, (255, 255, 255))
        screen.blit(slot_text, slot_text.get_rect(center=rect.center))


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
    draw_button(menu_mc_button, "MC", (120, 75, 35))
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
        if event.type == pygame.KEYDOWN and game_started:
            if event.key == pygame.K_ESCAPE:
                game_started = False
                current_mode = "jump"
            elif current_mode == "mc" and pygame.K_1 <= event.key <= pygame.K_9:
                mc_selected_slot = event.key - pygame.K_0
                mc_message = f"手持格已切換到 Slot {mc_selected_slot}"
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
    if not game_started:
        draw_menu()
        pygame.display.update()
        continue

    if current_mode == "mc":
        keys = pygame.key.get_pressed()
        crouching = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if crouching and mc_state_stack[-1][0] != "蹲下":
            mc_state_stack.append(("蹲下", 1.50, 1.3, True))
            mc_message = "按住 Shift 進入蹲下姿態"
        elif not crouching and len(mc_state_stack) > 1:
            mc_state_stack.pop()
            mc_message = "放開 Shift 恢復站立"
        if keys[pygame.K_s]:
            update_mc_movement()

        draw_mc_view()
        state_name, camera_height, _, anti_fall = mc_state_stack[-1]
        status_text = game_font.render(
            f"狀態：{state_name}  防墜：{'ON' if anti_fall else 'OFF'}",
            True,
            (255, 255, 255)
        )
        screen.blit(status_text, (10, 10))
        position_text = game_font.render(
            f"X：{mc_player_x:.2f}  相機高度：{1.0 + camera_height:.2f}m",
            True,
            (255, 255, 255)
        )
        screen.blit(position_text, (10, 42))
        elapsed = (pygame.time.get_ticks() - mc_start_time) // 1000
        mode_text = game_font.render(
            f"MC 速疊　時間：{elapsed}秒　方塊：{len(mc_world_blocks) - 1}",
            True,
            (255, 255, 255)
        )
        screen.blit(mode_text, (10, 74))
        help_text = game_font.render(
            "按住 S 移動並放方塊　Shift 蹲下防墜　數字鍵切換　Esc 返回",
            True,
            (255, 220, 100)
        )
        screen.blit(help_text, (10, 106))
        message_text = game_font.render(mc_message, True, (255, 230, 150))
        screen.blit(message_text, (10, 138))
        draw_mc_hotbar()
        draw_button(respawn_button, "重生", (45, 100, 150))
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
