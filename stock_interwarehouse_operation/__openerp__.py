# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Inter-Warehouse Product Movement",
    "version": "8.0.1.2.0",
    "summary": "More control to inter-warehouse product movements",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "category": "Stock Management",
    "depends": [
        "stock_route_transit",
        "stock_operation_type_location",
        "stock_warehouse_technical_information",
        "stock_operation_subtype",
    ],
    "data": [
        "data/stock_picking_subtype_data.xml",
        "views/stock_warehouse_view.xml"
    ],
    "installable": True,
    "license": "AGPL-3",
}
