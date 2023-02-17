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


def wrong_user_input(coordinate):
    """
    Возвращает True если введенные координаты за пределами игрового поля
    False если координаты соответствуют игровому полю.
    """
    if len(coordinate) == 3 and not coordinate[-1].isdigit():
        return True
    if 1 < len(coordinate) < 4 and coordinate[1].isdigit() \
            and int(coordinate[1:]) in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) and coordinate[0] in "абвгдежзик":
        return False
    return True


def user_input_conv(coordinate):
    """
    Принимает координаты в строковом формате,
    возвращает в числовом.
    """
    lst_y = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "к"]
    return int(coordinate[1:]), lst_y.index(coordinate[0]) + 1


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
    if field[y][x + 1] in (dead, part_ship) or field[y][x - 1] in (dead, part_ship):
        shift_x = 1
        shift_y = 0
    elif field[y + 1][x] in (dead, part_ship) or field[y - 1][x] in (dead, part_ship):
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
    if field[x][y+1] == dead or field[x][y-1] == dead:
        shift_x = 0
        shift_y = 1
    else:
        shift_x = 1
        shift_y = 0
    # Находим начало корабля
    while True:
        x -= shift_x
        y -= shift_y
        if field[x][y] != dead:
            x += shift_x
            y += shift_y
            break
    # Заполняем квадратики вокруг корабля
    while True:
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if field[i][j] != dead:
                    field[i][j] = miss
        x += shift_x
        y += shift_y
        if field[x][y] != dead:
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
    list_wounded = [0-мимо, 1-ранил], [хранит индекс направления смещения],
    [-1, 0], [1, 0], [0, -1], [0, 1] - смещения выстрела, [x, y] - координаты первого ранения, [подсчет попаданий]
    """
    if list_wounded[0] == [1]:
        x += list_wounded[list_wounded[1][0]][0]
        y += list_wounded[list_wounded[1][0]][1]
        return x, y
    # Если не попал при добивании, меняется индекс направление смещения
    list_wounded[1][0] += 1
    # Проверка индекса направления смещения
    if list_wounded[1][0] > 5 or list_wounded[1][0] < 2:
        list_wounded[1][0] = 2
    x = list_wounded[6][0] + list_wounded[list_wounded[1][0]][0]
    y = list_wounded[6][1] + list_wounded[list_wounded[1][0]][1]
    return x, y


#  Создание пустых игровых полей
part_ship = "●"
emp = "□"
dead = "X"
miss = "◦"
user_field = [[emp for _ in range(12)] for _ in range(12)]
open_bot_field = [[emp for _ in range(12)] for _ in range(12)]
hidden_bot_field = [[emp for _ in range(12)] for _ in range(12)]
#  Списки для подсчета очков и расстановки кораблей
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
        while True:
            #  Вводим координаты начала корабля
            user_input = input("Введите координаты начала корабля без пробела, например - б2: ").lower()
            if wrong_user_input(user_input):
                print("Координаты не соответствуют игровому полю! ")
                continue
            x_start, y_start = user_input_conv(user_input)
            # Проверяем свободно ли место на поле для корабля
            if not(check_coordinates(user_field, x_start, y_start, x_start, y_start)):
                show_field(user_field, open_bot_field)
                print("Место уже занято, либо рядом уже есть корабль")
                continue
            if ship == 1:
                fill_field(user_field, x_start, y_start, x_start, y_start)
                show_field(user_field, open_bot_field)
                break
            #  Вводим координаты конца корабля
            user_input = input("\nКонец корабля должен быть ниже или правее начала корабля! \n"
                               "Введите координаты конца корабля без пробела, например - д2: ").lower()
            x_end, y_end = user_input_conv(user_input)
            #  Проверяем размер корабля
            if not (x_end == x_start or y_end == y_start):
                print("Корабль должен занимать одну линию!")
                continue
            if not (x_end - x_start + 1 == ship or y_end - y_start + 1 == ship):
                print("Вы должны указать корабль с количеством секций: ", ship)
                continue
            if wrong_user_input(user_input):
                print("Координаты не соответствуют игровому полю! ")
                continue
            if not(check_coordinates(user_field, x_start, y_start, x_end, y_end)):
                show_field(user_field, open_bot_field)
                print("Место уже занято, либо рядом уже есть корабль")
                continue
            fill_field(user_field, x_start, y_start, x_end, y_end)
            break

#  Расстановка кораблей у бота
auto_fill_field(hidden_bot_field)
print("Скрытое поле бота")
show_field(hidden_bot_field, hidden_bot_field)


#  БОЙ БОЙ БОЙ БОЙ

finish_him = False  # True если есть раненый корабль

#  Список для добивания корабля:
# [0-мимо, 1-попал], [хранит индекс смещения], [][][][] - смещения выстрела, [x][y] - координаты первого ранения
list_wounded = [[0], [2], [-1, 0], [1, 0], [0, -1], [0, 1], [0, 0], [0]]

print("\n" + " " * 10 + "Корабли расставлены, первым ходит игрок.")

while bot_ships and user_ships:

    # АТАКА ИГРОКА

    show_field(user_field, open_bot_field)
    while bot_ships:
        user_attack = input("Введите координаты для выстрела без пробела, например - б2: ")
        #  Проверяем введенные координаты
        if wrong_user_input(user_attack):
            print("Введенных координат на игровом поле нет!")
            continue
        x_attack, y_attack = user_input_conv(user_attack)
        #  Проверяем выстрел на предмет попадания
        if open_bot_field[x_attack][y_attack] in (miss, dead):
            print("Вы уже стреляли по данным координатам")
            continue
        if hidden_bot_field[x_attack][y_attack] == part_ship:
            open_bot_field[x_attack][y_attack] = dead
            hidden_bot_field[x_attack][y_attack] = dead
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
            open_bot_field[x_attack][y_attack] = miss
            time.sleep(2)
            show_field(user_field, open_bot_field)
            break

    # АТАКА БОТА

    if bot_ships:
        print(" " * 22 + "Бот Атакует!!!")
    else:
        break
    while user_ships:
        if finish_him:
            # Если есть раненый, пытается добить
            x_attack_bot, y_attack_bot = attack_wounded(x_attack_bot, y_attack_bot)
        else:
            # Генерирует новые координаты выстрела
            x_attack_bot = random.randint(1, 10)
            y_attack_bot = random.randint(1, 10)
        #  Проверяет, был ли выстрел ранее по новым координатам
        if user_field[x_attack_bot][y_attack_bot] in (miss, dead):
            list_wounded[0][0] = 0
            continue
        # Проверяем попал ли бот по кораблю
        if user_field[x_attack_bot][y_attack_bot] == part_ship:
            user_field[x_attack_bot][y_attack_bot] = dead
            # Проверяем убит ли корабль
            if check_after_attack(user_field, x_attack_bot, y_attack_bot):
                print(" " * 22 + "Корабль уничтожен!")
                finish_him = False
                list_wounded[1][0] = 2  # Возвращаем индекс направления в исходное состояние
                fill_around_ship(user_field, x_attack_bot, y_attack_bot)
                user_ships.pop()
            else:
                print(" " * 22 + "Корабль ранен!")
                if not finish_him:
                    list_wounded[6][0] = x_attack_bot
                    list_wounded[6][1] = y_attack_bot
                finish_him = True
                list_wounded[0][0] = 1  # Указываем что было попадание
            continue
        else:
            print(" " * 22 + "Бот промахнулся!")
            user_field[x_attack_bot][y_attack_bot] = miss
            list_wounded[0][0] = 0  # Указываем что бот промахнулся
            break
print()
if user_field:
    print(" " * 15 + "Вы победили бота! Поздравляем!")
else:
    print(" " * 15 + "Вы проиграли! БОТ выиграл эту игру!")
