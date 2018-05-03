# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Salary Structure

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]
PAY_TYPE = [('allowance', 'Allowance'), ('deduction', 'Deduction')]


class SalaryStructure(surya.Sarpam):
    _name = "salary.structure"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    detail_ids = fields.One2many(comodel_name="salary.structure.detail",
                                 inverse_name="structure_id",
                                 string="Salary Structure Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Many2one(comodel_name="hr.employee", string="User", track_visibility='always')

    @api.multi
    def trigger_confirm(self):
        if not self.detail_ids:
            raise exceptions.ValidationError("Error! Salary Rules Not found")

        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])

        self.write({"progress": "confirmed", "writter": writter.id})

    _sql_constraints = [('rule_uniq', 'unique(rule_id, structure_id)', 'Error! In Salary Details..')]


class SalaryStructureDetail(surya.Sarpam):
    _name = "salary.structure.detail"

    rule_id = fields.Many2one(comodel_name="salary.rule", string="Salary Rule", required=True)
    code = fields.Many2one(comodel_name="salary.rule.code", string="Code", related="rule_id.code")
    sequence = fields.Integer(string="Sequence")
    is_need = fields.Boolean(string="Is Need")
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure", required=True)
    pay_type = fields.Selection(PAY_TYPE, string='Pay Type', required=True)
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='structure_id.progress')

    _sql_constraints = [('rule_uniq', 'unique(rule_id, structure_id)', 'Salary Structure should not duplicated')]
