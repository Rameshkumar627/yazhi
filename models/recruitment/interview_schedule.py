# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

SCHEDULE_INFO = [("draft", "Draft"),
                 ("scheduled", "Scheduled"),
                 ("cancelled", "Cancelled"),
                 ("on_process", "On Process"),
                 ("completed", "Completed")]

SCHEDULE_DETAIL_INFO = [("draft", "Draft"),
                        ("selected", "Selected"),
                        ("rejected", "Rejected"),
                        ("on_hold", "On Hold")]


# Interview Schedule
class InterviewSchedule(surya.Sarpam):
    _name = "interview.schedule"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    vacancy_id = fields.Many2one(comodel_name="vacancy.position", string="Vacancy Position")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position")
    progress = fields.Selection(selection=SCHEDULE_INFO, string="Progress", default='draft')
    scheduled_detail = fields.One2many(comodel_name="interview.schedule.detail",
                                       string="Scheduled Detail",
                                       inverse_name="scheduled_id")


class InterviewScheduledDetail(surya.Sarpam):
    _name = "interview.schedule.detail"
    _inherit = "mail.thread"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    scheduled_id = fields.Many2one(comodel_name="interview.schedule", string="Interview")
    status = fields.Selection(selection=SCHEDULE_DETAIL_INFO, string="Status")
    progress = fields.Selection(SCHEDULE_INFO, string='Progress', related='scheduled_id.progress')

