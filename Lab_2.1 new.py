import pickle
from functools import reduce


def input_positive_int(msg):
    while True:
        try:
            n = int(input(msg))
            if n > 0:
                return n
            else:
                raise ValueError()
        except ValueError as ex:
            print("Введённое число должно быть натуральным")


def count_dict(collection):
    res = {}
    for item in collection:
        res[item] = res.get(item, 0) + 1
    return res


def sentence_tuple(sentence):
    words = sentence.strip()
    return words, len(words.replace('-', '').split())


def make_summary():
    eos = '.?!'
    punctuation = '\0 ,;:-"\''
    eos_n_punctuation = (punctuation + eos)[2:]
    filename = "Lab_2.1.txt"

    print(f"Открываю файл {filename}")
    # если файл бинарный, а не текстовой, то он и не откроется
    with open(filename, "r") as lorem_file:
        lorem = lorem_file.read().replace('\n', '').replace('\r', '')

    if len(lorem.strip()) == 0:
        raise IOError(f"Файл {filename} пуст")

    tmp = reduce(lambda x, y: x.replace(y, y + '\0'), eos, lorem)
    tmp2 = reduce(lambda x, y: x.replace(y, ' '), eos_n_punctuation, lorem).lower()

    print("Анализирую файл")
    sentences = list(map(sentence_tuple, tmp.strip(punctuation).split('\0')))

    return {
        "Всего слов": sum(map(lambda t: t[1], sentences)),
        "Всего предложений": len(sentences),
        "Предложения": sentences,
        "Слова": count_dict(tmp2.split()),
        "Знаки препинания": count_dict(tuple(filter(lambda ch: ch in eos_n_punctuation, lorem)))
    }


def save_and_load(obj):
    with open("lorem_summary.dat", "wb") as lorem_summary:
        pickle.dump(obj, lorem_summary)
    with open("lorem_summary.dat", "rb") as lorem_summary:
        res = pickle.load(lorem_summary)
    return res


def print_summary(summary):
    print("Результат анализа текста: ")
    for key, val in summary.items():
        print(f'{key}: ', end='')
        if isinstance(val, tuple) or isinstance(val, list):
            print()
            for item in val:
                print(f'\t{item}')
        elif isinstance(val, dict):
            print()
            for key2, val2 in val.items():
                print(f'\t{key2}: {val2}')
        else:
            print(val)


def paragraphs_split(summary):
    n = input_positive_int("Введите кол-во абзацев: ")
    s = 0
    paragraph, paragraphs = [], []
    for sentence in summary['Предложения']:
        paragraph.append(sentence)
        s = (s + 1) % n
        if s == 0:
            paragraphs.append(tuple(paragraph))
            paragraph = []
    if s > 0:
        paragraphs.append(tuple(paragraph))
    return paragraphs


def len_of_paragraph(paragraph):
    return sum(map(lambda r: r[1], paragraph))


try:
    summary = make_summary()
    summary_new = save_and_load(summary)
    print_summary(summary_new)
    paragraphs = paragraphs_split(summary_new)
    paragraphs.sort(key=len_of_paragraph)

    with open('Lab_2.1(Результат).txt', 'w') as sorted_file:
        for paragraph in paragraphs:
            sorted_file.write(' '.join(map(lambda r: r[0], paragraph)) + '\n')
except UnicodeDecodeError as e:
    print(e.reason)
except IOError as e:
    print(e.reason)
