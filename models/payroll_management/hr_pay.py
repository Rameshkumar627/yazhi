# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# HR Pay
class HRPay(surya.Sarpam):
    _name = "hr.pay"
    _inherit = "mail.thread"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(comodel_name="hr.employee",
                                  string="Employee",
                                  track_visibility='onchange',
                                  readonly=True)
    basic = fields.Float(string="Basic", track_visibility='onchange', readonly=True)
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')
    structure_id = fields.Many2one(comodel_name="salary.structure",
                                   string="Salary Structure",
                                   track_visibility='onchange',
                                   readonly=True)

    _sql_constraints = [('name_uniq', 'unique(employee_id)', 'Payscale is already configured')]
