# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Do Not Create Accounting Entry on Inventory Revaluation",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_inventory_revaluation_extend",
    ],
    "data": [
        "views/stock_inventory_revaluation_views.xml",
    ],
}
