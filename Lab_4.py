import re
import requests


html = requests.get('http://lib.ru/PROZA').text

start = a = html.find('<h2>Авторы</h2')
end = html.find('<a name=2>', start)

while True:
    a = html.find('<li>', a)
    if a > end: break

    a = html.find('(', a)
    b = html.find(')', a)
    res1 = re.sub(r'\D', '', html[a:b])

    a = html.find('[', b)
    b = html.find(']', a)
    res2 = re.sub(r'\D', '', html[a:b])

    a = html.find('<b>', html.find('<A', b))
    b = html.find('</b>', a)
    res3 = re.sub(r'<b>', '', html[a:b])

    print(res1, res2, res3, sep='\t')
