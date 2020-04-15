import os
import requests
import shutil
import pandas as pd
from lxml import etree


def start():
    with open('input.txt') as file:
        url = str(file.readline())
    if os.path.isdir('result'):
        shutil.rmtree('result')
    full_df = parseXML(getStringByUrl(url))
    os.chdir('result')
    file = os.getcwd() +'/data.csv'
    full_df.to_csv(path_or_buf=file, sep=',', header=True, index=False, encoding='utf-8', mode='w')

    pass

def parseXML(xml: str):
    os.mkdir('result')
    full_df = pd.DataFrame()
    xmlList = xml.split('\n')[1:]
    xmlstr = '\n'.join(xmlList)
    offer_dict = dict({'offer_id': 'None', 'type_housing': 'None', 'deal_status': 'None', 'property_status': 'None',
         'is_new_house': 'None',
         'type_house': 'None', 'type_house_height': 'None', 'type_new': 'None', 'country_properties': 'None',
         'rural_properties': 'None', 'commercial_property': 'None', 'name_cottage_settlement': 'None',
         'cadastral_number': 'None',
         'land_category': 'None', 'type_permitted_use': 'None', 'investment_project': 'None', 'electro_supply': 'None',
         'water_supply': 'None', 'heating_type': 'None', 'gas_supply': 'None', 'parking_type': 'None',
         'underground_parking': 'None',
         'type_of_sewer': 'None', 'chute': 'None', 'access_roads': 'None', 'ramp': 'None', 'price_for_hundred': 'None',
         'vacation_rentals': 'None', 'minimum_rental_period': 'None', 'prepayment': 'None', 'type_of_lease': 'None',
         'developer': 'None', 'deadline_year': 'None', 'deadline_quarter': 'None', 'rooms': 'None',
         'rooms_for_rent': 'None',
         'layout_room': 'None', 'total_area': 'None', 'area_room': 'None', 'living_area': 'None',
         'land_plot_area': 'None',
         'total_rooms_apartment': 'None', 'floor': '', 'total_floor_house': 'None', 'number_of_bedrooms': 'None',
         'kitchen': 'None',
         'loggia': 'None', 'balcony': 'None', 'direction_windows': 'None', 'separate_bathrooms': 'None',
         'combined_bathrooms': 'None', 'location_bathroom': 'None', 'bath': 'None', 'type_of_finishing_repairs': 'None', 'description': 'None', 'year_building_construction': 'None', 'status_land_plot': '', 'сeiling_height': 'None', 'passenger_elevator': 'None', 'freight_elevator': 'None', 'country': 'None', 'property_region': 'None', 'locality_name': 'None', 'sub_locality_name': 'None', 'address': 'None', 'apartment': 'None', 'direction': 'None', 'ring_road_distance': 'None', 'latitude': 'None', 'longitude': 'None', 'metro_name': 'None', 'time_on_foot': 'None', 'county_name': 'None', 'locality_name_id': 'None', 'metro_id': 'None', 'price_area_base_value': 'None', 'room_furniture': 'None', 'property_price': 'None', 'property_sale_price': 'None'})
    root = etree.fromstring(xmlstr)
    root_list = root.tag.split('}')[0]
    nsmap = ''.join(root_list) + '}'
    for element in root.getchildren():
        if element.tag != '{http://webmaster.yandex.ru/schemas/feed/realty/2010-06}generation-date':
            offer_id = element.get('internal-id')
            offer_dict['offer_id'] = offer_id
        for param in element.getchildren():
            if param.tag == nsmap + 'location':
                for item in param.getchildren():
                    if item.tag == nsmap + 'country':
                        offer_dict['property_region'] = item.text
                    elif item.tag == nsmap + 'region':
                        offer_dict['property_region'] = item.text
                    elif item.tag == nsmap + 'locality-name':
                        offer_dict['locality_name'] = item.text
                    elif item.tag == nsmap + 'sub-locality-name':
                        offer_dict['sub_locality_name'] = item.text
                    elif item.tag == nsmap + 'micro-locality-name':
                        offer_dict['name_cottage_settlement'] = item.text
                    elif item.tag == nsmap + 'address':
                        offer_dict['address'] = item.text
                    elif item.tag == nsmap + 'apartment':
                        offer_dict['apartment'] = item.text
                    elif item.tag == nsmap + 'direction':
                        offer_dict['direction'] = item.text
                    elif item.tag == nsmap + 'ring_road_distance':
                        offer_dict['ring_road_distance'] = item.text
                    elif item.tag == nsmap + 'latitude':
                        offer_dict['latitude'] = item.text
                    elif item.tag == nsmap + 'longitude':
                        offer_dict['longitude'] = item.text
                    elif item.tag == nsmap + 'metro':
                       for items in item.getchildren():
                           if items.tag == nsmap + 'name':
                               offer_dict['metro_name'] = items.text
                           elif items.tag == nsmap + 'time-on-foot':
                               offer_dict['time_on_foot'] = items.text
            elif param.tag == nsmap + 'price-area-base':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['price_area_base_value'] = item.text
            elif param.tag == nsmap + 'image':
                img = param.text.split('/')[-1]
                file = os.getcwd()
                os.chdir('result')
                text = 'image'+ offer_id
                if not os.path.isdir(text):
                    os.mkdir(text)
                    os.chdir(text)
                    p = requests.get(param.text)
                    with open(img, 'wb') as target:
                        target.write(p.content)
                        target.close()
                        os.chdir(file)
                else:
                    os.chdir(text)
                    p = requests.get(param.text)
                    with open(img, 'wb') as target:
                        target.write(p.content)
                        target.close()
                        os.chdir(file)
            elif param.tag == nsmap + 'price':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['property_price'] = item.text
            elif param.tag == nsmap + 'description':
                offer_dict['description'] = param.text
            elif param.tag == nsmap + 'area':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['total_area'] = item.text
            elif param.tag == nsmap + 'living-space':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['living_area'] = item.text
            elif param.tag == nsmap + 'room-space':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['area_room'] = item.text
            elif param.tag == nsmap + 'kitchen-space':
                for item in param.getchildren():
                    if item.tag == nsmap + 'value':
                        offer_dict['kitchen'] = item.text
            elif param.tag == nsmap + 'type':
                offer_dict['type_housing'] = param.text
            elif param.tag == nsmap + 'deal-status':
                offer_dict['deal_status'] = param.text
            elif param.tag == nsmap + 'property-type':
                offer_dict['property_status'] = param.text
            elif param.tag == nsmap + 'is_new_house':
                offer_dict['is_new_house'] = param.text
            elif param.tag == nsmap + 'building-type':
                offer_dict['type_house'] = param.text
            elif param.tag == nsmap + 'category':
                offer_dict['country_properties'] = param.text
            elif param.tag == nsmap + 'cadastral-number':
                offer_dict['cadastral_number'] = param.text
            elif param.tag == nsmap + 'ownership-type-name':
                offer_dict['type_permitted_use'] = param.text
            elif param.tag == nsmap + 'hot_water':
                offer_dict['water_supply'] = param.text
            elif param.tag == nsmap + 'heating_type':
                offer_dict['heating_type'] = param.text
            elif param.tag == nsmap + 'rooms-real':
                offer_dict['rooms'] = param.text
            elif param.tag == nsmap + 'floor':
                offer_dict['floor'] = param.text
            elif param.tag == nsmap + 'floors-total':
                offer_dict['total_floor_house'] = param.text
            elif param.tag == nsmap + 'balcony':
                offer_dict['balcony'] = param.text
            elif param.tag == nsmap + 'window-view':
                offer_dict['direction_windows'] = param.text
            elif param.tag == nsmap + 'bathroom-unit':
                offer_dict['separate_bathrooms'] = param.text
            elif param.tag == nsmap + 'bath':
                offer_dict['bath'] = param.text
            elif param.tag == nsmap + 'renovation':
                offer_dict['type_of_finishing_repairs'] = param.text
            elif param.tag == nsmap + 'furnish':
                offer_dict['type_of_finishing_repairs'] = offer_dict.get('type_of_finishing_repairs') + '; ' + param.text
            elif param.tag == nsmap + 'built-year':
                offer_dict['year_building_construction'] = param.text
            elif param.tag == nsmap + 'ceiling-height':
                offer_dict['сeiling_height'] = param.text
            elif param.tag == nsmap + 'lift':
                offer_dict['freight_elevator'] = param.text
            elif param.tag == nsmap + 'county_name':
                offer_dict['county_name'] = param.text
            elif param.tag == nsmap + 'metro-id':
                offer_dict['metro_id'] = param.text
            elif param.tag == nsmap + 'room-furniture':
                offer_dict['room_furniture'] = param.text
        df = pd.DataFrame(offer_dict, index=[0])
        dict.clear(offer_dict)
        full_df = full_df.append(df, ignore_index=True)
        print(full_df[['description']])
    return full_df
def getStringByUrl(url: str) -> str:
    return requests.get(url).text
if __name__ == "__main__":
    start()
