import random
import time


def show_field(user, bot):
    print("      ПОЛЕ ИГРОКА:" + " " * 7 + "|Счет|" + " " * 5 + "     ПОЛЕ БОТА:")
    print("  |а|б|в|г|д|е|ж|з|и|к" + " " * 3, (10 - len(bot_ships)), ":",
          (10 - len(user_ships)), " " * 2 + "  |а|б|в|г|д|е|ж|з|и|к")
    for i in range(1, 11):
        print(i, end="  ") if i not in [10, 11] else print(i, end=" ")
        for j in range(1, 11):
            print(user[i][j], end=" ")
        print(" " * 11, end="")
        print(i, end="  ") if i not in [10, 11] else print(i, end=" ")
        for j in range(1, 11):
            print(bot[i][j], end=" ")
        print()


def user_input_conv(coordinate):
    """
    Принимает координаты в строковом формате,
    возвращает в числовом.
    """
    lst_y = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "к"]
    return int(coordinate[:-1]), lst_y.index(coordinate[-1]) + 1


def check_coordinates(field, x_1, y_1, x_2, y_2):
    """
    Проверяет место установки корабля с переданными координатами.
    True - можно, свободно
    False - нельзя, есть занятые клетки
    """
    for i in range(x_1 - 1, x_2 + 2):
        for j in range(y_1 - 1, y_2 + 2):
            if field[i][j] != emp:
                return False
    return True


def fill_field(field, x_1, y_1, x_2, y_2):
    """
    Устанавливает на поле корабль с заданными координатами.
    """
    for i in range(x_1, x_2+1):
        for j in range(y_1, y_2+1):
            field[i][j] = part_ship


def check_after_attack(field, y, x):
    """
    Возвращает True если корабль уничтожен
    и False если ранен
    """
    # Выясняем расположение корабля (горизонтальное или вертикальное)
    if field[y][x + 1] in ("x", part_ship) or field[y][x - 1] in ("x", part_ship):
        shift_x = 1
        shift_y = 0
    elif field[y + 1][x] in ("x", part_ship) or field[y - 1][x] in ("x", part_ship):
        shift_x = 0
        shift_y = 1
    else:
        return True
    # Находим начало корабля
    while True:
        x -= shift_x
        y -= shift_y
        if field[y][x] == emp:
            x += shift_x
            y += shift_y
            break
    # Проверяем корабль
    while True:
        if field[y][x] == part_ship:
            return False
        if field[y][x] == emp:
            return True
        x += shift_x
        y += shift_y


def fill_around_ship(field, x, y):
    """
    Заполняет пространство точками вокруг убитого корабля.
    """
    # Выясняем расположение(горизонтальное или вертикальное)
    if field[x][y+1] == "x" or field[x][y-1] == "x":
        shift_x = 0
        shift_y = 1
    else:
        shift_x = 1
        shift_y = 0
    # Находим начало корабля
    while True:
        x -= shift_x
        y -= shift_y
        if field[x][y] != "x":
            x += shift_x
            y += shift_y
            break
    # Заполняем квадратики вокруг корабля
    while True:
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if field[i][j] != "x":
                    field[i][j] = "◦"
        x += shift_x
        y += shift_y
        if field[x][y] != "x":
            break


def auto_fill_field(field):
    """
    Автоматическая расстановка кораблей.
    """
    for size_ship in bot_ships:
        while True:
            # Находим случайные координаты начала корабля
            x_1 = random.randint(1, 10)
            y_1 = random.randint(1, 10)
            # Выбор направления расположения корабля
            down_ship = random.choice([True, False])
            if down_ship:
                x_2 = x_1
                y_2 = y_1 + size_ship - 1
            else:
                x_2 = x_1 + size_ship - 1
                y_2 = y_1
            # Проверка находится ли конец корабля на игровом поле
            if x_1 + size_ship > 10 or y_1 + size_ship > 10:
                continue
            # Проверяем свободно ли место на поле для корабля
            if check_coordinates(field, x_1, y_1, x_2, y_2):
                break
        # Размещаем корабль на поле
        fill_field(field, x_1, y_1, x_2, y_2)
    return field


def attack_wounded(x, y):
    """
    Не работает полноценно, может зациклиться((((
    """
    if list_attack_wounded[0][0] != 0:
        if list_attack_wounded[1][0] == 5:
            list_attack_wounded[1][0] = 2
    else:
        list_attack_wounded[1][0] = list_attack_wounded[1][0] + 1
    while True:
        print("Смена координат для добивания")
        x = x + list_attack_wounded[list_attack_wounded[1][0]][0]
        y = y + list_attack_wounded[list_attack_wounded[1][0]][1]
        print(x, y)
        time.sleep(3)
        if 0 < x < 10 and 0 < y < 10:
            break
        elif list_attack_wounded[1][0] == 5:
            list_attack_wounded[1][0] = 2
        else:
            list_attack_wounded[1][0] = list_attack_wounded[1][0] + 1
    return x, y


#  Создание пустых игровых полей
part_ship = "●"
emp = "□"
user_field = [[emp for _ in range(12)] for _ in range(12)]
open_bot_field = [[emp for _ in range(12)] for _ in range(12)]
hidden_bot_field = [[emp for _ in range(12)] for _ in range(12)]

user_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
bot_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


print("Добро пожаловать в игру: Морской бой")

#  Расстановка кораблей у игрока
if input("Желаете автоматически создать свое поле?: да или нет ").lower() == "да":
    auto_fill_field(user_field)
else:
    for ship in user_ships:
        show_field(user_field, open_bot_field)
        print("Ввод координат корабля с количеством секций:", ship)
        x_start, y_start = user_input_conv(input("Введите координаты начала корабля без пробела,"
                                                 " например - 2б: "))
        if ship == 1:
            fill_field(user_field, x_start, y_start, x_start, y_start)
            show_field(user_field, open_bot_field)
            continue
        x_end, y_end = user_input_conv(input("Введите координаты конца корабля без пробела, например - 2б: "))
        fill_field(user_field, x_start, y_start, x_end, y_end)

#  Расстановка кораблей у бота
auto_fill_field(hidden_bot_field)
print("Скрытое поле бота")
show_field(hidden_bot_field, hidden_bot_field)

#  БОЙ БОЙ БОЙ БОЙ

finish_him = False  # True если есть раненый корабль

#  Список для добивания корабля:
# [0-мимо, 1-попал], [хранит индекс смещения], [][][][] - смещения выстрела, [x][y] - координаты первого ранения
list_attack_wounded = [[0], [2], [-1, 0], [1, 0], [0, -1], [0, 1], [0, 0]]

print("\n" + " " * 10 + "Корабли расставлены, первым ходит игрок.")
while bot_ships or user_ships:

    # АТАКА ИГРОКА

    show_field(user_field, open_bot_field)
    while bot_ships:
        while True:
            user_attack = input("Введите координаты для выстрела без пробела, например - 2б: ")
            if int(user_attack[0]) in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) and user_attack[1] in "абвгдежзик":
                x_attack, y_attack = user_input_conv(user_attack)
                break
            print("Введенных координат на игровом поле нет!")
        if hidden_bot_field[x_attack][y_attack] == part_ship:
            open_bot_field[x_attack][y_attack] = "x"
            hidden_bot_field[x_attack][y_attack] = "x"
            if check_after_attack(hidden_bot_field, x_attack, y_attack):
                print(" " * 22 + "Корабль уничтожен!")
                fill_around_ship(open_bot_field, x_attack, y_attack)
                bot_ships.pop()
            else:
                print(" " * 22 + "Корабль ранен!")
                time.sleep(1)

            show_field(user_field, open_bot_field)
            continue
        else:
            print(" " * 22 + "Вы промахнулись!")
            open_bot_field[x_attack][y_attack] = "◦"
            time.sleep(2)
            show_field(user_field, open_bot_field)
            break

    # АТАКА БОТА

    print(" " * 22 + "Бот Атакует!!!")
    while user_ships or bot_ships:
        if finish_him:
            x_attack, y_attack = attack_wounded(x_attack, y_attack)
        else:
            x_attack = random.randint(1, 10)
            y_attack = random.randint(1, 10)
        if user_field[x_attack][y_attack] in "◦X":
            list_attack_wounded[0][0] = 0
            continue
        if user_field[x_attack][y_attack] == part_ship:
            user_field[x_attack][y_attack] = "x"
            if check_after_attack(user_field, x_attack, y_attack):
                print(" " * 22 + "Корабль уничтожен!")
                finish_him = False
                list_attack_wounded[1][0] = 2
                fill_around_ship(user_field, x_attack, y_attack)
                user_ships.pop()
            else:
                print(" " * 22 + "Корабль ранен!")
                if not finish_him:
                    list_attack_wounded[6][0] = x_attack
                    list_attack_wounded[6][1] = y_attack
                finish_him = True
                list_attack_wounded[0][0] = 1
            continue
        else:
            print(" " * 22 + "Бот промахнулся!")
            user_field[x_attack][y_attack] = "◦"
            break
if user_field:
    print(" " * 22 + "Вы победили бота! Поздравляем!")
else:
    print(" " * 22 + "Вы проиграли! БОТ выиграл эту игру!")
