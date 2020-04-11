
import requests
import pandas as pd
from lxml import etree



def start():
  url = 'http://topnlab.ru/export/main/database/?data=objects&chosen=1&format=yandex&key=WlyBG73La6uYi5Wa4XY'

  # self.data_file = pd.read_csv(path_data_file) это создание из csv DataFrame

  full_df = pd.DataFrame()

  d = {
    'index': 0,
    'col1': 'fdgk4444hdfjk',
    'col2': 'fdgd22fgdf'
  }

  full_df = parseXML(getStringByUrl(url), full_df)

  #full_df.to_csv(path_or_buf=self.folder + 'out_' + str(now_str) + file_mane + '.csv', sep=',', header=True,
                #index=False, encoding='utf-8', mode='a+')
  return 0

def parseXML(xml: str, full_df):

  xmlList = xml.split('\n')[1:]
  xmlstr = '\n'.join(xmlList)

  root = etree.fromstring(xmlstr)


  offer_dict = {}
  offers =[]

  for offer in root.getchildren():
    for elem in offer.getchildren():
      a = (elem.tag.split('}')[1:])  # убираем лишнее
      elem.tag = ''.join(a)  # делаем список строкой
      if not elem.text:
        text = "None"
      else:
        if elem.tag == 'image':
            if 'image' in offer_dict:                                      #проверяем наличие аргуманта в словаре
                text = offer_dict.get('image') + '; ' + elem.text          #собираем адреса ссылок
            else:
                text = elem.text
        else:
          text = elem.text

        offer_dict[elem.tag] = text     #создаем словарь
        print(offer_dict)

      if offer.tag == "offer":
        offers.append(offer_dict)
        offer_dict = {}

        return offers

    #наполняем словарь
    #создаем датафрейм з словаря
    #df = pd.DataFrame(d, index=[0])
    #добовляем в датафрейи
    #full_df = full_df.append(df, ignore_index=True)

  return full_df

def getStringByUrl(url: str)-> str:
  return requests.get(url).text


if __name__ == "__main__":
  start()
