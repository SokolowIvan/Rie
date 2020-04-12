
import requests
import pandas as pd
from lxml import etree



def start():
  url = 'http://topnlab.ru/export/main/database/?data=objects&chosen=1&format=yandex&key=WlyBG73La6uYi5Wa4XY'

  #self.data_file = pd.read_csv(path_data_file) это создание из csv DataFrame

  #full_df = pd.DataFrame()

  #full_df = parseXML(getStringByUrl(url), full_df)

  #full_df.to_csv(path_or_buf=self.folder + 'out_' + str(now_str) + file_mane + '.csv', sep=',', header=True,index=False, encoding='utf-8', mode='a+')
  #full_df.to_csv('dddd') не работает

  return 0

def parseXML(xml: str, full_df):

  xmlList = xml.split('\n')[1:]         #удаляем ненужный заголовок
  xmlstr = '\n'.join(xmlList)
  xmlList2 = xmlstr.split('><')[2:]     #удаляем ненужный тег
  xmlList2.pop()
  xmlstr2 = '><'.join(xmlList2)         #редактируем строку
  xmlstr3 = xmlstr2 + '>'
  xmlList3 = xmlstr3.split('</offer><')  #
  offer_dict = {}

  for xmlList4 in xmlList3:
    s = xmlList4.split('><')[0]
    s1 = s.split('"')[1]
    offer_dict['id'] = s1

    if xmlList4 == xmlList3[-1]:
      xmlList4 = xmlList3[-1] + '</realty-feed>'
    else:
      xmlList4 = xmlList4 + '</offer></realty-feed>'
    xmlstr6 = '<realty-feed xmlns="http://webmaster.yandex.ru/schemas/feed/realty/2010-06"><' + (''.join(xmlList4))

    root = etree.fromstring(xmlstr6)

    for offer in root.getchildren():
      for elem in offer.getchildren():
        a = (elem.tag.split('}')[1:])                                        # убираем лишнее
        elem.tag = ''.join(a)                                                # делаем список строкой
        if not elem.text:
          text = "000"
        elif elem.tag == 'photo':
              if 'image' in offer_dict:                                      #проверяем наличие аргуманта в словаре
                  text = "None"                                              #собираем адреса ссылок
              else:
                  text = elem.text
        else:
          if elem.tag == 'image':
              if 'image' in offer_dict:                                      #проверяем наличие аргуманта в словаре
                  text = offer_dict.get('image') + '; ' + elem.text          #собираем адреса ссылок
              else:
                  text = elem.text
          else:
            text = elem.text

        offer_dict[elem.tag] = text     #создаем словарь
        #print(offer_dict)

    df = pd.DataFrame(offer_dict, index=[0])
    dict.clear(offer_dict)
    print(df)
      #добовляем в датафрейи
    full_df = full_df.append(df, ignore_index=True)
    print(full_df)

  return full_df


def getStringByUrl(url: str)-> str:
  return requests.get(url).text


if __name__ == "__main__":
  start()
