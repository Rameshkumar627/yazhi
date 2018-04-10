# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Language

class Language(surya.Sarpam):
    _name = "res.language"

    name = fields.Char(string="Language", required=True)
