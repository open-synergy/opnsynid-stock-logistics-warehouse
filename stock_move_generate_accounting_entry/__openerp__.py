# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Move Generate Accounting Entry",
    "version": "8.0.1.1.0",
    "category": "Stock Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_move_line_stock_info",
    ],
    "data": [
        "wizards/generate_stock_move_account_entry_views.xml",
        "views/stock_move_view.xml",
    ],
}
