from bs4 import BeautifulSoup
import json
import pandas as pd

def bool_map(val):
  tmp = {'-': False, '+': True, 'no': False, 'yes': True}
  return tmp[val]

type_dic = {'id': int, 'reviews': int, 'price': float, 'rating': float,
            'new': bool_map, 'exclusive': bool_map, 'sporty': bool_map}

def xml_reader(filename, list_xml):

  with open('127.xml', 'r', encoding='utf-8') as file:
          content = file.read()

  clothes = BeautifulSoup(content, 'xml').find_all('clothing')

  for item in clothes:

    data = {el.name: type_dic[el.name](el.get_text().strip()) if el.name in type_dic.keys()
              else el.get_text().strip()
              for el in item if el.name is not None}

    list_xml.append(data)

  return list_xml

list_xml = []
for i in range(1, 155):
  xml_reader(f'{i}.xml', list_xml)

with open('fourth_task_output.json', 'w', encoding='utf-8') as file:
    json.dump(list_xml, file, ensure_ascii=False)

df = pd.DataFrame(list_xml)
df.head()

df_sorted = df.sort_values('price')

df_filtered = df[df['new'] == True]

stats = {}
stats['min'] = df['rating'].min()
stats['max'] = df['rating'].max()
stats['avg'] = round(df['rating'].mean(), 2)
stats['med'] = df['rating'].median()

print(f'''statistics for 'distance' column:\nminimum rating is {stats['min']}\nmaximum rating is {stats['max']}
average rating is {stats['avg']}\nmedian rating is {stats['med']}''')

print({siz : len(df[df['size']==siz]) for siz in df['size'].unique()})