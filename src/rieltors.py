import os
import requests
import pandas as pd
from lxml import etree


def start():
    url = 'http://topnlab.ru/export/main/database/?data=objects&chosen=1&format=yandex&key=WlyBG73La6uYi5Wa4XY'

    full_df = parseXML(getStringByUrl(url))
    file = os.getcwd()+'data.csv'

    # if os.path.exists(file):
    #
    # try:
    #   read_df = patd.read_csv(file)
    # except IOError as e:
    #   print(u'не удалось открыть файл')
    # else:
    #   with file:
    #     print(u'делаем что-то с файлом')
    full_df.to_csv(path_or_buf=file, sep=',', header=True, index=False, encoding='utf-8', mode='w')

    # data_file = pd.read_csv(path_data_file)                              #это создание из csv DataFrame
    pass


def parseXML(xml: str):
    full_df = pd.DataFrame()
    xmlList = xml.split('\n')[1:]  # удаляем ненужный заголовок
    xmlstr = '\n'.join(xmlList)

    root = etree.fromstring(xmlstr)

    for element in root.getchildren():
        tag_tree = ['location', 'price-area-base', 'image', 'price', 'description', 'area', 'living-space',
                    'room-space', 'kitchen-space']
        offer_dict = dict(
            {'offer_id': 'None', 'type_housing': 'None', 'deal_status': 'None', 'property_status': 'None', 'is_new_house': 'None',
             'type_house': 'None', 'type_house_height': 'None', 'type_new': 'None', 'country_properties': 'None',
             'rural_properties': 'None', 'commercial_property': 'None', 'name_cottage_settlement': 'None', 'cadastral_number': 'None',
             'land_category': 'None', 'type_permitted_use': 'None', 'investment_project': 'None', 'electro_supply': 'None',
             'water_supply': 'None', 'heating_type': 'None', 'gas_supply': 'None', 'parking_type': 'None', 'underground_parking': 'None',
             'type_of_sewer': 'None', 'chute': 'None', 'access_roads': 'None', 'ramp': 'None', 'price_for_hundred': 'None',
             'vacation_rentals': 'None', 'minimum_rental_period': 'None', 'prepayment': 'None', 'type_of_lease': 'None',
             'developer': 'None', 'deadline_year': 'None', 'deadline_quarter': 'None', 'rooms': 'None', 'rooms_for_rent': 'None',
             'layout_room': 'None', 'total_area': 'None', 'area_room': 'None', 'living_area': 'None', 'land_plot_area': 'None',
             'total_rooms_apartment': 'None', 'floor': '', 'total_floor_house': 'None', 'number_of_bedrooms': 'None', 'kitchen': 'None',
             'loggia': 'None', 'balcony': 'None', 'direction_windows': 'None', 'separate_bathrooms': 'None', 'combined_bathrooms': 'None',
             'location_bathroom': 'None', 'bath': 'None', 'type_of_finishing_repairs': 'None', 'description': 'None',
             'year_building_construction': 'None', 'status_land_plot': '', 'сeiling_height': 'None', 'passenger_elevator': 'None',
             'freight_elevator': 'None', 'country': 'None', 'property_region': 'None', 'locality_name': 'None', 'sub_locality_name': 'None',
             'address': 'None', 'apartment': 'None', 'direction': 'None', 'ring_road_distance': 'None', 'latitude': 'None', 'longitude': 'None',
             'metro_name': 'None', 'time_on_foot': 'None', 'county_name': 'None', 'locality_name_id': 'None', 'metro_id': 'None',
             'price_area_base_value': 'None', 'room_furniture': 'None', 'property_price': 'None', 'property_sale_price': 'None',
             'image': 'None'})

        if element.tag != '{http://webmaster.yandex.ru/schemas/feed/realty/2010-06}generation-date':

            offer_id = element.get('internal-id')
            offer_dict['offer_id'] = offer_id
            for elements in element.getchildren():
                for param in elements.getchildren():
                    if param.tag in set(tag_tree):
                        if param.tag == 'location':
                            for elem in param.getchildren():
                                if elem.tag == 'micro-locality-name':
                                    offer_dict['name_cottage_settlement'] = elem.text
                                elif elem.tag == 'region':
                                    offer_dict['property_region'] = elem.text
                                elif elem.tag == 'locality-name':
                                    offer_dict['locality_name'] = elem.text
                                elif elem.tag == 'sub-locality-name':
                                    offer_dict['sub_locality_name'] = elem.text
                                elif elem.tag == 'address':
                                    offer_dict['address'] = elem.text
                                elif elem.tag == 'apartment':
                                    offer_dict['apartment'] = elem.text
                                elif elem.tag == 'direction':
                                    offer_dict['direction'] = elem.text
                                elif elem.tag == 'ring_road_distance':
                                    offer_dict['ring_road_distance'] = elem.text
                                elif elem.tag == 'latitude':
                                    offer_dict['latitude'] = elem.text
                                elif elem.tag == 'longitude':
                                    offer_dict['longitude'] = elem.text
                                elif elem.tag == 'metro':
                                    for metro in elem.getchildren():
                                        if metro.tag == 'name':
                                            offer_dict['metro_name'] = metro.text
                                        elif metro.tag == 'time-on-foot':
                                            offer_dict['time_on_foot'] = metro.text
                                        else:
                                            break
                                elif elem.tag == 'locality-name-id':
                                    offer_dict['locality_name_id'] = elem.text
                        elif param.tag == 'price-area-base':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['price_area_base_value'] = elem.text
                        elif param.tag == 'image':
                            offer_dict['image'] = offer_dict.get('image')+'; '+param.text
                        elif param.tag == 'price':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['property_price'] = elem.text
                        elif param.tag == 'description':
                            offer_dict['description'] = param.text
                        elif param.tag == 'area':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['total_area'] = elem.text
                        elif param.tag == 'living-space':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['living_area'] = elem.text
                        elif param.tag == 'room-space':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['area_room'] = elem.text
                        elif param.tag == 'kitchen-space':
                            for elem in param.getchildren():
                                if elem.tag == 'value':
                                    offer_dict['kitchen'] = elem.text
                    elif param.tag == 'type':
                        offer_dict['type_housing'] = param.text
                    elif param.tag == 'deal-status':
                        offer_dict['deal_status'] = param.text
                    elif param.tag == 'property-type':
                        offer_dict['property_status'] = param.text
                    elif param.tag == 'is_new_house':
                        offer_dict['is_new_house'] = param.text
                    elif param.tag == 'building-type':
                        offer_dict['type_house'] = param.text
                    elif param.tag == 'cadastral-number':
                        offer_dict['cadastral_number'] = param.text
                    elif param.tag == 'ownership-type-name':
                        offer_dict['type_permitted_use'] = param.text
                    elif param.tag == 'hot_water':
                        offer_dict['water_supply'] = param.text
                    elif param.tag == 'heating_type':
                        offer_dict['heating_type'] = param.text
                    elif param.tag == 'rooms-real':
                        offer_dict['rooms'] = param.text
                    elif param.tag == 'floor':
                        offer_dict['floor'] = param.text
                    elif param.tag == 'floors-total':
                        offer_dict['total_floor_house'] = param.text
                    elif param.tag == 'balcony':
                        offer_dict['balcony'] = param.text
                    elif param.tag == 'window-view':
                        offer_dict['direction_windows'] = param.text
                    elif param.tag == 'bathroom-unit':
                        offer_dict['separate_bathrooms'] = param.text
                    elif param.tag == 'bath':
                        offer_dict['bath'] = param.text
                    elif param.tag == 'renovation':
                        offer_dict['type_of_finishing_repairs'] = param.text
                    elif param.tag == 'furnish':
                        offer_dict['type_of_finishing_repairs'] = offer_dict.get('type_of_finishing_repairs')+'; '+param.text
                    elif param.tag == 'built-year':
                        offer_dict['year_building_construction'] = param.text
                    elif param.tag == 'ceiling-height':
                        offer_dict['сeiling_height'] = param.text
                    elif param.tag == 'lift':
                        offer_dict['freight_elevator'] = param.text
                    elif param.tag == 'county_name':
                        offer_dict['county_name'] = param.text
                    elif param.tag == 'metro-id':
                        offer_dict['metro_id'] = param.text
                    elif param.tag == 'room-furniture':
                        offer_dict['room_furniture'] = param.text

                    print(offer_dict)

            df = pd.DataFrame(offer_dict, index=[0])
            print(df)
            dict.clear(offer_dict)
            full_df = full_df.append(df, ignore_index=True)
    print(full_df)
    return full_df


def getStringByUrl(url: str) -> str:
    return requests.get(url).text


if __name__ == "__main__":
    start()
