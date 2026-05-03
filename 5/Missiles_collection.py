from Units import Missle
_missles = []
_canvas = None

def initialize(canv):
    global _canvas
    _canvas = canv


def fire(owner):
    m = Missle(_canvas, owner)
    _missles.append(m)

def update():
    start = len(_missles) - 1
    for i in range(start, -1, -1):
        if _missles[i].is_destroyed():
            del _missles[i]
        else:
            _missles[i].update()

def check_missiles_collection(tank):
    for missle in _missles:
        if missle.get_owner() == tank:
            continue
        if missle.intersects(tank):
            missle.destroy()
            tank.damage(25)

            return

