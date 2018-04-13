# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'Approved')]


# Voucher
class Voucher(surya.Sarpam):
    _name = "employee.voucher"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    amount = fields.Float(string="Amount")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
