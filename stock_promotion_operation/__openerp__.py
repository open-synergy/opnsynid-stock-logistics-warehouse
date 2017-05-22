# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Promotion Operation",
    "version": "8.0.2.0.0",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "category": "Stock Management",
    "depends": [
        "stock_warehouse_technical_information",
        "stock_operation_type_location",
        "stock_route_transit",
        "stock_push_rule_picking_type",
        "stock_pull_rule_picking_type",
    ],
    "data": [
        "data/stock_location_datas.xml",
        "data/ir_property_datas.xml",
        "views/res_partner_views.xml",
        "views/stock_warehouse_views.xml"
    ],
    "installable": True,
    "license": "AGPL-3",
}
