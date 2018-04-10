# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Account Type
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class AccountType(surya.Sarpam):
    _name = "account.type"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
