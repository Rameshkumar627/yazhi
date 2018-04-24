# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

# Time Sheet Application


class TimeSheetApplication(surya.Sarpam):
    _name = "time.sheet.application"

    date = fields.Datetime(string="Date")

    @api.multi
    def trigger_employee_in(self):
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        data = {"employee_id": employee_id.id,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "progress": "in",
                "process": "automatic"}

        self.env["time.sheet"].create(data)

    @api.multi
    def trigger_employee_out(self):
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        data = {"employee_id": employee_id.id,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "progress": "out",
                "process": "automatic"}

        self.env["time.sheet"].create(data)

    def default_vals_creation(self, vals):
        vals["active"] = False
        return vals
