import math
from random import choice
from random import randint as rnd
import pygame

FPS = 60  # кадры в секунду

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (144, 238, 144)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # доступные цвета в игре

WIDTH = 800
HEIGHT = 600
g = 1  # ускорение свободного падения
k = 0.2  # коэффициэнт потерь скорости при столкновении
mu = 0.15  # коэффициэнт потерь скорости по ортогональной оси при столкновении


class Ball:  # снаряд
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - размер снаряда
        vx, vy - проекции скоростей
        lifetime - время жизни
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        # self.live = 30
        self.lifetime = 500

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy  # движение
        self.vy -= g  # действие гравитации
        self.lifetime -= 1  # таймер жизни
        if self.lifetime < 0:
            balls.remove(self)
        if self.x + self.r > WIDTH:  # столкновение справа
            self.x = 2 * WIDTH - self.x - self.r
            self.vx = -self.vx * (1 - k)
            self.vy = self.vy * (1 - mu)
        if self.y + self.r > HEIGHT:  # столкновение снизу
            if self.vy * self.vy < 5:  # остановка
                self.vy = 0
                self.y = HEIGHT - self.r
            else:
                self.y = 2 * HEIGHT - self.y - self.r
                self.vy = -self.vy * (1 - k)
                self.vx = self.vx * (1 - mu)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((obj.x) - (self.x)) ** 2 + ((obj.y) - (self.y)) ** 2 <= (self.r + obj.r) ** 2:
            balls.remove(self)
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREY
        self.x = 20
        self.y = 400
        self.leng = 30 + self.f2_power // 1.25

    def real_angle(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        self.an = math.atan2((y_mouse - 450), (x_mouse - 40))

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        rectangle_surface = pygame.Surface((WIDTH, HEIGHT))
        rectangle_surface.fill((255, 255, 255))
        old_center = rectangle_surface.get_rect().center
        pygame.draw.rect(rectangle_surface, self.color,
                         pygame.Rect(WIDTH // 2, HEIGHT // 2, self.leng + self.f2_power / 2, 10))
        rectangle_surface = pygame.transform.rotate(rectangle_surface, -self.an * 180 / math.pi)
        rect = rectangle_surface.get_rect()
        rect.center = (old_center[0] + self.x - WIDTH // 2, old_center[1] + self.y - HEIGHT // 2)
        self.screen.blit(rectangle_surface, rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.x = rnd(600, 780)  # координаты
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.live = True  # проверка жизни
        self.points = 0  # количество очков

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = RED
        self.points += 1
        target.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.real_angle()
    target.draw()
    gun.draw()
    print(gun.an)
    for b in balls:
        b.draw()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)

        gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()
    pygame.display.update()

pygame.quit()