# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Waste Operation",
    "version": "8.0.1.1.5",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "category": "Stock Management",
    "depends": [
        "stock_warehouse_technical_information",
        "stock_operation_type_location",
        "stock_operation_subtype",
    ],
    "data": ["data/stock_picking_subtype_data.xml", "views/stock_warehouse_view.xml"],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "license": "AGPL-3",
}
