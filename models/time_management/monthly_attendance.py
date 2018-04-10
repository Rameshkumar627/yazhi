# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
from lxml import etree


# Week Schedule

PROGRESS_INFO = [('draft', 'draft'), ('closed', 'Closed')]


class MonthAttendance(surya.Sarpam):
    _name = "month.attendance"

    period_id = fields.Many2one(comodel_name="period.period", string="Month")
    month_detail = fields.One2many(comodel_name="time.attendance",
                                   inverse_name="month_id",
                                   string="Month Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MonthAttendance, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//iframe"):
            node.set('src', "https://erp.vvsuagrs.com")
        res['arch'] = etree.tostring(doc)
        return res


