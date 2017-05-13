# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Waste Operation",
    "version": "8.0.1.0.2",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "category": "Stock Management",
    "depends": [
        "stock_warehouse_technical_information",
        "stock_operation_type_location",
    ],
    "data": [
        "views/stock_warehouse_view.xml"
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "license": "AGPL-3",
}
