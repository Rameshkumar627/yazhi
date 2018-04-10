# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Religion

class Religion(surya.Sarpam):
    _name = "res.religion"

    name = fields.Char(string="Religion", required=True)
