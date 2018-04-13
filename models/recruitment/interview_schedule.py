# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("scheduled", "Scheduled"),
                 ("cancelled", "Cancelled"),
                 ("on_process", "On Process"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"),
               ("selected", "Selected"),
               ("rejected", "Rejected"),
               ("on_hold", "On Hold")]


# Interview Schedule
class InterviewSchedule(surya.Sarpam):
    _name = "interview.schedule"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position")
    interview_id = fields.Many2one(comodel_name="interview.schedule", string="Previous Interview")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default='draft')
    interview_detail = fields.One2many(comodel_name="interview.schedule",
                                       inverse_name="interview_id",
                                       string="Interview Detail")
    scheduled_detail = fields.One2many(comodel_name="interview.schedule.detail",
                                       string="Scheduled Detail",
                                       inverse_name="scheduled_id")

    @api.multi
    def trigger_start_process(self):
        self.write({"progress": "on_process"})

    @api.multi
    def trigger_cancelled(self):
        self.write({"progress": "cancelled"})

    @api.multi
    def trigger_scheduled(self):
        self.write({"progress": "scheduled"})

    @api.multi
    def trigger_completed(self):
        self.write({"progress": "completed"})


class InterviewScheduledDetail(surya.Sarpam):
    _name = "interview.schedule.detail"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    scheduled_id = fields.Many2one(comodel_name="interview.schedule", string="Interview")
    status = fields.Selection(selection=STATUS_INFO, string="Status")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='scheduled_id.progress')

