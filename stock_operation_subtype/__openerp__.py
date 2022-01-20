# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Operation Subtype",
    "version": "8.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "category": "Stock",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_picking_subtype_data.xml",
        "views/stock_picking_subtype_views.xml",
        "views/stock_picking_type_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "license": "AGPL-3",
    "installable": True,
    "post_init_hook": "update_existing_picking_type",
}
