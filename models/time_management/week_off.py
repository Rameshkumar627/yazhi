# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya

# Week Off

PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'Approved')]


class WeekOff(surya.Sarpam):
    _name = "time.week.off"

    date = fields.Date(string="Date")
    week_off_detail = fields.One2many(comodel_name="time.week.off.detail",
                                      inverse_name="week_off_id",
                                      string="Week-Off Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress')

    def update_attendance(self):
        recs = self.week_off_detail

        for rec in recs:
            attendance = self.env["time.attendance.detail"].search([("employee_id", "=", rec.employee_id.id),
                                                                    ("attendance_id.date", "=", self.date)])

            if attendance:
                attendance.day_progress = 'holiday'
            else:
                raise exceptions.ValidationError("Error! please check")

    @api.multi
    def trigger_schedule(self):
        self.update_attendance()
        self.write({'progress': 'approved'})


class WeekOffDetail(surya.Sarpam):
    _name = "time.week.off.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    week_off_id = fields.Many2one(comodel_name="time.week.off", string="Week Off")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='week_off_id.progress')

