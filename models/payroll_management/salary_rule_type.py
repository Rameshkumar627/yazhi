# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Salary Rule Type

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


class SalaryRuleCode(surya.Sarpam):
    _name = "salary.rule.code"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')

