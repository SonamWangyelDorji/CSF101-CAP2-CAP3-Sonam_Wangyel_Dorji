import pytest
import pygame
from stellar_showdown import yellow_handle_movement, red_handle_movement, BORDER, WIDTH, HEIGHT, home_screen

# Mocking the spaceship objects for testing
class MockSpaceship:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


#Mocking the surface for testing
class MockSurface:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def blit(self, text, position):
        pass

    def update(self):
        pass
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT)) 
WIN = MockSurface(WIDTH, HEIGHT)

#Mocking health font 
@pytest.fixture
def mock_health_font(monkeypatch):
    class MockFont:
        def render(self, text, _, color):
            return MockSurface(100, 50) 

    monkeypatch.setattr(pygame.font, 'SysFont', lambda *args: MockFont())


# Mocking the pygame.mouse module
class MockMouse:
    def get_pos(self):
        return (0, 0)

    def get_pressed(self):
        return (0, 0, 0)

pygame.mouse = MockMouse()

def test_home_screen(mock_health_font, monkeypatch):
    pygame_event_quit = pygame.event.Event(pygame.QUIT)
    pygame_event_mouse = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})

    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame_event_quit, pygame_event_mouse])

    with pytest.raises(SystemExit):
        home_screen()
    assert WIN.width == WIDTH
    assert WIN.height == HEIGHT


def yellow_handle_movement(keys_pressed, yellow):
    VEL = 5
    if pygame.K_a in keys_pressed and keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if pygame.K_d in keys_pressed and keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if pygame.K_w in keys_pressed and keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if pygame.K_s in keys_pressed and keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    VEL = 5
    if pygame.K_LEFT in keys_pressed and keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if pygame.K_RIGHT in keys_pressed and keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if pygame.K_UP in keys_pressed and keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if pygame.K_DOWN in keys_pressed and keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

@pytest.fixture
def yellow_spaceship():
    return MockSpaceship(x=100, y=300, width=55, height=40)

@pytest.fixture
def red_spaceship():
    return MockSpaceship(x=700, y=300, width=55, height=40)




# Testing yellow spaceship movement
def test_yellow_movement_left(yellow_spaceship):
    keys_pressed = {pygame.K_a: True}
    yellow_handle_movement(keys_pressed, yellow_spaceship)
    assert yellow_spaceship.x == 95

def test_yellow_movement_right(yellow_spaceship):
    keys_pressed = {pygame.K_d: True}
    yellow_handle_movement(keys_pressed, yellow_spaceship)
    assert yellow_spaceship.x == 105

def test_yellow_movement_up(yellow_spaceship):
    keys_pressed = {pygame.K_w: True}
    yellow_handle_movement(keys_pressed, yellow_spaceship)
    assert yellow_spaceship.y == 295

def test_yellow_movement_down(yellow_spaceship):
    keys_pressed = {pygame.K_s: True}
    yellow_handle_movement(keys_pressed, yellow_spaceship)
    assert yellow_spaceship.y == 305



# Testing red spaceship movement
def test_red_movement_left(red_spaceship):
    keys_pressed = {pygame.K_LEFT: True}
    red_handle_movement(keys_pressed, red_spaceship)
    assert red_spaceship.x == 695

def test_red_movement_right(red_spaceship):
    keys_pressed = {pygame.K_RIGHT: True}
    red_handle_movement(keys_pressed, red_spaceship)
    assert red_spaceship.x == 705

def test_red_movement_up(red_spaceship):
    keys_pressed = {pygame.K_UP: True}
    red_handle_movement(keys_pressed, red_spaceship)
    assert red_spaceship.y == 295

def test_red_movement_down(red_spaceship):
    keys_pressed = {pygame.K_DOWN: True}
    red_handle_movement(keys_pressed, red_spaceship)
    assert red_spaceship.y == 305

#Testing Home Screen of the game
def test_home_screen():
    with pytest.raises(SystemExit):
        home_screen()


if __name__ == '__main__':
    pytest.main()
