######################載入套件/ import packages######################

import random
# random 是用來生成隨機數的套件

import array
import math
import os

import pygame
# pygame 是製作遊戲和多媒體程式的套件

import sys
# sys 可以用來結束程式


######################物件類別/ object class######################

class Brick:
    # 建立一個磚塊類別

    def __init__(self, x, y, width, height, color, kind="normal"):
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

        self.kind = kind
        # 設定磚塊種類，normal 是一般磚塊

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

            center_x = self.rect.centerx
            center_y = self.rect.centery

            if self.kind == "explosive":
                pygame.draw.circle(display_area, (35, 35, 35), (center_x, center_y), 5)
                pygame.draw.line(
                    display_area,
                    (255, 220, 0),
                    (center_x + 3, center_y - 3),
                    (center_x + 8, center_y - 7),
                    2
                )
                pygame.draw.circle(
                    display_area,
                    (255, 255, 255),
                    (center_x + 9, center_y - 8),
                    2
                )
            elif self.kind == "add":
                pygame.draw.line(
                    display_area,
                    (255, 255, 255),
                    (center_x - 7, center_y),
                    (center_x + 7, center_y),
                    3
                )
                pygame.draw.line(
                    display_area,
                    (255, 255, 255),
                    (center_x, center_y - 5),
                    (center_x, center_y + 5),
                    3
                )


class ExtraLife:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.speed_y = 3

    def move(self):
        self.rect.y += self.speed_y

    def draw(self, display_area):
        pygame.draw.rect(display_area, (35, 190, 90), self.rect)
        pygame.draw.line(
            display_area,
            (255, 255, 255),
            (self.rect.centerx - 5, self.rect.centery),
            (self.rect.centerx + 5, self.rect.centery),
            3
        )
        pygame.draw.line(
            display_area,
            (255, 255, 255),
            (self.rect.centerx, self.rect.centery - 5),
            (self.rect.centerx, self.rect.centery + 5),
            3
        )


class GorillaPaddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "kenney-monkey.png"
        )
        original_image = pygame.image.load(image_path).convert_alpha()
        image_height = height - 8
        image_width = round(
            image_height * original_image.get_width() / original_image.get_height()
        )
        self.image = pygame.transform.smoothscale(
            original_image,
            (image_width, image_height)
        )

    def draw(self, display_area):
        y = self.rect.y
        center_x = self.rect.centerx

        headphone_color = (35, 35, 45)
        pygame.draw.line(
            display_area,
            headphone_color,
            (center_x - 31, y + 24),
            (center_x - 29, y + 12),
            6
        )
        pygame.draw.line(
            display_area,
            headphone_color,
            (center_x - 29, y + 12),
            (center_x, y + 5),
            6
        )
        pygame.draw.line(
            display_area,
            headphone_color,
            (center_x, y + 5),
            (center_x + 29, y + 12),
            6
        )
        pygame.draw.line(
            display_area,
            headphone_color,
            (center_x + 29, y + 12),
            (center_x + 31, y + 24),
            6
        )

        image_x = center_x - self.image.get_width() // 2
        image_y = y + self.rect.height - self.image.get_height()
        display_area.blit(self.image, (image_x, image_y))

        for ear_x, accent_color in (
            (center_x - 34, (55, 210, 240)),
            (center_x + 34, (240, 80, 180))
        ):
            pygame.draw.circle(display_area, headphone_color, (ear_x, y + 25), 11)
            pygame.draw.circle(display_area, accent_color, (ear_x, y + 25), 6)


class Ball:
    # 建立一個球的類別

    max_paddle_bounces = 22
    explosion_duration = 900
    speed_increase = 0.3
    max_speed = 12

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

        self.game_over = False
        # 設定遊戲一開始尚未結束

        self.game_win = False
        # 設定遊戲一開始尚未獲勝

        self.paddle_bounce_count = 0
        self.exploding = False
        self.explosion_start = 0
        self.destroyed = False

    def draw(self, display_area):
        # 建立繪製球的函式
        # display_area 代表要繪製球的畫面

        if self.destroyed:
            return

        if self.exploding:
            elapsed = pygame.time.get_ticks() - self.explosion_start
            progress = min(elapsed / self.explosion_duration, 1)
            center = (int(self.x), int(self.y))
            radius = self.radius + int(progress * 35)

            pygame.draw.circle(display_area, (230, 45, 20), center, radius + 12)
            pygame.draw.circle(display_area, (255, 130, 0), center, radius + 5)
            pygame.draw.circle(display_area, (255, 240, 80), center, radius)

            directions = (
                (-1, -1), (0, -1), (1, -1), (-1, 0),
                (1, 0), (-1, 1), (0, 1), (1, 1)
            )
            for direction_x, direction_y in directions:
                start = (
                    center[0] + direction_x * (radius + 4),
                    center[1] + direction_y * (radius + 4)
                )
                end = (
                    center[0] + direction_x * (radius + 20),
                    center[1] + direction_y * (radius + 20)
                )
                pygame.draw.line(display_area, (255, 255, 220), start, end, 4)
            return

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

    def increase_speed(self):
        # 用畢氏定理計算球目前的總速度
        current_speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
        if current_speed == 0:
            return

        new_speed = min(current_speed + self.speed_increase, self.max_speed)
        # 同比例調整 X、Y 速度，維持球原本的方向
        speed_scale = new_speed / current_speed
        self.speed_x *= speed_scale
        self.speed_y *= speed_scale

    def check_collision(self, bg_x, bg_y, bricks, pad, life_drops):
        # 建立碰撞檢查球的函式
        if self.x - self.radius <= 0 or self.x + self.radius >= bg_x:
            self.speed_x = -self.speed_x
            self.increase_speed()
        if self.y-self.radius<=0:
            self.speed_y=-self.speed_y
            self.increase_speed()
        if (
            self.speed_y > 0
            and self.y + self.radius >= pad.rect.y
            and self.y - self.radius <= pad.rect.y + pad.rect.height
            and self.x + self.radius >= pad.rect.x
            and self.x - self.radius <= pad.rect.x + pad.rect.width
        ):
            self.speed_y=-abs(self.speed_y)
            self.increase_speed()
            self.paddle_bounce_count += 1
            if self.paddle_bounce_count > self.max_paddle_bounces:
                self.exploding = True
                self.explosion_start = pygame.time.get_ticks()
                self.is_moving = False
                return
        elif self.y + self.radius >= bg_y:
            self.game_over = True
            self.is_moving = False
        for brick in bricks[:]:
            # 使用清單複本，讓新增的磚塊不會在這一輪立刻被檢查
            if not brick.hit:
                dx = abs(self.x - (brick.rect.x + brick.rect.width / 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height / 2))
                if (
                    dx <= self.radius + brick.rect.width / 2
                    and dy <= self.radius + brick.rect.height / 2
                ):
                    brick.hit = True

                    play_next_fur_elise_note()

                    maybe_drop_extra_life(brick, life_drops)

                    if self.x < brick.rect.x or self.x > brick.rect.x + brick.rect.width:
                        self.speed_x = -self.speed_x
                    else:
                        self.speed_y = -self.speed_y
                    self.increase_speed()

                    if brick.kind == "explosive":
                        for nearby_brick in bricks:
                            if (
                                nearby_brick is not brick
                                and not nearby_brick.hit
                                and abs(nearby_brick.rect.x - brick.rect.x) <= brick_w + bricks_gap
                                and abs(nearby_brick.rect.y - brick.rect.y) <= brick_h + bricks_gap
                            ):
                                nearby_brick.hit = True
                                maybe_drop_extra_life(nearby_brick, life_drops)
                    elif brick.kind == "add":
                        add_random_brick(bricks, (brick.rect.x, brick.rect.y))


def add_random_brick(bricks, excluded_position):
    available_positions = []

    for col in range(bricks_col):
        current_rows = min(bricks_row + level - 1, max_bricks_row)
        for row in range(current_rows + 3):
            # 多預留三列空間，讓新方塊有位置可以生成
            x = col * (brick_w + bricks_gap) + 70
            y = row * (brick_h + bricks_gap) + 60
            position = (x, y)

            if position != excluded_position:
                position_is_used = False
                for brick in bricks:
                    if not brick.hit and brick.rect.topleft == position:
                        position_is_used = True
                        break

                if not position_is_used:
                    available_positions.append(position)

    if available_positions:
        x, y = random.choice(available_positions)
        color = (
            random.randint(20, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        bricks.append(Brick(x, y, brick_w, brick_h, color))
    else:
        print("沒有空位可以新增方塊")


def maybe_drop_extra_life(brick, life_drops):
    if random.randint(1, 100) <= 10:
        life_drops.append(ExtraLife(brick.rect.centerx, brick.rect.centery))


def all_bricks_hit(bricks):
    # return 會把檢查結果傳回呼叫這個函式的位置
    # 逐一檢查磚塊，找出還沒被打中的磚塊
    for brick in bricks:
        if not brick.hit:
            return False
    # 沒有找到未被打中的磚塊，代表全部清除了
    return True


def create_note_sound(frequency, duration):
    # 用 sin 波形產生一個音符，再轉成 pygame 可以播放的聲音
    sample_rate = 44100
    sample_count = int(sample_rate * duration)
    samples = array.array("h")

    for sample_number in range(sample_count):
        fade_in = min(sample_number / 100, 1)
        fade_out = min((sample_count - sample_number) / 1000, 1)
        volume = min(fade_in, fade_out)
        wave = math.sin(
            2 * math.pi * frequency * sample_number / sample_rate
        )
        samples.append(int(32767 * 0.25 * volume * wave))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def play_next_fur_elise_note():
    # 取得下一個音符；若上一個音符還在播放，就先放進佇列
    global fur_elise_index

    note = fur_elise_notes[fur_elise_index]
    if fur_elise_channel.get_busy():
        fur_elise_queue.append(note)
    else:
        fur_elise_channel.play(note)

    fur_elise_index = (fur_elise_index + 1) % len(fur_elise_notes)


def update_fur_elise_music():
    # 播完目前音符後，接著播放佇列中的音符
    if not fur_elise_channel.get_busy() and fur_elise_queue:
        fur_elise_channel.play(fur_elise_queue.pop(0))


######################定義函式區/ define functions######################

# 這個區域用來放置其他需要使用的函式
# 目前沒有另外建立函式


######################初始化設定/ initialize settings######################

pygame.mixer.pre_init(44100, -16, 1, 512)
# 設定音效格式，必須在 pygame.init() 之前呼叫

pygame.init()
# 開始使用 pygame 的功能

FPS = pygame.time.Clock()
# 建立一個 Clock 物件
# 用來控制遊戲執行的速度


######################載入圖片/ load images######################

# 這個區域用來載入遊戲需要的圖片
# 目前沒有使用圖片


######################音樂設定/ music settings######################

fur_elise_frequencies = {
    "E5": 659.25,
    "D#5": 622.25,
    "B4": 493.88,
    "D5": 587.33,
    "C5": 523.25,
    "A4": 440.00,
    "C4": 261.63,
    "E4": 329.63,
    "G#4": 415.30
}
fur_elise_sequence = [
    "E5", "D#5", "E5", "D#5", "E5", "B4", "D5", "C5", "A4",
    "C4", "E4", "A4", "B4", "E4", "G#4", "B4", "C5",
    "E5", "D#5", "E5", "D#5", "E5", "B4", "D5", "C5", "A4"
]
fur_elise_notes = [
    create_note_sound(fur_elise_frequencies[note], 0.16)
    for note in fur_elise_sequence
]
fur_elise_channel = pygame.mixer.Channel(0)
fur_elise_queue = []
fur_elise_index = 0


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
# 先在這個畫面上繪圖，之後移動貼到視窗來製作震動效果
game_surface = pygame.Surface(bg_size)


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

def create_bricks():
    # 建立一組新的磚塊，讓重新開始時可以重新使用
    new_bricks = []

    for col in range(bricks_col):
        for row in range(bricks_row):
            x = col * (brick_w + bricks_gap) + 70
            y = row * (brick_h + bricks_gap) + 60

            kind = "normal"
            if col == 2 and row == 1:
                kind = "explosive"
                color = (230, 65, 45)
            elif col == 7 and row == 1:
                kind = "add"
                color = (45, 170, 70)
            else:
                color = (
                    random.randint(20, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

            brick = Brick(x, y, brick_w, brick_h, color, kind)
            new_bricks.append(brick)

    return new_bricks


bricks = create_bricks()
# 建立遊戲一開始的磚塊列表


######################顯示文字設定/ text display settings######################

# 這個區域用來設定遊戲中的文字
# 目前沒有設定文字


######################底板設定/ paddle settings######################

pad_w = 112
pad_h = 64
pad = GorillaPaddle(bg_x // 2 - pad_w // 2, bg_y - pad_h - 12, pad_w, pad_h)
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


######################遊戲結束與獲勝設定/ game over and win settings######################

game_over_font = pygame.font.SysFont("Microsoft JhengHei", 48)
game_over_text = game_over_font.render("遊戲結束", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(bg_x // 2, bg_y // 2))
game_win_text = game_over_font.render("恭喜獲勝！", True, (255, 255, 255))
game_win_rect = game_win_text.get_rect(center=(bg_x // 2, bg_y // 2))

restart_font = pygame.font.SysFont("Microsoft JhengHei", 30)
restart_text = restart_font.render("重新開始", True, (255, 255, 255))
restart_button_rect = pygame.Rect(0, 0, 220, 54)
restart_button_rect.center = (bg_x // 2, bg_y // 2 + 80)


def reset_game():
    global bricks, ball, fur_elise_queue, fur_elise_index

    pad.rect.x = bg_x // 2 - pad.rect.width // 2
    bricks = create_bricks()
    ball = Ball(
        pad.rect.centerx,
        pad.rect.y - ball_radius,
        ball_radius,
        ball_color
    )
    fur_elise_channel.stop()
    fur_elise_queue = []
    fur_elise_index = 0


######################主程式/ main program######################

while True:
    # 持續執行遊戲主程式
    # while True 會讓遊戲一直執行

    FPS.tick(60)
    # 控制遊戲速度
    # 遊戲最多每秒執行 60 次

    update_fur_elise_music()

    game_surface.fill((0, 0, 0))
    # 清除背景
    # 使用黑色填滿整個遊戲畫面

    if not ball.game_over and not ball.game_win and not ball.exploding:
        mos_x, mos_y = pygame.mouse.get_pos()
        # 取得滑鼠的座標
        # mos_x 是滑鼠目前的 X 座標
        # mos_y 是滑鼠目前的 Y 座標

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

            ball.check_collision(bg_x, bg_y, bricks, pad)
            # 呼叫 check_collision() 函式檢查球是否碰到邊界或磚塊
            # bg_x、bg_y 是遊戲畫面的寬度和高度
            # bricks 是磚塊列表
            # pad 是底板物件

            if (
                not ball.game_over
                and not ball.exploding
                and all_bricks_hit(bricks)
            ):
                ball.game_win = True
                ball.is_moving = False

    # 將球的 Y 座標設定為底板上方

    for event in pygame.event.get():
        # 取得所有遊戲事件
        # 檢查遊戲中發生的事件
        # 例如關閉視窗、鍵盤或滑鼠事件

        if event.type == pygame.QUIT:
            # 判斷是否按下關閉視窗

            sys.exit()
            # 結束遊戲程式
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                event.button == 1
                and (ball.game_over or ball.game_win)
                and restart_button_rect.collidepoint(event.pos)
            ):
                reset_game()
            elif (
                not ball.game_over
                and not ball.game_win
                and not ball.exploding
                and not ball.is_moving
            ):
                # 判斷是否按下滑鼠按鈕，讓球開始移動
                ball.is_moving = True

    for brick in bricks:
        # 逐一取得磚塊列表中的磚塊
        # 每次取得一個磚塊

        brick.draw(game_surface)
        # 將每一個磚塊畫到遊戲畫面上

    pad.draw(game_surface)
    # 將底板畫到遊戲畫面上

    ball.draw(game_surface)
    # 將球畫到遊戲畫面上

    shake_x = 0
    shake_y = 0
    if ball.exploding:
        explosion_elapsed = pygame.time.get_ticks() - ball.explosion_start
        if explosion_elapsed >= ball.explosion_duration:
            ball.exploding = False
            ball.destroyed = True
            if all_bricks_hit(bricks):
                ball.game_win = True
            else:
                ball.game_over = True
        else:
            shake_strength = max(0, 10 - explosion_elapsed // 90)
            shake_x = random.randint(-shake_strength, shake_strength)
            shake_y = random.randint(-shake_strength, shake_strength)

    screen.fill((0, 0, 0))
    screen.blit(game_surface, (shake_x, shake_y))

    if ball.game_win:
        screen.blit(game_win_text, game_win_rect)
    elif ball.game_over:
        screen.blit(game_over_text, game_over_rect)

    if ball.game_over or ball.game_win:
        pygame.draw.rect(screen, (40, 130, 75), restart_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), restart_button_rect, 2)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

    pygame.display.update()
    # 更新遊戲視窗
    # 將這一幀畫好的內容顯示出來
