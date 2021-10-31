from requests import request
from bs4 import BeautifulSoup as bs
import re
import pickle


class Analyzer:
    def __init__(self, text):
        self.text = text
        self.structure = {
            "Всего слов": 0,
            "Всего предложений": 0,
            "Предложения": [],  # список кортежей (<предложение>, <кол-во слов>)
            "Слова": {},  # словарь <слово>: <кол-во букв>
            "Знаки препинания": {}  # словарь <знак препинания>: <кол-во таких знаков в тексте>
        }
        self.punctuationMarks = [".", "...", ",", "!", "?", "-", ":", ";", "(", ")", "'", "\""]
        self.fileName = "structure.pickle"

    def analyzePunctuationMarks(self):
        """Выполняет анализ текста (поиск знаков препинания и их кол-во)"""
        for word in self.text.split(" "):
            symbol = re.sub(r'\w+', "", word)
            if symbol in self.punctuationMarks:
                if symbol not in self.structure["Знаки препинания"]:
                    self.structure["Знаки препинания"][symbol] = 1
                else:
                    self.structure["Знаки препинания"][symbol] += 1

    def analyzeSentenses(self):
        """Выполняет анализ предложений в тексте (поиск, кол-во предложений)"""
        endOfSentensesMarks = [".", "!", "?", "..."]
        sentenses = []
        for key in self.structure["Знаки препинания"]:
            if key in endOfSentensesMarks:
                # можно было бы написать понятнее, но нужно показать, что знаю функцию map() :)
                for sentense in map(lambda sentense: (
                        sentense.strip() + key, len(re.sub(r"[^A-zА-я, +] ", "", sentense.strip()).split(" "))) if (
                        len(re.sub(r"[^A-zА-я+]", "", sentense).strip()) > 0) else (), self.text.split(key)):
                    if len(sentense) > 0:
                        sentenses.append(sentense)
        self.structure["Предложения"] = sentenses
        self.structure["Всего предложений"] = len(sentenses)

    @staticmethod
    def isWordAlreadyFound(words, searchWord):
        """Определяет находится ли слово в списке слов"""
        for word in words:
            if word.upper() == searchWord.upper():
                return True
        return False

    def analyzeWords(self):
        """Выполняет анализ слов в тексте (поиск, кол-во букв)"""
        words = {}
        allWordsCount = 0
        for item in self.structure["Предложения"]:
            sentense = item[0]
            for word in sentense.split(" "):
                word = re.sub(r"[^A-zА-я]", "", word.strip())
                if len(word) > 0:
                    allWordsCount += 1
                    if not self.isWordAlreadyFound(words, word):
                        words[word] = len(word)
        self.structure["Слова"] = words
        self.structure["Всего слов"] = allWordsCount

    def analyzeText(self):
        """Выполняет анализ текста (кол-во слов, кол-во предложений и т.д. по заданию)"""
        # первым анализируем знаки препинания, чтобы потом использовать эту информацию
        self.analyzePunctuationMarks()
        self.analyzeSentenses()
        self.analyzeWords()

    def writeDataInBinaryFile(self):
        """Выполняет запись данных в бинарный файл"""
        with open(self.fileName, "wb") as file:
            pickle.dump(self.structure, file)

    def readDataFromBinaryFile(self):
        """Выполняет чтение данных из бинарного файла"""
        with open(self.fileName, "rb") as file:
            return pickle.load(file)


def isUpperLetter(letter):
    """Выполняет проверку является ли буква заглавной"""
    if letter is None:
        return False
    upperLetter = letter.upper()
    return upperLetter == letter


def normalizeText(text):
    """Нормализует текст (метод нужен для того, чтобы убрать случаи,
        когда заглавная буква идёт не в начале предложения) """
    result = ""
    lastSymbol = ""
    punctuationMarks = ".!?"
    for word in text.split(" "):
        firstLetter = word[0]
        if punctuationMarks.find(lastSymbol) < 0 and isUpperLetter(firstLetter):
            word = firstLetter.lower() + word[1:]
        result += word + " "
        lastSymbol = result.rstrip()[-1]
    return result


def getTextByUrl(urlAdress, tagName, className):
    """Возвращает текст в определённом теге на веб-странице по URL-адресу, названию тега и класса"""
    markup = request("GET", urlAdress).text
    hierarchy = bs(markup, features="html.parser").find_all(tagName, attrs={"class": className})
    if hierarchy is None or len(hierarchy) < 1:
        return ""
    contents = hierarchy[0].contents
    content = list(filter(lambda string: str(string).find("<") < 0, contents))
    text = " ".join(content)
    return normalizeText(text)


def printData(data):
    """Выполняет вывод данных в удобоваримом виде"""
    print("Итоговая структура:\n")
    message = ""
    for key in data:
        value = data[key]
        if isinstance(value, (int, float)):
            message += f"{key}: {value}"
        elif isinstance(value, list):
            message += "[\n  "
            message += "\n  ".join(map(lambda val: f"{val},", value))
            message = message[:-1] + "\n"
            message += "]"
        elif isinstance(value, dict):
            message += "{\n  "
            message += "\n  ".join(map(lambda k: f"\'{k}\': {value[k]},", value))
            message = message[:-1] + "\n"
            message += "}"
        message += ",\n"
    if len(message) > 0:
        message = message[:-2]
    print(message)


def tryGetValue(textForShow):
    """Возвращает целое число, введённое пользователем с клавиатуры"""
    result = ""
    while isinstance(result, (str)):
        try:
            result = int(input(textForShow))
        except:
            print("\n")
            result = ""
    return result


def splitTextIntoParagraphs(listSentenses, count):
    """Выполняет разделение текста на предложения"""
    sentenses = list(map(lambda s: s[0], listSentenses))
    result = []
    paragraph = ""
    i = 0
    for sentense in sentenses:
        if i < count:
            i += 1
        else:
            result.append(paragraph)
            paragraph = ""
            i = 0
        paragraph += sentense + " "
    """exit()"""


url = "http://students.perm.hse.ru/anthem/"
tagName = "p"
className = "first_child last_child"
text = getTextByUrl(url, tagName, className)
analyzer = Analyzer(text)
analyzer.analyzeText()
analyzer.writeDataInBinaryFile()
data = analyzer.readDataFromBinaryFile()
printData(data)
countSentensesInParagraph = tryGetValue("Введите число предложений в абзаце: ")
splitTextIntoParagraphs(data["Предложения"], countSentensesInParagraph)