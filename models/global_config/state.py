# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# State

class State(surya.Sarpam):
    _name = "res.state"

    name = fields.Char(string="State", required=True)
