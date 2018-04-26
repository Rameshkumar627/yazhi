# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# HR Pay

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]
PAY_TYPE = [('allownace', 'Allowance'), ('deduction', 'Deduction')]


class PayrollGeneration(surya.Sarpam):
    _name = "payroll.generation"
    _inherit = "mail.thread"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    basic = fields.Float(string="Basic")
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")



