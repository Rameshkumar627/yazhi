# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Week Schedule

PROGRESS_INFO = [('draft', 'Draft'), ('scheduled', 'Scheduled')]


class WeekSchedule(surya.Sarpam):
    _name = "week.schedule"

    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    schedule_detail = fields.One2many(comodel_name="week.schedule.detail",
                                      inverse_name="schedule_id",
                                      string="Schedule Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")

    def check_date(self):
        """ From Date < Till Date """
        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.till_date, "%Y-%m-%d")
        if from_date > till_date:
            raise exceptions.ValidationError("Error! From Date should be greater than Till Date")

        """ From Date is a week start """
        from_date_current_week = from_date.strftime("%W")
        last_week = from_date - timedelta(days=1)
        from_date_last_week = last_week.strftime("%W")

        if from_date_current_week != from_date_last_week:
            raise exceptions.ValidationError("Error! From Date should be a week start")

        """ Till Date is a week end """
        till_date_current_week = till_date.strftime("%W")
        next_week = from_date + timedelta(days=1)
        till_date_next_week = next_week.strftime("%W")

        if till_date_current_week != till_date_next_week:
            raise exceptions.ValidationError("Error! Till Date should be a week end")

    def generate_attendance(self):
        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.till_date, "%Y-%m-%d")
        date_range = (till_date - from_date).days + 1

        recs = self.schedule_detail

        for day in range(0, date_range):
            current_date_obj = from_date + timedelta(days=day)
            next_date_obj = current_date_obj + timedelta(days=1)
            current_date = current_date_obj.strftime("%Y-%m-%d")
            next_date = next_date_obj.strftime("%Y-%m-%d")

            attendance_detail = []
            for rec in recs:
                expected_from_time = "{0} {1}:{2}:00.0".format(current_date,
                                                               rec.shift_id.from_hours,
                                                               rec.shift_id.from_minutes)

                if rec.shift_id.end_day == 'current_day':
                    expected_till_time = "{0} {1}:{2}:00.0".format(current_date,
                                                                   rec.shift_id.till_hours,
                                                                   rec.shift_id.till_minutes)
                elif rec.shift_id.end_day == 'next_day':
                    expected_till_time = "{0} {1}:{2}:00.0".format(next_date,
                                                                   rec.shift_id.till_hours,
                                                                   rec.shift_id.till_minutes)

                attendance_detail.append((0, 0, {"shift_id": rec.shift_id.id,
                                                 "employee_id": rec.employee_id.id,
                                                 "expected_from_time": expected_from_time,
                                                 "expected_till_time": expected_till_time}))

            month_id = self.env["month.attendance"].search([("period_id.from_date", ">=", current_date),
                                                            ("period_id.till_date", "<=", current_date)])

            if not month_id:
                raise exceptions.ValidationError("Error! Attendance Month is not set")

            self.env["time.attendance"].create({"date": current_date,
                                                "month_id": month_id,
                                                "attendance_detail": attendance_detail})

    @api.multi
    def trigger_schedule(self):
        self.check_date()
        self.generate_attendance()
        self.write({'progress': 'scheduled'})


class WeekScheduleDetail(surya.Sarpam):
    _name = "week.schedule.detail"

    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    schedule_id = fields.Many2one(comodel_name="week.schedule", string="Schedule")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='schedule_id.progress')
