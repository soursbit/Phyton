# Лабароторная работа №3: "Армия (отряд специального назначения)"

from copy import deepcopy


class Human:

    def __init__(self, name: str = 'Хамидулин', age: int = 23):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def __str__(self):
        return f'{self.name}, возраст: {self.age}'


class Military(Human):
    PRIVATE = 0
    CORPORAL = 1
    JUNIOR_SERGEANT = 2
    SERGEANT = 3
    SENIOR_SERGEANT = 4
    FOREMAN = 5
    ENSIGN = 6
    SENIOR_ENSIGN = 7
    LIEUTENANT = 8
    SENIOR_LIEUTENANT = 9
    CAPTAIN = 10
    MAJOR = 11
    LT_COLONEL = 12
    COLONEL = 13
    GENERAL = 14

    ranks = [
        'Рядовой', 'Ефрейтор', 'Младший сержант', 'Сержант',
        'Старший сержант', 'Старшина', 'Прапорщик', 'Старший прапорщик',
        'Лейтенант', 'Старший лейтенант',
        'Капитан', 'Майор', 'Подполковник', 'Полковник', 'Генерал'
    ]

    def __init__(self, name: str = 'Андрей', age: int = 23, rank: int = CORPORAL):
        super().__init__(name, age)
        self.rank = rank

    def __add__(self, other):
        if isinstance(other, Military):
            result = Squad(militaries=[self]) if self == other else Squad(militaries=[self, other])
        elif isinstance(other, Squad):
            result = other + deepcopy(self)
        elif isinstance(other, Human):
            raise TypeError("Добавление гражданкского лица в отряд СпН запрещен!")
        else:
            raise TypeError("В отряд разрешено добавить, лиц служащих в Армии")
        return result

    @staticmethod
    def is_same_type(other):
        if not isinstance(other, Military):
            raise TypeError('Солдата возможно сравнить только с другим солдатом')

    # сравнение солдат по военному званию
    def __gt__(self, other):
        self.is_same_type(other)
        return self.rank > other.rank

    def __ge__(self, other):
        self.is_same_type(other)
        return self.rank >= other.rank

    def __lt__(self, other):
        self.is_same_type(other)
        return self.rank < other.rank

    def __le__(self, other):
        self.is_same_type(other)
        return self.rank <= other.rank

    def __eq__(self, other):
        res = False
        if isinstance(other, Military):
            res = all((self.name == other.name, self.age == other.age, self.rank == other.rank))
        return res

    def __str__(self):
        return f'{self.ranks[self.rank]} {self.name}, возраст: {self.age}'


class Squad:
    def __init__(self, name: str = 'Серые волки', militaries: list = None):
        self.name = name
        self.militaries = [] if militaries is None else deepcopy(militaries)

    def set_name(self, name: str):
        self.name = name

    def __add__(self, other):
        if isinstance(other, Military):
            if other in self.militaries:
                result = deepcopy(self)
            else:
                result = Squad(name=self.name, militaries=self.militaries + [other])
        elif isinstance(other, Squad):
            add_me = []
            result = deepcopy(self)
            for military in other.militaries:
                if not (military in result.militaries):
                    add_me.append(military)
            result.militaries += add_me
        elif isinstance(other, Human):
            raise TypeError("Добавление гражданкского лица в отряд СпН запрещен!")
        else:
            raise TypeError("В отряд разрешено добавить, лиц служащих в Армии")
        return result

    def __eq__(self, other):
        return all(map(lambda x, y: x == y, self.militaries, other.militaries))

    def __str__(self):
        return f"Отряд {self.name}, кол-во военнослужащих: {len(self.militaries)}\n\t" + \
               '\n\t'.join(map(lambda a: str(a), self.militaries))


soldier_1 = Military(name='Алексеев', age=17, rank=Military.PRIVATE)
soldier_2 = Military(name='Карпатов', age=32, rank=Military.FOREMAN)
soldier_3 = Military(name='Арситов', age=35, rank=Military.COLONEL)
soldier_4 = Military(name='Попов', age=22, rank=Military.SENIOR_LIEUTENANT)
soldier_5 = Military(name='Соколов', age=17)

print(soldier_1)
print(soldier_2)
print(soldier_3)
print(soldier_4)
print(soldier_5)

if soldier_1 < soldier_2:
    print(f'{soldier_2.get_name()} выше по званию, чем {soldier_1.get_name()}')
elif soldier_1 > soldier_2:
    print(f'{soldier_1.get_name()} выше по званию, чем {soldier_2.get_name()}')
else:
    print(f'{soldier_1.get_name()} и {soldier_2.get_name()} равны по званию')
print()

volf = soldier_1 + soldier_2
lynx = Squad(name='Храбрые рыси', militaries=[soldier_1, soldier_2])

print(volf)
print(lynx)

if volf == lynx:
    print('Серые волки и Храбрые рыси - один и тот же отряд.')
else:
    print('Отряд Серые волки и Храбрые рыси - разные отряды.')

print('Попробуем добавить в Альфу солдата, который уже состоит в ней!')
volf += soldier_1
print(volf)
print()

print('Присоединим к Серым волкам ещё одного солдата!')
volf += soldier_3
print(volf)
print()

print('Проделаем то же самое с Храбрыми рысями')
lynx += soldier_4
print(lynx)
print()

try:
    print('Попробуем присоеденить гражданского')
    volf += soldier_5
except TypeError as e:
    print(e)
finally:
    print(volf)
    print()

print('Создадим новый отряд из двух существующих...')
viper = volf + lynx
viper.set_name('Гадюки')
print(viper)
print()
