# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Donation Operation",
    "version": "8.0.1.0.1",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "category": "Stock Management",
    "depends": [
        "stock_warehouse_technical_information",
        "stock_operation_type_location",
        "stock_route_transit",
        "stock_push_rule_picking_type",
        "stock_pull_rule_picking_type",
    ],
    "data": [
        "data/stock_picking_subtype_data.xml",
        "data/stock_location_datas.xml",
        "data/ir_property_datas.xml",
        "views/res_partner_views.xml",
        "views/stock_warehouse_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
