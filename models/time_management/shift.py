# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Shift Master

PROGRESS_INFO = [('draft', 'draft'), ('confirmed', 'Confirmed')]
END_INFO = [('current_day', 'Current Day'), ('next_day', 'Next Day')]


class Shift(surya.Sarpam):
    _name = "time.shift"

    name = fields.Char(string="Shift", required=True)
    total_hours = fields.Float(string="Total Hours", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    end_day = fields.Selection(selection=END_INFO, string="Ends On")
    from_hours = fields.Integer(string="From Hours")
    from_minutes = fields.Integer(string="From Minutes")
    till_hours = fields.Integer(string="Till Hours")
    till_minutes = fields.Integer(string="Till Minutes")

    @api.multi
    def trigger_calculate(self):
        total_from_hours = (self.from_hours * 60) + self.from_minutes
        total_till_hours = (self.till_hours * 60) + self.till_minutes
        if self.end_day == 'current_day':
            self.total_hours = float(total_till_hours - total_from_hours) / 60
        elif self.end_day == 'next_day':
            self.total_hours = 24 - (float(total_from_hours - total_till_hours) / 60)

    @api.multi
    def trigger_allocate(self):
        self.trigger_calculate()
        self.write({'progress': 'confirmed'})
