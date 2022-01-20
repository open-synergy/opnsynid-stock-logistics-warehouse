# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Picking/Move Policy Based on Subtype - Multi Address",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_picking_subtype_policy",
    ],
    "data": [
        "views/stock_picking_subtype_views.xml",
        "views/stock_picking_views.xml",
    ],
    "demo": [],
    "images": [
        "static/description/banner.png",
    ],
}
