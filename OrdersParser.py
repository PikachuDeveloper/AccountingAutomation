#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
# pip install beautifulsoup4
product_name = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Link__link__cmgtoz ali-kit_Link__size-xs__cmgtoz ali-kit_Link__default__cmgtoz OrderList_TradeProductInfo__productTitle__18tx4"

def tag2json(row, pattern=True):
    draft = r'Order ID:.(?P<orderNum>\d+).View DetailOrder time:.Store name:.(?P<storeName>.+)View StoreContact SellerOrder amount:.\$ (?P<fullprice>\d+\.\d\d)(?P<product>.+)\[Transaction Screenshot\]\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    price = r'\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    products = soup.find_all(class_=product_name)
    if row.count('[Transaction Screenshot]') == 1 and pattern:
        info = re.finditer(draft, row)
        for m in info:
            return {'shop': m.group('storeName'), 'price_per_1': m.group('price_per_1'),
                   'order ID': m.group('orderNum'), 'paid': m.group('fullprice'),
                   'product': m.group('product'), 'amount': m.group('amount')}
    elif row.count('[Transaction Screenshot]') == 1:
        for tag in products:
            if tag.get_text() in row:
                n = re.finditer(price, row)
                return {'shop': m.group('storeName'), 'price_per_1': n.group('price_per_1'),
                         'order ID': m.group('orderNum'), 'paid': m.group('fullprice'),
                         'product': tag.get_text(), 'amount': n.group('amount')}
    else:
        x = {}
        parts = row.split('[Transaction Screenshot]')[:2]
        part = '[Transaction Screenshot]'.join(row.split('[Transaction Screenshot]')[:2])
        x.update(tag2json(part, True))
        for i in range(1, len(parts)-1):
            part = '[Transaction Screenshot]'.join(row.split('[Transaction Screenshot]')[:2])
            x.update(tag2json(part, False))
        return x


with open('AliExpressTransactions.htm', 'r', encoding="utf-8") as f:

    #contents = f.read()
    x = []
    soup = BeautifulSoup(f, 'html.parser')
    mydivs = soup.findAll("div", {"class": None})
    class_num = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Label__label__1n9sab ali-kit_Label__size-xs__1n9sab"
    product_name = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Link__link__cmgtoz ali-kit_Link__size-xs__cmgtoz ali-kit_Link__default__cmgtoz OrderList_TradeProductInfo__productTitle__18tx4"
    orders = soup.findAll("span", {"class": class_num})
    # id = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub price ali-kit_Price__size-xs__12ybyf OrderList_TradeProductInfo__productAmount__18tx4"
    # seven_day = soup.find(id="seven-day-forecast")
    shopNum = soup.find_all(class_=class_num)
    shopNum = list(map(lambda x: x.get_text(), shopNum))
    shopNum = list(filter(('').__ne__, shopNum))
    draft = r'Order ID:.(?P<orderNum>\d+).View DetailOrder time:.Store name:.(?P<storeName>.+)View StoreContact SellerOrder amount:.\$ (?P<fullprice>\d+\.\d\d)(?P<product>.+)\[Transaction Screenshot\]\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    price = r'\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    info = re.finditer(draft, mydivs[0].get_text())
    for m in info:
        print(m.group('orderNum'))
    # class_prod = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Link__link__cmgtoz ali-kit_Link__size-xs__cmgtoz ali-kit_Link__default__cmgtoz OrderList_TradeProductInfo__productTitle__18tx4"
    # products = soup.findAll("a", {"class": class_prod})
    #
    # for i in products:
    #     print(i.get_text())

    #prints everything
    for obj in mydivs.copy():
        if 'Order ID:' != obj.get_text()[:9] or "$" not in obj.get_text():
            mydivs.remove(obj)
    for box in mydivs:
        if box.get_text().count('[Transaction Screenshot]'):
            x.append(tag2json(box.get_text()))

    for el in x:
        print(el)
    # print(x)
    print(len(x))

