# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Account(surya.Sarpam):
    _name = "account.account"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    balance = fields.Float(string="Balance")
    type_id = fields.Many2one(comodel_name="account.type", string="Type", required=True)
    parent_id = ields.Many2one(comodel_name="account.account", string="Type", required=True)


