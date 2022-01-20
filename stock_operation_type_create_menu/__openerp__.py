# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Create Menu for Stock Operation Type",
    "version": "8.0.2.1.1",
    "summary": "Create Menu for Operation Type",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["stock"],
    "data": [
        "views/stock_operation_type_create_menu.xml",
        "views/stock_picking_type_view.xml",
        "views/stock_warehouse.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
