# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# City

class City(surya.Sarpam):
    _name = "res.city"

    name = fields.Char(string="City", required=True)
