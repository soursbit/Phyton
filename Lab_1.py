# Вариант №10
"""Задание 1.
Написать функцию, которая определяет принадлежность точки с координатами (x; y)
заштрихованной фигуре (обратить внимание на закрашенность границ: если граница не закрашена,
она не принадлежит фигуре) и возвращает логическое значение.
В зависимости от ответа выводить “YES” / “NO”."""

# Решение:
ErrorY = False
ErrorX = False
print('Программа определяет пренадлежность точки (х;y) на коордиатах, для этого: ')

ay = input('Введите координату y: ')
ax = input('Введите координату Х: ')
while not ErrorY:
    try:
        y = float(ay)
        ErrorY = True
        break
    except ValueError:
        print('Некорректный ввод Y!')
        ay = input('Введите координату Y (Введенное значение должно быть числом!): ')

while not ErrorX:
    try:
        x = float(ax)
        ErrorX = True
        break
    except ValueError:
        print('Некорректный ввод X!')
        ax = input('Введите координату X (Введенное значение должно быть числом!): ')

# Вершины ромба №1
x1 = -7
y1 = 5
x2 = -5
y2 = 7
x3 = -3
y3 = 5
x4 = -5
y4 = 3

# Центр круга и радиус
x0 = 8
y0 = -5
r = 2

# Условие для ромба
if y >= 5:
    T1 = ((x1 - x) * (y2 - y1)) - ((x2 - x1) * (y1 - y))
    T2 = ((x2 - x) * (y3 - y2)) - ((x3 - x2) * (y2 - y))
    T3 = ((x3 - x) * (y1 - y3)) - ((x1 - x3) * (y3 - y))
    if (T1 > 0 and T2 > 0 and T3 >= 0) or (T1 < 0 and T2 < 0 and T3 <= 0):
        print('YES')
    else:
        print('NO')
elif (y < 5) and (y > -3):
    T1 = ((x1 - x) * (y4 - y1)) - ((x4 - x1) * (y1 - y))
    T2 = ((x4 - x) * (y3 - y4)) - ((x3 - x4) * (y4 - y))
    T3 = ((x3 - x) * (y1 - y3)) - ((x1 - x3) * (y3 - y))
    if (T1 > 0 and T2 > 0 and T3 > 0) or (T1 < 0 and T2 < 0 and T3 < 0):
        print('YES')
    else:
        print('NO')
elif (y <= -3) and (y >= -5):
    # Вершины ромба №2
    x1 = 6
    y1 = -5
    x2 = 8
    y2 = -3
    x3 = 10
    y3 = -5

    T1 = ((x1 - x) * (y2 - y1)) - ((x2 - x1) * (y1 - y))
    T2 = ((x2 - x) * (y3 - y2)) - ((x3 - x2) * (y2 - y))
    T3 = ((x3 - x) * (y1 - y3)) - ((x1 - x3) * (y3 - y))
    if ((T1 >= 0 and T2 >= 0 and T3 >= 0) or (T1 <= 0 and T2 <= 0 and T3 <= 0)) or (
            (T1 < 0 and T2 >= 0 and T3 >= 0) or (T1 > 0 and T2 <= 0 and T3 <= 0)):
        if (((x - x0) ** 2) + ((y - y0) ** 2)) <= r ** 2:
            print('YES')
        else:
            print('NO')
    else:
        print('NO')

elif y < -5:
    x1 = 6
    y1 = -5
    x3 = 10
    y3 = -5
    x4 = 8
    y4 = -7

    T1 = ((x1 - x) * (y4 - y1)) - ((x4 - x1) * (y1 - y))
    T2 = ((x4 - x) * (y3 - y4)) - ((x3 - x4) * (y4 - y))
    T3 = ((x3 - x) * (y1 - y3)) - ((x1 - x3) * (y3 - y))

    if ((T1 >= 0 and T2 >= 0 and T3 >= 0) or (T1 <= 0 and T2 <= 0 and T3 <= 0)) or (
            (T1 >= 0 and T2 < 0 and T3 >= 0) or (T1 <= 0 and T2 > 0 and T3 <= 0)):
        if (((x - x0) ** 2) + ((y - y0) ** 2)) <= r ** 2:
            print('YES')
        else:
            print('NO')
    else:
        print('NO')
else:
    print('NO')
