# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Attendance

PROGRESS_INFO = [('draft', 'draft'), ('closed', 'Closed')]
AVAIL_PROGRESS = [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')]
DAY_PROGRESS = [('holiday', 'Holiday'), ('working_day', 'Working Day')]


class TimeAttendance(surya.Sarpam):
    _name = "time.attendance"

    date = fields.Date(string="Date")
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month")
    attendance_detail = fields.One2many(comodel_name="time.attendance.detail",
                                        inverse_name="attendance_id",
                                        string="Attendance Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")


class TimeAttendanceDetail(surya.Sarpam):
    _name = "time.attendance.detail"

    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    attendance_id = fields.Many2one(comodel_name="time.attendance", string="Attendance")
    expected_from_time = fields.Datetime(string="Expected From Time")
    actual_from_time = fields.Datetime(string="Actual From Time")
    expected_till_time = fields.Datetime(string="Expected Till Time")
    actual_till_time = fields.Datetime(string="Actual Till Time")
    expected_hours = fields.Float(string="Expected Hours", default=0)
    actual_hours = fields.Float(string="Actual Hours", default=0)
    day_progress = fields.Selection(DAY_PROGRESS, string='Progress')
    availability_progress = fields.Selection(AVAIL_PROGRESS, string='Progress', compute="_get_availability_progress")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='attendance_id.progress')

    @api.multi
    def update_hours(self):
        if self.expected_from_time and self.expected_till_time:
            expected_from_time = datetime.strptime(self.expected_from_time, "%Y-%m-%d %H:%M:%S")
            expected_till_time = datetime.strptime(self.expected_till_time, "%Y-%m-%d %H:%M:%S")
            self.expected_hours = (expected_till_time - expected_from_time).total_seconds()/(60 * 60 * 24)

        if self.actual_from_time and self.actual_till_time:
            actual_from_time = datetime.strptime(self.actual_from_time, "%Y-%m-%d %H:%M:%S")
            actual_till_time = datetime.strptime(self.actual_till_time, "%Y-%m-%d %H:%M:%S")
            self.actual_hours = (actual_till_time - actual_from_time).total_seconds() / (60 * 60 * 24)

    @api.depends('actual_hours')
    def _get_availability_progress(self):
        full_day = self.env["time.configuration"].search([('name', '=', 'Full Day')])
        half_day = self.env["time.configuration"].search([('name', '=', 'Half Day')])
        if self.actual_hours >= full_day.value:
            self.availability_progress = "full_day"
        elif self.actual_hours >= half_day.value:
            self.availability_progress = "half_day"
        else:
            self.availability_progress = "absent"

    _sql_constraints = [('unique_attendance',
                         'unique (attendance_id, employee_id)',
                         'Error! Employee should not repeated')]
