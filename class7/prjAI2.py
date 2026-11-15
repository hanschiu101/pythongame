
import pygame
import sys
import random

pygame.init()

# ==============================
# 共用設定
# ==============================
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("雙遊戲合集")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Microsoft JhengHei", 24)


def draw_text(text, x, y, color=(255, 255, 255)):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


# ==============================
# Doodle Jump 物件
# ==============================
class Player:
    def __init__(self):
        self.rect = pygame.Rect(185, 500, 30, 30)
        self.speed = 5
        self.velocity_y = 0
        self.jump_power = -12
        self.gravity = 0.5

    def move(self, direction):
        self.rect.x += direction * self.speed

        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

    def gravity_move(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 10)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.collected = False

    def draw(self):
        if not self.collected:
            pygame.draw.circle(
                screen, (255, 220, 0),
                self.rect.center, 9
            )


# ==============================
# 弓箭遊戲物件
# ==============================
class Arrow:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 20, 4, 20)

    def move(self):
        self.rect.y -= 10

    def draw(self):
        pygame.draw.line(
            screen, (120, 60, 20),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.centerx, self.rect.top), 4
        )


# ==============================
# 主選單
# ==============================
def menu():
    while True:
        clock.tick(60)
        screen.fill((20, 30, 60))

        draw_text("雙遊戲合集", 130, 150, (255, 255, 0))
        draw_text("按 1：Doodle Jump", 90, 250)
        draw_text("按 2：弓箭射擊", 90, 310)
        draw_text("按 ESC：離開遊戲", 90, 370)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    doodle_jump()

                elif event.key == pygame.K_2:
                    archery_game()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ==============================
# Doodle Jump
# ==============================
def doodle_jump():

    player = Player()

    platforms = [
        Platform(170, 550)
    ]

    stars = []

    for i in range(10):
        x = random.randint(0, WIDTH - 60)
        y = 480 - i * 60
        platforms.append(Platform(x, y))
        stars.append(Star(x + 21, y - 28))

    score = 0

    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move(-1)

        if keys[pygame.K_RIGHT]:
            player.move(1)

        old_bottom = player.rect.bottom

        player.gravity_move()

        # 平台碰撞
        if player.velocity_y > 0:
            for platform in platforms:
                if (
                    old_bottom <= platform.rect.top
                    and player.rect.bottom >= platform.rect.top
                    and player.rect.right > platform.rect.left
                    and player.rect.left < platform.rect.right
                ):
                    player.rect.bottom = platform.rect.top
                    player.velocity_y = player.jump_power
                    break

        # 攝影機移動
        if player.rect.y < 250:
            offset = 250 - player.rect.y
            player.rect.y = 250

            for platform in platforms:
                platform.rect.y += offset

            for star in stars:
                star.rect.y += offset

            platforms = [
                p for p in platforms if p.rect.top < HEIGHT
            ]

            stars = [
                s for s in stars if s.rect.top < HEIGHT
            ]

            if platforms:
                highest = min(p.rect.top for p in platforms)

                while len(platforms) < 10:
                    x = random.randint(0, WIDTH - 60)
                    y = highest - 60
                    platforms.append(Platform(x, y))
                    stars.append(Star(x + 21, y - 28))
                    highest = y

        # 星星碰撞
        for star in stars:
            if not star.collected and player.rect.colliderect(star.rect):
                star.collected = True
                score += 1

        # 繪製
        for platform in platforms:
            platform.draw()

        for star in stars:
            star.draw()

        player.draw()

        draw_text(f"星星：{score}", 10, 10, (255, 255, 0))

        if player.rect.top > HEIGHT:
            draw_text("遊戲結束！按 ESC 回選單", 35, 280)
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return

        pygame.display.update()


# ==============================
# 弓箭射擊遊戲
# ==============================
def archery_game():

    player = pygame.Rect(185, 520, 30, 40)

    arrows = []

    targets = []

    for i in range(5):
        x = random.randint(30, 350)
        y = random.randint(50, 250)
        targets.append(pygame.Rect(x, y, 30, 30))

    score = 0

    while True:
        clock.tick(60)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_SPACE:
                    arrows.append(
                        Arrow(player.centerx, player.top)
                    )

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5

        # 弓箭移動
        for arrow in arrows[:]:
            arrow.move()

            if arrow.rect.bottom < 0:
                arrows.remove(arrow)
                continue

            for target in targets[:]:
                if arrow.rect.colliderect(target):
                    targets.remove(target)
                    arrows.remove(arrow)
                    score += 1

                    x = random.randint(30, 350)
                    y = random.randint(50, 250)
                    targets.append(
                        pygame.Rect(x, y, 30, 30)
                    )
                    break

        # 繪製玩家
        pygame.draw.rect(screen, (0, 150, 0), player)

        # 繪製弓箭
        for arrow in arrows:
            arrow.draw()

        # 繪製目標
        for target in targets:
            pygame.draw.circle(
                screen, (255, 0, 0),
                target.center, 15
            )

        draw_text(f"分數：{score}", 10, 10, (0, 0, 0))
        draw_text("空白鍵射箭 ESC回選單", 10, 40, (0, 0, 0))

        pygame.display.update()


# ==============================
# 執行遊戲
# ==============================
menu()
