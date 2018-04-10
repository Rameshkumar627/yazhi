# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya


class Week(surya.Sarpam):
    _name = "week.week"
    _rec_name = 'name'

    name = fields.Char(string="Week", required=True)
    year_id = fields.Many2one(comodel_name="year.year", string="Year")
