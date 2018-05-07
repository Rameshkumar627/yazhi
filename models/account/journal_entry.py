# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class JournalEntry(surya.Sarpam):
    _name = "journal.entry"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date", required=True)
    reference = fields.Char(string="Reference", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    items = fields.One2many(comodel_name="journal.items", string="Items", inverse_name="journal_id")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")



