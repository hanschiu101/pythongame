###################### 載入套件 ######################
import pygame  # 載入 pygame 套件，用來製作遊戲
import sys  # 載入 sys 套件，用來處理系統相關功能
import random  # 載入 random 套件，用來產生隨機數
import time  # 載入 time 套件，用來計算反應時間


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
mc_is_crouching = False
mc_successful_bridges = 0
mc_clutch_count = 0
mc_fail_trigger_time = 0.0
mc_reaction_times = []
current_mode = "jump"
game_started = False
mc_start_time = 0
parkour_goal = None
parkour_message = ""
parkour_won = False
respawn_button = pygame.Rect(10, bg_y - 48, 120, 36)
menu_jump_button = pygame.Rect(100, 220, 200, 55)
menu_mc_button = pygame.Rect(100, 295, 200, 55)
menu_parkour_button = pygame.Rect(100, 370, 200, 55)
menu_exit_button = pygame.Rect(100, 445, 200, 55)


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

    if mode == "parkour":
        parkour_platforms = [
            Platform(45, 500, 70, 18, (80, 120, 210)),
            Platform(135, 440, 70, 18, (80, 160, 220)),
            Platform(225, 370, 70, 18, (80, 200, 230)),
            Platform(315, 300, 70, 18, (220, 180, 40)),
        ]
        return parkour_platforms, []

    for i in range(platform_count):
        x = random.randint(0, bg_x - platform_w)
        y = (bg_y - 100) - (i * 60)
        platform = Platform(x, y, platform_w, platform_h, color)
        new_platforms.append(platform)
        new_stars.append(Star(platform.rect.centerx - 9, platform.rect.top - 28))

    return new_platforms, new_stars


def respawn():
    global mc_world_blocks, mc_state_stack, mc_player_x
    global mc_selected_slot, mc_message, mc_is_crouching
    global mc_successful_bridges, mc_clutch_count
    global mc_fail_trigger_time, mc_reaction_times
    global parkour_message, parkour_won
    player.rect.x = (bg_x - player_w) // 2
    player.rect.y = bg_y - player_h - 50
    player.velocity_y = 0
    player.on_platform = False
    mc_world_blocks = {(0, 0, 0): "基石方塊"}
    mc_state_stack = [("站立", 1.62, 4.3, False)]
    mc_player_x = 0.0
    mc_selected_slot = 1
    mc_is_crouching = False
    mc_successful_bridges = 0
    mc_clutch_count = 0
    mc_fail_trigger_time = 0.0
    mc_reaction_times = []
    mc_message = "訓練場準備完成！請交替按 S 與 J 開始"
    parkour_message = "跑酷關卡準備完成！跳到最後的金塊上獲勝"
    parkour_won = False


def start_game(mode):
    global current_mode, game_started, platforms, stars, score
    global bridge_blocks, mc_start_time, last_block_time, mc_bridge_y
    global parkour_goal
    current_mode = mode
    game_started = True
    score = 0
    bridge_blocks = 0
    last_block_time = 0
    platforms, stars = create_platforms(mode)
    mc_bridge_y = platforms[0].rect.top
    respawn()
    if mode == "parkour":
        parkour_goal = platforms[-1].rect
        player.rect.centerx = platforms[0].rect.centerx
        player.rect.bottom = platforms[0].rect.top
        player.velocity_y = 0
    mc_start_time = pygame.time.get_ticks()


def update_mc_movement():
    global mc_player_x, mc_message, game_started
    global mc_clutch_count, mc_fail_trigger_time
    global mc_reaction_times

    state_name, _, speed, _ = mc_state_stack[-1]
    move_distance = speed * 0.15
    next_x = mc_player_x + move_distance
    current_block_index = int(mc_player_x)
    next_block_index = int(next_x)

    if next_block_index > current_block_index:
        if (next_block_index, 0, 0) not in mc_world_blocks:
            if mc_is_crouching:
                if mc_fail_trigger_time > 0.0:
                    reaction_time = time.time() - mc_fail_trigger_time
                    mc_reaction_times.append(reaction_time)
                    mc_clutch_count += 1
                    mc_fail_trigger_time = 0.0
                    mc_player_x = float(current_block_index) + 0.99
                    mc_message = (
                        f"神救橋！反應時間 {reaction_time * 1000:.0f} 毫秒"
                    )
                    return

                mc_player_x = float(current_block_index) + 0.95
                mc_message = "按住 Shift 安全挪步中，等待前方方塊"
                return

            mc_message = "墜空身亡：沒有方塊且沒有按住 Shift"
            game_started = False
            return

    mc_player_x = next_x
    mc_message = f"移動中：{state_name}"


def place_mc_block():
    global mc_successful_bridges, mc_fail_trigger_time, mc_message

    target_block = int(mc_player_x + 1.0)
    if (target_block, 0, 0) in mc_world_blocks:
        mc_message = "前方已有方塊，請繼續按 S 移動"
        return

    if random.random() < 0.35:
        mc_fail_trigger_time = time.time()
        mc_message = "卡彈！前方沒有方塊，請立刻按住 Shift 再按 S"
        return

    mc_world_blocks[(target_block, 0, 0)] = "羊毛"
    mc_successful_bridges += 1
    mc_fail_trigger_time = 0.0
    mc_message = f"成功搭橋：第 {target_block} 格"


def draw_3d_block(surface, block_rect, color, depth):
    side_color = tuple(max(0, value - 45) for value in color)
    top_color = tuple(min(255, value + 35) for value in color)
    side_width = max(3, depth // 3)
    side_height = max(3, depth // 4)

    top_points = (
        (block_rect.left, block_rect.top),
        (block_rect.left + side_width, block_rect.top - side_height),
        (block_rect.right + side_width, block_rect.top - side_height),
        (block_rect.right, block_rect.top)
    )
    side_points = (
        (block_rect.right, block_rect.top),
        (block_rect.right + side_width, block_rect.top - side_height),
        (block_rect.right + side_width, block_rect.bottom - side_height),
        (block_rect.right, block_rect.bottom)
    )

    pygame.draw.polygon(surface, top_color, top_points)
    pygame.draw.polygon(surface, side_color, side_points)
    pygame.draw.rect(surface, color, block_rect)
    pygame.draw.polygon(surface, (45, 45, 50), top_points, 1)
    pygame.draw.polygon(surface, (45, 45, 50), side_points, 1)
    pygame.draw.rect(surface, (45, 45, 50), block_rect, 1)


def draw_mc_view():
    _, camera_height, _, _ = mc_state_stack[-1]
    crouch_offset = int((1.62 - camera_height) * 55)
    center_x = bg_x // 2

    horizon_y = 125 + crouch_offset
    for sky_y in range(bg_y):
        blend = sky_y / bg_y
        sky_color = (
            int(145 - blend * 20),
            int(195 - blend * 15),
            int(245 - blend * 5)
        )
        pygame.draw.line(screen, sky_color, (0, sky_y), (bg_x, sky_y))

    pygame.draw.rect(
        screen,
        (38, 48, 80),
        (0, horizon_y, bg_x, bg_y - horizon_y)
    )

    # 速疊視角只顯示實際存在的橋面，橋外是虛空。
    for (block_x, _, _), block_name in mc_world_blocks.items():
        relative_x = block_x - mc_player_x
        if -1 <= relative_x <= 10:
            depth = 1 / (relative_x + 1.5)
            block_center_y = bg_y - int((1 - depth) * 390)
            block_width = max(18, int(190 * depth))
            block_length = max(10, int(125 * depth))
            block_center_x = center_x
            block_points = (
                (block_center_x - block_width // 2, block_center_y - block_length // 2),
                (block_center_x + block_width // 2, block_center_y - block_length // 2),
                (block_center_x + block_width // 2, block_center_y + block_length // 2),
                (block_center_x - block_width // 2, block_center_y + block_length // 2)
            )
            if block_name == "基石方塊":
                block_color = (95, 95, 100)
            elif block_name == "羊毛":
                block_color = (235, 235, 240)
            else:
                block_color = (210, 170, 45)
            draw_3d_block(
                screen,
                pygame.Rect(
                    block_points[0][0],
                    block_points[0][1],
                    block_width,
                    block_length
                ),
                block_color,
                max(4, int(block_width * 0.18))
            )

    crosshair_color = (255, 255, 255)
    crosshair_x = center_x
    crosshair_y = bg_y // 2
    pygame.draw.line(
        screen, crosshair_color, (crosshair_x - 7, crosshair_y),
        (crosshair_x + 7, crosshair_y), 2
    )
    pygame.draw.line(
        screen, crosshair_color, (crosshair_x, crosshair_y - 7),
        (crosshair_x, crosshair_y + 7), 2
    )

    hand_x = bg_x - 82
    hand_y = bg_y - 102 + crouch_offset
    pygame.draw.polygon(
        screen,
        (235, 185, 140),
        (
            (hand_x, hand_y + 60),
            (hand_x + 25, hand_y + 24),
            (hand_x + 62, hand_y + 36),
            (hand_x + 45, hand_y + 78),
        )
    )
    draw_3d_block(
        screen,
        pygame.Rect(hand_x + 12, hand_y + 28, 35, 35),
        (235, 235, 240),
        9
    )


def draw_mc_hotbar():
    slot_width = 38
    slot_height = 42
    start_x = (bg_x - slot_width * 9) // 2
    y = bg_y - slot_height - 10
    pygame.draw.rect(
        screen,
        (25, 25, 28),
        (start_x - 5, y - 5, slot_width * 9 + 10, slot_height + 10)
    )
    for slot in range(1, 10):
        rect = pygame.Rect(
            start_x + (slot - 1) * slot_width,
            y,
            slot_width,
            slot_height
        )
        color = (235, 205, 75) if slot == mc_selected_slot else (75, 75, 80)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        if slot == mc_selected_slot:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        if slot in (1, 2):
            item_color = (235, 235, 240) if slot == 1 else (125, 80, 45)
            draw_3d_block(
                screen,
                pygame.Rect(rect.centerx - 9, rect.centery - 7, 18, 18),
                item_color,
                5
            )
        slot_text = game_font.render(str(slot), True, (225, 225, 225))
        screen.blit(slot_text, (rect.left + 3, rect.top + 2))


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
    draw_button(menu_parkour_button, "跑酷", (170, 110, 35))
    draw_button(menu_exit_button, "離開遊戲", (130, 45, 45))


def draw_parkour_game():
    screen.fill((145, 195, 245))
    pygame.draw.rect(screen, (45, 55, 85), (0, 330, bg_x, bg_y - 330))

    for index, platform in enumerate(platforms):
        platform.draw(screen)
        if index < len(platforms) - 1:
            pygame.draw.rect(screen, (80, 190, 245), platform.rect, 3)
        else:
            pygame.draw.rect(screen, (255, 230, 80), platform.rect, 3)

    player.draw(screen)
    title = game_font.render("Python 跑酷挑戰", True, (255, 255, 255))
    screen.blit(title, (10, 10))
    help_text = game_font.render(
        "方向鍵移動　空白鍵跳躍　跳到最後的金塊過關　Esc 返回",
        True,
        (255, 240, 120)
    )
    screen.blit(help_text, (10, 42))
    message_text = game_font.render(parkour_message, True, (255, 255, 255))
    screen.blit(message_text, (10, 74))

    if parkour_won:
        victory_text = title_font.render("恭喜通關！", True, (255, 215, 0))
        screen.blit(victory_text, victory_text.get_rect(center=(bg_x // 2, 180)))
        draw_button(respawn_button, "再玩一次", (45, 100, 150))


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
            elif current_mode == "mc" and event.key == pygame.K_s:
                update_mc_movement()
            elif current_mode == "mc" and event.key == pygame.K_j:
                place_mc_block()
            elif current_mode == "parkour" and event.key == pygame.K_SPACE:
                if player.on_platform and not parkour_won:
                    player.velocity_y = player.jump_power
                    player.on_platform = False
        if (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT)
            and game_started
            and current_mode == "mc"
        ):
            if not mc_is_crouching:
                mc_is_crouching = True
                mc_state_stack[-1] = ("蹲下", 1.50, 1.3, False)
                mc_message = "Shift 煞車已按下"
        if (
            event.type == pygame.KEYUP
            and event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT)
            and current_mode == "mc"
        ):
            if not pygame.key.get_pressed()[pygame.K_LSHIFT] and not pygame.key.get_pressed()[pygame.K_RSHIFT]:
                mc_is_crouching = False
                mc_state_stack[-1] = ("站立", 1.62, 4.3, False)
                mc_message = "Shift 已放開，現在是高危險極速狀態"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if menu_jump_button.collidepoint(event.pos):
                    start_game("jump")
                elif menu_mc_button.collidepoint(event.pos):
                    start_game("mc")
                elif menu_parkour_button.collidepoint(event.pos):
                    start_game("parkour")
                elif menu_exit_button.collidepoint(event.pos):
                    sys.exit()
            elif respawn_button.collidepoint(event.pos):
                if current_mode == "parkour":
                    start_game("parkour")
                else:
                    respawn()
    if not game_started:
        draw_menu()
        pygame.display.update()
        continue

    if current_mode == "mc":
        draw_mc_view()
        state_name, camera_height, _, _ = mc_state_stack[-1]
        status_text = game_font.render(
            f"狀態：{state_name}  手動防摔：{'按下' if mc_is_crouching else '放開'}",
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
            f"手動防摔訓練　時間：{elapsed}秒　成功搭橋：{mc_successful_bridges}",
            True,
            (255, 255, 255)
        )
        screen.blit(mode_text, (10, 74))
        help_text = game_font.render(
            "按 S 移動　按 J 放方塊　按住 Shift 防摔　數字鍵切換　Esc 返回",
            True,
            (255, 220, 100)
        )
        screen.blit(help_text, (10, 106))
        message_text = game_font.render(mc_message, True, (255, 230, 150))
        screen.blit(message_text, (10, 138))
        clutch_text = game_font.render(
            f"成功救橋：{mc_clutch_count} 次",
            True,
            (255, 255, 255)
        )
        screen.blit(clutch_text, (10, 170))
        if mc_reaction_times:
            average_reaction = (
                sum(mc_reaction_times) / len(mc_reaction_times) * 1000
            )
            reaction_text = game_font.render(
                f"平均反應時間：{average_reaction:.0f} 毫秒",
                True,
                (255, 255, 255)
            )
            screen.blit(reaction_text, (10, 202))
        draw_mc_hotbar()
        draw_button(respawn_button, "重生", (45, 100, 150))
        pygame.display.update()
        continue

    if current_mode == "parkour":
        if not parkour_won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1, bg_x, wrap_edges=False)
            if keys[pygame.K_RIGHT]:
                player.move(1, bg_x, wrap_edges=False)

            player.apply_gravity()
            player.check_platform_collision(platforms)

            if parkour_goal is not None and player.rect.colliderect(parkour_goal):
                parkour_won = True
                parkour_message = "成功踩到金塊！你完成了 Python 跑酷關卡！"

            if player.rect.top > bg_y:
                parkour_message = "你掉下去了！挑戰失敗，3 秒後回到起點..."
                pygame.display.update()
                time.sleep(3)
                start_game("parkour")

        draw_parkour_game()
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
