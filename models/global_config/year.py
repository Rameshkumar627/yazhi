# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya


class Year(surya.Sarpam):
    _name = "year.year"
    _rec_name = 'name'

    name = fields.Char(string="Year", required=True)
    financial_year = fields.Char(string="Financial Year", required=True)
    period_detail = fields.One2many(comodel_name="period.period",
                                    inverse_name="year_id",
                                    string="Period",
                                    readonly=True)
