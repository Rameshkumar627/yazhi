# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave
class HRLeave(surya.Sarpam):
    _name = "hr.leave"

    month_id = fields.Many2one(comodel_name="period.period", string="Month")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level", required=True)
    leave_detail = fields.One2many(comodel_name="hr.leave.detail",
                                   inverse_name="hr_leave_id",
                                   string="HR Leave Detail")
    total_days = fields.Float(string="Total Days")
    total_present = fields.Float(string="Total Present")
    total_absent = fields.Float(string="Total Absent")
    total_working_days = fields.Float(string="Total Working Days")
    total_holidays = fields.Float(string="Total Holidays")
    total_lop = fields.Float(string="Total LOP")

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")

    _sql_constraints = [('unique_leave_period',
                         'unique (month_id, employee_id)',
                         'Error! Leave period should not be repeated')]


class HRLeaveDetail(surya.Sarpam):
    _name = "hr.leave.detail"

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True, readonly=True)
    opening_balance = fields.Float(string="Opening Balance", readonly=True)
    increment = fields.Float(string="Increment")
    leave_taken = fields.Float(string="Leave Taken")
    closing_balance = fields.Float(string="Closing Balance", readonly=True)
    order = fields.Integer(string="Order Sequence")
    hr_leave_id = fields.Many2one(comodel_name="hr.leave", string="HR Leave")

    _sql_constraints = [('unique_leave_type',
                         'unique (leave_type_id, hr_leave_id)',
                         'Error! Leave Type should not be repeated')]