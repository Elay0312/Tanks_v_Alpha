from tkinter import PhotoImage, NW
from hitbox import Hitbox
from random import randint
import world
import Texture as skin

class Tank:

    __count = 0

    def __init__(self,canvas,x,y,model = 'Золотая Заря',ammo = 100, speed = 10,
                #  file_up='../img/tank_up.png',
                #     file_down = '../img/tank_down.png',
                #
                # file_left = '../img/tank_left.png',
                # file_right = '../img/tank_right.png',
                 bot = True):

        self.__bot = bot
        self.__canvas = canvas
        Tank.__count += 1

        self.__model = model
        self.__water_speed = speed / 2
        self.__usual_speed = speed
        self.__speed_boost = speed * 2
        self.__hp = 100
        self.__speed = speed
        self.__xp = 0
        self.__ammo = ammo
        self.__x = x
        self.__y = y
        self.__fuel = 20000
        self.__vx = 0
        self.__vy = 0
        self.__dx = 0
        self.__dy = 0

        if self.__x < 0:
            self.__x = 0
        if self.__y < 0:
            self.__y = 0

        # self.__skin_up = PhotoImage(file=file_up)
        # self.__skin_down = PhotoImage(file=file_down)
        # self.__skin_left = PhotoImage(file=file_left)
        # self.__skin_right = PhotoImage(file=file_right)

        self.__hitbox = Hitbox(x, y, self.get_size(), self.get_size(), padding = 8)

        self.__create()
        self.__target = None

    def __take_ammo(self):
        self.__ammo += 10
        if self.__ammo > 100:
            self.__ammo = 100

    def __take_hp(self):
        self.__hp += 10
        if self.__hp > 200:
            self.__hp = 200

    def intersects(self, other_tank):
        value = self.__hitbox.intersect(other_tank._hitbox)
        if value:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()
        return value

    def __take_explosion(self, row, col):
        world.destroy(row + 1, col)
        world.destroy(row - 1, col)
        world.destroy(row, col + 1)
        world.destroy(row, col - 1)
        world.destroy(row + 1, col + 1)
        world.destroy(row + 1, col - 1)
        world.destroy(row - 1, col + 1)
        world.destroy(row - 1, col - 1)

    def __set_usual_speed(self):

        self.__speed = self.__usual_speed

    def __set_water_speed(self):

        self.__speed = self.__water_speed

    def __set_speed_boost(self):

        self.__speed = self.__speed_boost

    def __check_map_collision(self):
        details = {}
        if self.__speed != self.__speed_boost:
            self.__set_usual_speed()
        result = self.__hitbox.check_map_collision(details)

        if result:
            self.__on_map_collision(details)

    def __on_map_collision(self, details):
        if world.WATER in details and len(details) == 1:
            if self.__speed == self.__speed_boost:
                self.__set_usual_speed()
                print(self.__speed)
            else:
                self.__set_water_speed()
                print(self.__speed)
            return self.__speed

        elif world.BRICK in details:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

        elif world.CONCRETE in details:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

        elif world.MISSLE in details:
            pos = details[world.MISSLE]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self.__take_ammo()

        elif world.EXPLOSION in details:
            pos = details[world.EXPLOSION]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self.__take_explosion(pos['row'], pos['col'])

        elif world.HEAL in details:
            pos = details[world.HEAL]
            print(self.__hp)
            if world.take(pos['row'], pos['col']) != world.AIR:
                self.__take_hp()
        elif world.SPEED_BOOST in details:
            pos = details[world.SPEED_BOOST]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self.__set_speed_boost()
                print(self.__speed)
        else:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

    def __check_out_of_world(self):
        if self.__hitbox.left < 0 or self.__hitbox.top < 0 or self.__hitbox.right >= world.get_width() or self.__hitbox.bottom >= world.get_height():
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

    def set_target(self, target):
        self.__target = target

    def __AI_goto_target(self):

        if randint(1,2) == 1:
            if self.__target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self.__target.get_y() < self.get_y():
                self.forward()
            else:
                self.backward()


    def __AI(self):

        if randint(1,30) == 1:
            if randint(1,10) < 9 and self.__target is not None:
                self.__AI_goto_target()
            else:
                self.__AI_change_orientation()

    def __AI_change_orientation(self):
        rand = randint(0,3)
        if rand == 0:
            self.left()
        elif rand == 1:
            self.right()
        elif rand == 2:
            self.forward()
        else:
            self.backward()

    def fire(self):
        if self.__ammo > 0:
            self.__ammo -= 1
            print('ОГОНЬ!')

    def info(self):
        info = (f'Докладывает Связист Медведев  - Модель техники <<{self.__model}>> , Прочность техники: {self.__hp}, Накопилось {self.__xp} '
                f'боевого потенциала, Осталось {self.__ammo} боеголовок, Координаты Х({self.__x}), У({self.__y})! ')
        print(info)

    def forward(self):

        self.__vx = 0
        self.__vy = -1
        self.__canvas.itemconfig(self.__id, image= skin.get('tank_up'))
        self.__repaint()

    def backward(self):
        self.__vx = 0
        self.__vy = 1
        self.__canvas.itemconfig(self.__id, image= skin.get('tank_down'))
        self.__repaint()

    def left(self):
        self.__vx = -1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id, image=skin.get('tank_left'))
        self.__repaint()

    def right(self):
        self.__vx = 1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id, image=skin.get('tank_right'))
        self.__repaint()

    def stop(self):

        self.__vx = 0
        self.__vy = 0

    def __create(self):
        self.__id = self.__canvas.create_image(self.__x, self.__y, image= skin.get('tank_up'), anchor=NW)


    def __repaint(self):
        self.__canvas.moveto(self.__id, x = world.get_screen_x(self.__x), y = world.get_screen_y(self.__y))

    def __update_hitnox(self):
        self.__hitbox.moveto(self.__x, self.__y)

    def intersects(self, other_tank):
        value = self.__hitbox.intersect(other_tank._hitbox)
        if value:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()
        return value

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_ammo(self):
        return self.__ammo

    def get_model(self):
        return self.__model

    def get_hp(self):
        return self.__hp

    def get_xp(self):
        return self.__xp

    def get_fuel(self):
        return self.__fuel

    def get_speed(self):
        return self.__speed

    @staticmethod
    def get_quantity():
        return Tank.__count

    def get_size(self):
        return skin.get('tank_up').width()

    def __undo_move(self):

        if self.__dx == 0 and self.__dy == 0:
            return

        self.__x -= self.__dx
        self.__y -= self.__dy
        self.__fuel += self.__speed
        self.__update_hitnox()
        self.__repaint()
        self.__dx = 0
        self.__dy = 0

    def update(self):

        if self.__fuel >= self.__speed:

            if self.__bot:
                self.__AI()

            self.__dx = self.__vx * self.__speed
            self.__dy = self.__vy * self.__speed
            self.__x += self.__dx
            self.__y += self.__dy
            self.__fuel -= self.__speed
            self.__update_hitnox()

            self.__check_out_of_world()
            self.__check_map_collision()

            self.__repaint()

    def __del__(self):
        print('Лишний танк удалён')
        try:
            self.__canvas.delete(self.__id)
        except Exception:
            pass

    def __str__(self):
        # return (f'Докладывает Связист Медведев  - Модель техники <<{self.__model}>> , Прочность техники: {self.__hp}, Накопилось {self.__xp} '
        #         f'боевого потенциала, Осталось {self.__ammo} боеголовок, Уровень топлива:{self.__fuel} Координаты Х({self.__x}), У({self.__y})! ')
        return (f'Модель <<{self.__model}>> , Прочность: {self.__hp}, Накопилось {self.__xp} '
                f'боевого потенциала, Осталось {self.__ammo} боеголовок, Уровень топлива:{self.__fuel} Координаты Х({self.__x}), У({self.__y})! ')



