from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты:
        body_color (tuple): Цвет объекта.
        position (tuple): Координаты позиции объекта.
    """

    def __init__(self, color, position: tuple):
        """Инициализация объекта с заданными цветом и позицией."""
        self.body_color = color
        self.position = position

    def draw(self):
        """Отрисовка объекта. Должен быть реализован в подклассах."""
        pass


class Snake(GameObject):
    """
    Класс, представляющий змею в игре.

    Атрибуты:
        length (int): Длина змеи.
        positions (list): Список координат, составляющих тело змеи.
        direction (tuple): Направление движения змеи.
        next_direction (tuple): Направление движения на следующем ходу.
        last (tuple): Последняя позиция тела змеи.
    """

    def __init__(self):
        """Инициализация змеи с начальной позицией и параметрами."""
        super().__init__(SNAKE_COLOR, (
            GRID_WIDTH * GRID_SIZE // 2, GRID_HEIGHT * GRID_SIZE // 2
        ))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змеи, если оно было изменено."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, is_increased):
        """
        Перемещение змеи на одну позицию вперед.

        Параметры:
            is_increased (bool): Указывает, увеличилась ли длина змеи после
            последнего шага.
        """
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if not is_increased:
            self.positions.pop()

    def draw(self):
        """Отрисовка тела змеи и затирание последнего сегмента."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змеи
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущую позицию головы змеи."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змею к начальной позиции и параметрам."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        self.position = (
            GRID_WIDTH * GRID_SIZE // 2,
            GRID_HEIGHT * GRID_SIZE // 2
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Наследует:
        GameObject: Базовый класс для игровых объектов.

    Атрибуты:
        position (tuple): Координаты яблока.
    """

    def __init__(self):
        """Инициализация яблока с цветом и случайной позицией."""
        super().__init__(APPLE_COLOR, (0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает яблоко в случайную позицию на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления направлением змеи.

    Параметры:
        game_object (Snake): Экземпляр змеи для обновления направления.

    Исключения:
        SystemExit: Выход из игры при закрытии окна.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция для запуска игры.

    Создает игровой цикл, в котором обрабатываются действия пользователя,
    обновляются позиции змеи и яблока, выполняется отрисовка и проверяются
    условия конца игры.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        head = snake.get_head_position()
        next_head = (
            (head[0] + snake.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + snake.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

        if next_head == apple.position:
            snake.move(True)
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
        else:
            snake.move(False)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
