# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Production Operation",
    "version": "12.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "category": "Stock Management",
    "depends": [
        "stock_warehouse_technical_information",
        "stock_picking_location_policy",
    ],
    "data": [
        "views/stock_warehouse_view.xml"
    ],
    "installable": True,
    "license": "AGPL-3",
}
