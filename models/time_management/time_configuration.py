# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Time Configuration

PROGRESS_INFO = [('draft', 'draft'), ('closed', 'Closed')]


class TimeConfiguration(surya.Sarpam):
    _name = "time.configuration"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    value = fields.Float(string="Value")
