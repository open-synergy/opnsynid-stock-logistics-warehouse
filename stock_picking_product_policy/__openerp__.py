# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Product Policy",
    "version": "8.0.2.0.0",
    "category": "Stock",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_action_rule",
        "stock",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
    ],
}
