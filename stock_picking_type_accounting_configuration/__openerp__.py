# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Type Accounting Configuration",
    "version": "8.0.1.1.0",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_move_account_source_data.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_move_account_source_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
