# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
from lxml import etree


# Week Schedule

PROGRESS_INFO = [('draft', 'draft'), ('closed', 'Closed')]


class MonthAttendance(surya.Sarpam):
    _name = "month.attendance"
    _rec_name = "period_id"

    period_id = fields.Many2one(comodel_name="period.period", string="Month")
    month_detail = fields.One2many(comodel_name="time.attendance",
                                   inverse_name="month_id",
                                   string="Month Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")

    @api.multi
    def trigger_closed(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        data = {"progress": "verified"}
        self.write(data)

    @api.multi
    def trigger_monthly_attendance_report(self):
        pass
