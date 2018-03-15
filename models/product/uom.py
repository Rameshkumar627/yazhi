# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("done", "Done")]


class UOM(surya.Sarpam):
    _name = "product.uom"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress")
