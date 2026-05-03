import Missiles_collection
from tkinter import *
import world
import tanks_collection
import Texture

KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN = 37, 39, 38, 40

KEY_W = 87
KEY_S = 83
KEY_A = 65
KEY_D = 68
SPACE = 32
FPS = 60


def key_press(event):
    player = tanks_collection.get_player()

    if player.is_destroyed():
        return
    if event.keycode == SPACE:
        player.fire()
    if event.keycode == KEY_W:
        player.forward()

    if event.keycode == KEY_S:
        player.backward()

    if event.keycode == KEY_A:
        player.left()

    if event.keycode == KEY_D:
        player.right()

    if event.keycode == KEY_UP:
        world.move_camera(0, -5)
    if event.keycode == KEY_DOWN:
        world.move_camera(0,5)
    if event.keycode == KEY_RIGHT:
        world.move_camera(5,0)
    if event.keycode == KEY_LEFT:
        world.move_camera(-5,0)

def update():

    tanks_collection.update()
    Missiles_collection.update()


    player = tanks_collection.get_player()

    world.set_camera_xy(player.get_x() - world.SCREEN_WIDTH//2 + player.get_size()//2, player.get_y() - world.SCREEN_HEIGHT//2 + player.get_size()//2)

    world.update_map()

    w.after(1000//FPS, update)
def load_textures():


    Texture.load('tank_up', '../img/tank_up.png')
    Texture.load('tank_down', '../img/tank_down.png')
    Texture.load('tank_right', '../img/tank_right.png')
    Texture.load('tank_left', '../img/tank_left.png')

    Texture.load('tank_up_player', '../img/tank_up_player.png')
    Texture.load('tank_down_player', '../img/tank_down_player.png')
    Texture.load('tank_right_player', '../img/tank_right_player.png')
    Texture.load('tank_left_player', '../img/tank_left_player.png')

    Texture.load(world.BRICK, '../img/brick.png')
    Texture.load(world.CONCRETE, '../img/wall.png')
    Texture.load(world.WATER, '../img/water.png')
    Texture.load(world.GROUND, '../img/ground.png')
    Texture.load(world.MISSLE, '../img/bonus.png')
    Texture.load(world.HEAL, '../img/heal.png')
    Texture.load(world.FUEL_BOOST, '../img/f_boost.png')
    Texture.load(world.SPEED_BOOST, '../img/speed.png')
    Texture.load(world.EXPLOSION, '../img/explosion.png')

    Texture.load('missle_up', '../img/missile_up.png')
    Texture.load('missle_down', '../img/missile_down.png')
    Texture.load('missle_left', '../img/missile_left.png')
    Texture.load('missle_right', '../img/missile_right.png')

w = Tk()

load_textures()

w.title('Танки на минималках 2.0')
canv = Canvas(w, width = world.SCREEN_WIDTH, height = world.SCREEN_HEIGHT, bg = 'light green')
canv.pack()

world.initialaze(canv = canv)
tanks_collection.initialize(canv= canv)
Missiles_collection.initialize(canv = canv)


w.bind('<KeyPress>', key_press)
update()
w.mainloop()

