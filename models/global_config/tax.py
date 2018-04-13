# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


STATE_INFO = [("in", "Inter state"), ("out", "Outer State")]


# Tax
class Tax(surya.Sarpam):
    _name = "res.tax"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(selection=STATE_INFO, string="State")
    value = fields.Char(string="Value", required=True)
