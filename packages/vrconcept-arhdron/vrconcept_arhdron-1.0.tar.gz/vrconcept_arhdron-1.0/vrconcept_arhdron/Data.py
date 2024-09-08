import math

class Data:

    # Индексы
    move_value_x_index = 9
    move_value_y_index = 6
    move_value_z_index = 7
    rotate_value_index = 8
    sound_play_index = 5
    red_blades_rotate_index = 4
    yellow_blades_rotate_index = 20
    rotate_front_index = 2
    rotate_side_index = 3
    battery_division_indexes = [1, 11, 12, 13, 14, 15, 16]

    # Перемещение
    move_value_x = 0.0
    move_value_y = 0.0
    move_value_z = 0.0

    # Повороты
    rotate_value = 0.0
    rotate_side = 0.0
    rotate_front = 0.0
    stabilize_side_angle = 0.1
    stabilize_front_angle = 0.1

    # Лопасти
    blades_rotate_value = 0.0
    blades_rotate_speed = 35

    # Заряд батареи
    battery = 1.0
    battery_consumption = 0.000001

    # Включена ли музыка
    is_sound_play = False

    # Имитация ветра
    wind_vector = [2, 1, 0]
    wind_power = 5

    # Масштабы
    move_scale = 10
    rotate_scale = 0.0001

    # Инерция
    inertia_x = 0
    inertia_y = 0
    inertia_move_x = 0.01
    inertia_move_y = 0.01

    def __init__(self, x, y, z, rotate, rotate_front, rotate_side, red_blades, yellow_blades, blades_speed, sound, battery, move_scale, rotate_scale, battery_consumption, wind_power, wind_vector_x, wind_vecrot_y, wind_vecrot_z, stabilize_side, stabilize_front, inertia_x, inertia_y):
        # Перемещение
        self.move_value_x = 0.0
        self.move_value_y = 0.0
        self.move_value_z = 0.0
        # Повороты
        self.rotate_value = 0.0
        self.rotate_side = 0.0
        self.rotate_front = 0.0
        self.stabilize_side_angle = stabilize_side
        self.stabilize_front_angle = stabilize_front
        # Лопасти
        self.blades_rotate_value = 0.0
        self.blades_rotate_speed = blades_speed
        # Батарея
        self.battery = 1.0
        self.battery_consumption = battery_consumption
        # Включена ли музыка
        self.is_sound_play = False
        # Имитация ветра
        self.wind_vector = [wind_vector_x, wind_vecrot_y, wind_vecrot_z]
        self.wind_power = wind_power
        # Индексы
        self.move_value_x_index = x
        self.move_value_y_index = y
        self.move_value_z_index = z
        self.rotate_value_index = rotate
        self.sound_play_index = sound
        self.red_blades_rotate_index = red_blades
        self.yellow_blades_rotate_index = yellow_blades
        self.rotate_front_index = rotate_front
        self.rotate_side_index = rotate_side
        self.battery_division_indexes = battery
        self.move_scale = move_scale
        self.rotate_scale = rotate_scale
        # Инерция
        self.inertia_move_x = inertia_x
        self.inertia_move_y = inertia_y

    def move_vertical(self, send_array, stick_value):
        self.inertia_x = stick_value
        self.battery -= self.battery_consumption
        self.move_value_y -= self.move_scale * math.sin(self.rotate_value * math.pi / 180) * self.battery * stick_value
        self.move_value_x -= self.move_scale * math.cos(-self.rotate_value * math.pi / 180) * self.battery * stick_value
        send_array[self.move_value_x_index] = self.move_value_x
        send_array[self.move_value_y_index] = self.move_value_y
        send_array = self.rotate_blades(send_array, stick_value, stick_value)
        return send_array


    def rotate_right(self, send_array, stick_value):
        self.battery -= self.battery_consumption
        self.rotate_value -= self.rotate_scale * stick_value
        send_array[self.rotate_value_index] = self.rotate_value
        send_array = self.rotate_blades(send_array, stick_value, -stick_value)
        return send_array

    def rotate_left(self, send_array, stick_value):
        self.battery -= self.battery_consumption
        self.rotate_value -= self.rotate_scale * stick_value
        send_array[self.rotate_value_index] = self.rotate_value
        send_array = self.rotate_blades(send_array, -stick_value, stick_value)
        return send_array



    def turn_on_sound(self, send_array):
        if not self.is_sound_play:
            send_array[self.sound_play_index] = 1
            self.is_sound_play = True
        return send_array


    def turn_off_sound(self, send_array):
        if self.is_sound_play:
            send_array[self.sound_play_index] = 0
        return send_array


    def rotate_blades(self, send_array, koef_l, koef_r):
        self.blades_rotate_value += self.blades_rotate_speed
        send_array[self.red_blades_rotate_index] = self.blades_rotate_value * koef_l
        send_array[self.yellow_blades_rotate_index] = self.blades_rotate_value * koef_r
        return send_array

    def charge(self, send_array):
        if self.battery > 0:
            self.battery -= self.battery_consumption
        part_number = len(self.battery_division_indexes) - 1
        for division_index in self.battery_division_indexes:
            intermediate_value = part_number / len(self.battery_division_indexes)
            if self.battery > intermediate_value:
                send_array[division_index] = 1
            else:
                send_array[division_index] = 0
            part_number -= 1
        return send_array

    def run(self, send_array, left_stick_vertical, left_stick_horizontal, right_stick_vertical, right_stick_horizontal, battery_limit):
        # если заряд батареи больше порогового значения, то выполняются все действия
        if self.battery > battery_limit:
            # Поворот по часовой
            if left_stick_horizontal > 0.1:
                send_array = self.rotate_right(send_array=send_array, stick_value=left_stick_horizontal)
            # Поворот против часовой
            if left_stick_horizontal < -0.1:
                send_array = self.rotate_left(send_array=send_array, stick_value=left_stick_horizontal)
            # Перемещение вперед и назад
            if right_stick_vertical < -0.1 or right_stick_vertical > 0.1:
                send_array = self.move_vertical(send_array=send_array, stick_value=right_stick_vertical)
        # Заряд батареи
        send_array = self.charge(send_array=send_array)
        return send_array
