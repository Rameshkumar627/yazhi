# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class ProductGroup(surya.Sarpam):
    _name = "product.group"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress")
