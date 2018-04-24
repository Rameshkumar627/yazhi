# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Salary Structure

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


class SalaryStructure(surya.Sarpam):
    _name = "salary.structure"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    detail_ids = fields.One2many(comodel_name="salary.structure.detail",
                                 inverse_name="structure_id",
                                 string="Salary Structure Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')


class SalaryStructureDetail(surya.Sarpam):
    _name = "salary.structure.detail"

    rule_id = fields.Many2one(comodel_name="salary.rule", string="Salary Rule")
    sequence = fields.Integer(string="Sequence")
    is_need = fields.Boolean(string="Is Need")
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='structure_id.progress')
