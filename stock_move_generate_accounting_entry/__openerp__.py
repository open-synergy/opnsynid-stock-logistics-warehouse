# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Move Generate Accounting Entry",
    "version": "8.0.1.1.0",
    "category": "Stock Management",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_move_line_stock_info",
    ],
    "data": [
        "wizards/generate_stock_move_account_entry_views.xml",
        "views/stock_move_view.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
