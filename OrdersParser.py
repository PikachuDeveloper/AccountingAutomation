#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

with open('AliExpressTransactions.htm', 'r', encoding="utf-8") as f:

    #contents = f.read()

    soup = BeautifulSoup(f, 'html.parser')
    mydivs = soup.findAll("div", {"class": None})
    class_ = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Label__label__1n9sab ali-kit_Label__size-xs__1n9sab"
    # id = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub price ali-kit_Price__size-xs__12ybyf OrderList_TradeProductInfo__productAmount__18tx4"
    # seven_day = soup.find(id="seven-day-forecast")
    d = soup.div
    forecast_items = soup.find_all(class_=class_)
    forecast_items = list(map(lambda x: x.get_text(), forecast_items))
    forecast_items = list(filter(('').__ne__, forecast_items))

    #prints everything
    for i in mydivs:
        if 'Order ID:' == i.get_text()[:9]:
            print(i.get_text())

    #prints only order number and shop name
    # for i in range(0, len(forecast_items), 4):
    #     print('Order number: ', forecast_items[i])
    #     print('Shop: ', forecast_items[i+1])
    #     print('?: ', forecast_items[i+2])
    #     print('?: ', forecast_items[i+3])
    #     print('---------------------------------------------')


#soup = BeautifulSoup(contents, 'html')
# class="OrderList_OrderItem__row__9lg56 OrderList_OrderItem__productItemWrap__9lg56"
#
# class ="OrderList_OrderItem__row__9lg56 OrderList_OrderItem__productItemWrap__9lg56"
# class ="OrderList_OrderItem__row__9lg56"
# class ="ali-kit_Col__col__1lcv7b ali-kit_Col__col-6__1lcv7b"
# class ="OrderList_TradeProductInfo__wrapper__18tx4 OrderList_OrderItem__productCell__9lg56"
#
# class ="ali-kit_Base__base__1odrub ali-kit_Base__light__1odrub ali-kit_Label__label__1n9sab ali-kit_Label__size-xs__1n9sab"
#
#
# class ="product-policy_ProductPolicy__wrapper__to6hoe"