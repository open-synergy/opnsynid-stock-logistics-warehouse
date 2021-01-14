# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Picking Location Policy",
    "version": "12.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "category": "Stock",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_picking_type_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_move_view.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
