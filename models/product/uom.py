# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product UOM
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class UOM(surya.Sarpam):
    _name = "product.uom"
    _rec_name = "code"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress", default="draft")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! UOM Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! UOM must be unique')]
