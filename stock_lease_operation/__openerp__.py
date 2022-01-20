# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Leasing Operation",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_warehouse_technical_information",
        "stock_operation_type_location",
        "stock_route_transit",
        "stock_push_rule_picking_type",
        "stock_pull_rule_picking_type",
        "stock_operation_subtype",
    ],
    "data": [
        "data/stock_picking_subtype_data.xml",
        "data/stock_location_datas.xml",
        "data/ir_property_datas.xml",
        "views/res_partner_views.xml",
        "views/stock_warehouse_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
