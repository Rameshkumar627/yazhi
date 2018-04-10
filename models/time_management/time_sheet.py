# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Time Sheet

PROGRESS_INFO = [('in', 'In'), ('out', 'Out')]
PROCESS_INFO = [('manual', 'Manual'), ('automatic', 'Automatic')]


class TimeSheet(surya.Sarpam):
    _name = "time.sheet"

    date = fields.Datetime(string="Date")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    progress = fields.Selection(PROGRESS_INFO, string='Progress')
    process = fields.Selection(PROCESS_INFO, string='Process', default="automatic")

    def default_vals_creation(self, vals):
        current_time = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.strptime(self.date, "%Y-%m-%d")

        if 'in' in self.progress:
            accepted_time = self.env["time.configuration"].search([("name", "=", "IN Grace Time")])
            time = current_time - timedelta(minutes=accepted_time.value)
            attendance = self.env["time.attendance.detail"].search(
                [("expected_from_time", ">=", time.strftime("%Y-%m-%d %H:%M:%S")),
                 ("attendance_id.date", "=", current_date)])

            attendance.write({"actual_from_time": current_date})

        elif 'out' in self.progress:
            accepted_time = self.env["time.configuration"].search([("name", "=", "OUT Grace Time")])
            time = current_time + timedelta(minutes=accepted_time.value)
            attendance = self.env["time.attendance.detail"].search(
                [("expected_till_time", ">=", time.strftime("%Y-%m-%d %H:%M:%S")),
                 ("attendance_id.date", "=", current_date)])

            attendance.write({"actual_till_time": current_date})
        return vals


