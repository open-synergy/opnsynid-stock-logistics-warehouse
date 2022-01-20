# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking View Layout - Multi Address Ext",
    "version": "8.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "category": "Stock Management",
    "depends": [
        "stock_transport_multi_address",
        "stock_picking_view_layout",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_picking_type_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "license": "AGPL-3",
}
