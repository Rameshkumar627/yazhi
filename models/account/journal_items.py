# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class JournalItems(surya.Sarpam):
    _name = "journal.items"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date", required=True)
    reference = fields.Char(string="Reference", required=True)
    posting_id = fields.Many2one(comodel_name="journal.posting", string="Journal Posting", required=True)
    period_id = fields.Many2one(comodel_name="period.period", string="Period", required=True)
    credit = fields.Float(string="Credit")
    debit = fields.Float(string="Debit")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    reconcile = fields.Many2one(comodel_name="journal.items", string="Reconcile Ref")
    journal_id = fields.Many2one(comodel_name="journal.entry", string="Journal")
