from tkinter import NW
import world
from hitbox import Hitbox
import Texture as skin
from random import randint, random
import Missiles_collection

class Unit:
    def __init__(self,canvas,x,y,speed, pad ,bot, default_image):

        self._destroyed = False
        self._boosted = False

        self._default_image = default_image
        self._left_image = default_image
        self._right_image = default_image
        self._forward_image = default_image
        self._backward_image = default_image

        self._bot = bot
        self._canvas = canvas

        self._water_speed = speed / 2
        self._usual_speed = speed
        self._speed_boost = speed * 2
        self._hp = 100
        self._speed = speed
        self._xp = 0
        self._x = x
        self._y = y
        self._fuel = 20000
        self._vx = 0
        self._vy = 0
        self._dx = 0
        self._dy = 0
        self._do_explosion = False

        # if self._x < 0:
        #     self._x = 0
        # if self._y < 0:
        #     self._y = 0

        self._hitbox = Hitbox(x, y, world.BLOCK_SIZE, world.BLOCK_SIZE, padding = pad)

        self._create()

    def damage(self, value):
        self._hp -= value
        if self._hp <= 0:
            self.destroy()

    def is_destroyed(self):
        return self._destroyed

    def destroy(self):
        self._destroyed = True
        self.stop()
        self._speed = 0

    def _create(self):
        self._id = self._canvas.create_image(self._x,
                                             self._y,
                                             image=skin.get(self._default_image),
                                             anchor=NW)

    def forward(self):

        self._vx = 0
        self._vy = -1
        self._fuel -= self._speed
        self._canvas.itemconfig(self._id, image= skin.get(self._forward_image))

    def backward(self):
        self._vx = 0
        self._vy = 1
        self._fuel -= self._speed
        self._canvas.itemconfig(self._id, image= skin.get(self._backward_image))

    def left(self):
        self._vx = -1
        self._vy = 0
        self._fuel -= self._speed
        self._canvas.itemconfig(self._id, image=skin.get(self._left_image))

    def right(self):
        self._vx = 1
        self._vy = 0
        self._fuel -= self._speed
        self._canvas.itemconfig(self._id, image=skin.get(self._right_image))

    def stop(self):

        self._vx = 0
        self._vy = 0

    def update(self):

        if self._bot:
            self._AI()

        self._dx = self._vx * self._speed
        self._dy = self._vy * self._speed
        self._x += self._dx
        self._y += self._dy
        self._update_hitbox()
        self._check_map_collision()
        self._repaint()

    def _AI(self):
        pass

    def _set_usual_speed(self):

        self._speed = self._usual_speed

    def _set_water_speed(self):

        self._speed = self._water_speed

    def _take_hp(self):
        self._hp += 10
        if self._hp > 200:
            self._hp = 200

    def get_do_explosion(self):
        return self._do_explosion

    def _set_speed_boost(self):

        self._speed = self._speed_boost

    def _take_ammo(self):
        self._ammo += 10
        if self._ammo > 100:
            self._ammo = 100

    def _update_hitbox(self):
        self._hitbox.moveto(self._x, self._y)

    def _check_map_collision(self):
        details = {}
        result = self._hitbox.check_map_collision(details)
        if result:
            self._on_map_collision(details)
        else:
            if self._boosted == True:
                self._set_speed_boost()
            if self._boosted == False:
                self._set_usual_speed()

    def _on_map_collision(self, details):
        if world.WATER in details and len(details) == 1:
            if self._boosted == False:
                self._set_water_speed()
                print(f'Вода = {self._speed}')
            elif self._boosted == True:
                self._set_usual_speed()
            return self._speed

        elif world.BRICK in details:
            self._undo_move()
            if self._bot:
                self._change_orientation()

        elif world.CONCRETE in details:
            self._undo_move()
            if self._bot:
                self._change_orientation()

        elif world.MISSLE in details:
            pos = details[world.MISSLE]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self._take_ammo()

        elif world.EXPLOSION in details:
            pos = details[world.EXPLOSION]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self._do_explosion = True

        elif world.HEAL in details:
            pos = details[world.HEAL]
            print(self._hp)
            if world.take(pos['row'], pos['col']) != world.AIR:
                self._take_hp()
        elif world.SPEED_BOOST in details:
            if self._boosted == False:
                pos = details[world.SPEED_BOOST]
                if world.take(pos['row'], pos['col']) != world.AIR:
                    self._boosted = True
                    print(f'Скорость = {self._speed}')
            elif self._boosted == True:
                pass
        else:
            self._undo_move()
            if self._bot:
                self._change_orientation()

    def _no_map_collision(self):
        self._set_usual_speed()

    def _repaint(self):
        screen_x = world.get_screen_x(self._x)
        screen_y = world.get_screen_y(self._y)
        self._canvas.moveto(self._id, x = screen_x, y = screen_y)

    def _undo_move(self):

        if self._dx == 0 and self._dy == 0:
            return

        self._x -= self._dx
        self._y -= self._dy
        self._update_hitbox()
        self._repaint()
        self._dx = 0
        self._dy = 0

    def intersects(self, other_unit):
        value = self._hitbox.intersect(other_unit._hitbox)
        if value:
            self._on_intersects(other_unit)

        return value

    def _on_intersects(self, other_unit):
        self._undo_move()

    def _change_orientation(self):
        rand = randint(0,3)
        if rand == 0:
            self.left()
        elif rand == 1:
            self.right()
        elif rand == 2:
            self.forward()
        elif rand == 3:
            self.backward()

    def get_hp(self):
        return self._hp

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_vx(self):
        return self._vx

    def get_vy(self):
        return self._vy

    def get_speed(self):
        return self._speed

    def get_size(self):
        return world.BLOCK_SIZE

    def is_bot(self):
        return self._bot

    def __del__(self):
        try:
            self._canvas.delete(self._id)
        except Exception:
            pass

class Tank(Unit):
    def __init__(self, canvas, row, col, bot = True):
        super().__init__(canvas,
                         col*world.BLOCK_SIZE,
                         row*world.BLOCK_SIZE,
                         4,
                         8,
                         bot,
                         'tank_up' )

        if bot:
            self._forward_image = 'tank_up'
            self._backward_image = 'tank_down'
            self._left_image = 'tank_left'
            self._right_image = 'tank_right'
        else:
            self._forward_image = 'tank_up_player'
            self._backward_image = 'tank_down_player'
            self._left_image = 'tank_left_player'
            self._right_image = 'tank_right_player'

        self.forward()
        self._ammo = 80
        self._usual_speed = self._speed
        self._water_speed = self._speed//2
        self._target = None
        self._can_fire = True

    def set_target(self, target):
        self._target = target

    def _AI_fire(self):
        if self._target is None:
            return
        center_x = self.get_x() + self.get_size() // 2
        center_y = self.get_y() + self.get_size() // 2
        target_center_x = self._target.get_x() + self.get_size() // 2
        target_center_y = self._target.get_y() + self.get_size() // 2

        row = world.get_row(center_y)
        col = world.get_col(center_x)
        row_target = world.get_row(target_center_y)
        col_target = world.get_col(target_center_x)

        if row == row_target:
            if col_target < col:
                self.left()
                self.fire()
            else:
                self.right()
                self.fire()
        elif col == col_target:
            if row_target < row:
                self.forward()
                self.fire()
            else:
                self.backward()
                self.fire()

    def _AI_goto_target(self):

        if randint(1, 2) == 1:
            if self._target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self._target.get_y() < self.get_y():
                self.forward()
            else:
                self.backward()

    def _set_can_fire(self):
        self._can_fire = True

    def _reload(self):
        self._can_fire = False
        self._canvas.after(2000, self._set_can_fire)

    def fire(self):
        if self._can_fire:
            if self._ammo > 0:
                self._ammo -= 1
                print(self._speed)
                Missiles_collection.fire(self)
                self._reload()
        else:
            pass

    def _get_ammo(self):
        return self._ammo

    def _get_fuel(self):
        return self._fuel

    def _take_ammo(self):
        self._ammo += 10
        if self._ammo > 100:
            self._ammo = 100

    def _set_usual_speed(self):

        self._speed = self._usual_speed

    def _no_map_collision(self):
        pass

    def _on_intersects(self, other_unit):
        super()._on_intersects(other_unit)
        if self._bot:
            self._change_orientation()

    def _AI(self):

        if randint(1, 30) == 1:
            if randint(1, 10) < 9 and self._target is not None:
                self._AI_goto_target()
            else:
                self._change_orientation()
        elif randint(1,30) == 1:
            self._AI_fire()
        elif randint(1,100) == 1:
            self.fire()

    def _take_hp(self):
        self._hp += 10
        if self._hp > 200:
            self._hp = 200

class Missle(Unit):

    def __init__(self,canvas,owner):
        super().__init__(canvas,owner.get_x(),owner.get_y(),20,20,False,'missle_up')

        self._forward_image = 'missle_up'
        self._backward_image = 'missle_down'
        self._left_image = 'missle_left'
        self._right_image = 'missle_right'
        self._owner = owner
        self._target = None
        self._ammo = 80
        self._hitbox.set_blacklist([world.CONCRETE, world.BRICK])

        if owner.get_vx() == 1 and owner.get_vy() == 0:
            self.right()
        if owner.get_vx() == -1 and owner.get_vy() == 0:
            self.left()
        if owner.get_vx() == 0 and owner.get_vy() == 1:
            self.backward()
        if owner.get_vx() == 0 and owner.get_vy() == -1:
            self.forward()

        self._x += owner.get_vx() * self.get_size() // 2
        self._y += owner.get_vy() * self.get_size() // 2

    def get_owner(self):
        return self._owner

    def _on_map_collision(self, details):
        if world.BRICK in details:
            row = details[world.BRICK]['row']
            col = details[world.BRICK]['col']
            world.destroy(row, col)
            self.destroy()

        if world.CONCRETE in details:
            self.destroy()