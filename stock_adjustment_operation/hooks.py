# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    create_adjustment_for_existing_company(env)


def create_adjustment_for_existing_company(env):
    criteria = [
        ("adjustment_type_id", "=", False),
    ]
    obj_company = env["res.company"]
    for company in obj_company.search(criteria):
        adj_type = company._create_adjustment_type()
        company.write({
            "adjustment_type_id": adj_type.id
        })
