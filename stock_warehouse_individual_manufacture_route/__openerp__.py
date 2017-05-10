# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Individual Manufacture Route for Each Warehouse",
    "version": "8.0.1.0.1",
    "category": "Stock Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_warehouse_technical_information",
        "mrp",
    ],
    "data": [
        "views/stock_warehouse_views.xml",
    ],
}
