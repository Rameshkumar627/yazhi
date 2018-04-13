# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Notes
class Noted(surya.Sarpam):
    _name = "hospital.notes"

    from_time = fields.Datetime(string="From time")
    notes = fields.Text(string="Notes")
