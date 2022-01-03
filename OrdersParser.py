#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from json import dump
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import re

# pip install beautifulsoup4
product_name = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Link__link__cmgtoz " \
               "ali-kit_Link__size-xs__cmgtoz ali-kit_Link__default__cmgtoz " \
               "OrderList_TradeProductInfo__productTitle__18tx4 "


def tag2json(row, pattern=True):
    t = '[Transaction Screenshot]'
    draft = r'Order ID:.(?P<orderNum>\d+).View DetailOrder time:.(?P<date>.*)Store name:.(?P<storeName>.+)View StoreContact SellerOrder amount:.\$ (?P<fullprice>\d+\.\d\d)(?P<product>.+)\[Transaction Screenshot\]\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    price = r'\$ (?P<price_per_1>\d+\.\d\d) X(?P<amount>\d+)'
    products = soup.find_all(class_=product_name)
    if row.count(t) == 1 and pattern:
        info = re.finditer(draft, row)
        for m in info:
            return {'shop': m.group('storeName'), 'order ID': m.group('orderNum'),
                    'paid': m.group('fullprice'), 'date': m.group('date'),
                    'details': [{'product': m.group('product'), 'amount': m.group('amount'),
                                 'price_per_1': m.group('price_per_1')}]}
    elif row.count(t) == 1:
        for tag in products:
            if tag.get_text() in row:
                newrow = row.split('[Transaction Screenshot]')[-1]
                info = re.finditer(price, newrow)
                for n in info:
                    return {'price_per_1': n.group('price_per_1'),
                            'product': tag.get_text(), 'amount': n.group('amount')}
    else:
        parts = row.split(t)
        part = t.join(row.split(t)[:2])
        x = tag2json(part, True)
        for i in range(1, len(parts) - 1):
            part = t.join(row.split(t)[i: i + 2])
            x['details'].append(tag2json(part, False))
        return x


if __name__ == '__main__':
    parser = ArgumentParser(description='Document Taxonomy Builder.',
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('-fpath', '--filepath', type=str,
                        help='Path to a html file with orders')
    parser.add_argument('-o', '--outp-filename', default='orders.json',
                        help='Output json file with orders info')

    args = parser.parse_args()

    with open(args.filepath, 'r', encoding="utf-8") as f:  # 'AliExpressTransactions.htm'
        x = []
        soup = BeautifulSoup(f, 'html.parser')
        mydivs = soup.findAll("div", {"class": None})

        # delete unnecessary tags
        for obj in mydivs.copy():
            if 'Order ID:' != obj.get_text()[:9] or "$" not in obj.get_text():
                mydivs.remove(obj)
        for box in mydivs:
            if box.get_text().count('[Transaction Screenshot]'):
                # print(box.get_text())
                x.append(tag2json(box.get_text()))

        for el in x:
            print(el)
        with open(args.outp_filename, 'w') as file:
            dump(x, file)
