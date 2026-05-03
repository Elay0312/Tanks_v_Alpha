from Units import Tank
from tkinter import NW
from random import randint
from Missiles_collection import check_missiles_collection
import world

id_screen_text = 0
_tanks = []
_canvas = None
reload_score = 1

def _update_screen_text():
    _canvas.itemconfig(id_screen_text, text = _get_screen_text())
    _canvas.itemconfig(hp_text, text=f'Прочность машины: {Tank.get_hp(self = player)}')
    _canvas.itemconfig(ammo_text, text=f'Cнаряды: {Tank._get_ammo(player)}')
    _canvas.itemconfig(speed_text, text=f'Скорость:{Tank.get_speed(player) * 10} км/ч')
    _canvas.itemconfig(fuel_text, text=f'Топливо:{Tank._get_fuel(player)}')

def _get_screen_text():
    if get_player().is_destroyed():
        return 'Потрачено'
    if len(_tanks) == 1:
        return 'Победа'
    return f'Осталось врагов: {len(_tanks) - 1}'

def initialize(canv):
    global _canvas, id_screen_text, hp_text, player, reload_text, ammo_text, speed_text, fuel_text
    _canvas = canv

    player = spawn(False)
    # enemy = spawn(True).set_target(player)
    # spawn(True).set_target(player)
    # for i in range(5):
    #     spawn(True).set_target(get_player())

    id_screen_text = _canvas.create_text(10,10, text = _get_screen_text(), font = ('TkDefaultFont', 20, 'bold'), fill = 'white', anchor = NW)
    hp_text = _canvas.create_text(10, 60, text=f'Прочность машины: {Tank.get_hp(self = player)}', font=('TkDefaultFont', 20, 'bold'),
                                         fill='white', anchor=NW)
    ammo_text = _canvas.create_text(610, 10, text=f'Cнаряды: {Tank._get_ammo(player)}',
                                  font=('TkDefaultFont', 20, 'bold'),
                                  fill='white', anchor=NW)
    speed_text = _canvas.create_text(560, 60, text=f'Скорость:{Tank.get_speed(player) * 10} км/ч', font=('TkDefaultFont', 20, 'bold'),
                                         fill='white', anchor=NW)

    fuel_text = _canvas.create_text(10, 110, text=f'Топливо:{Tank._get_fuel(player)}',
                                     font=('TkDefaultFont', 20, 'bold'),
                                     fill='white', anchor=NW)

def get_player():
    return _tanks[0]

def update():
    _update_screen_text()
    start = len(_tanks) - 1
    for i in range(start, -1, -1):
        if _tanks[i].is_destroyed() and i != 0:
            del _tanks[i]
        else:
            _tanks[i].update()
            check_collision(_tanks[i])
            check_missiles_collection(_tanks[i])

def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False

def spawn(is_bot = True):
    cols = world.get_cols()
    rows = world.get_rows()
    while True:
        col = randint(1, cols - 1)
        row = randint(1, rows - 1)

        if world.get_block(row, col) != world.GROUND:
            continue

        t = Tank(_canvas, row, col,bot = is_bot)
        if not check_collision(t):
            _tanks.append(t)
            return t