# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class HospitalLocation(surya.Sarpam):
    _name = "hospital.location"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")

