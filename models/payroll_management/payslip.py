# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Payslip

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]
PAY_TYPE = [('allowance', 'Allowance'), ('deduction', 'Deduction')]


class Payslip(surya.Sarpam):
    _name = "pay.slip"
    _inherit = "mail.thread"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", readonly=True)
    payslip_details = fields.One2many(comodel_name="payslip.detail",
                                      inverse_name="payslip_id",
                                      string="Pay Slip Details")
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    _sql_constraints = [('payslip_uniq', 'unique(employee_id, month_id)', 'Payslip is already generated')]

    @api.multi
    def generate_payslip(self):
        self.payslip_details.unlink()
        pay = self.update_payslip_dict()

        hr_pay = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])
        recs = hr_pay.structure_id.detail_ids
        sorted(recs, key=lambda x: x.sequence)

        for rec in recs:
            if rec.is_need:
                data = {"code": rec.rule_id.code.id,
                        "amount": pay[rec.rule_id.code.name],
                        "payslip_id": self.id,
                        "pay_order": rec.sequence,
                        "pay_type": rec.pay_type}
                self.env["payslip.detail"].create(data)

        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        self.write({"progress": self.progress, "writter": writter.id})

    @api.multi
    def update_payslip_dict(self):
        hr_pay = self.env["hr.pay"].search([("employee_id", "=", self.employee_id.id)])
        recs = hr_pay.structure_id.detail_ids
        sorted(recs, key=lambda x: x.sequence)

        pay = {"BASIC": hr_pay.basic}

        for rec in recs:
            if rec.rule_id.rule_type == "fixed":
                pay[rec.rule_id.code.name] = rec.rule_id.fixed

            elif rec.rule_id.rule_type == "formula":
                pay[rec.rule_id.code.name] = eval(rec.rule_id.formula, pay)

            elif rec.rule_id.rule_type == "slab":
                for record in rec.rule_id.slab_ids:
                    if record.range_till >= eval(record.rule_id.slab_input, pay) >= record.range_from:
                        if record.slab_output == "fixed":
                            pay[rec.rule_id.code.name] = record.fixed
                        elif record.slab_output == "formula":
                            pay[rec.rule_id.code.name] = eval(record.formula, pay)
                        else:
                            pay[rec.rule_id.code.name] = 0
                    else:
                        pay[rec.rule_id.code.name] = 0
        return pay


class PayslipDetail(surya.Sarpam):
    _name = "payslip.detail"

    code = fields.Many2one(comodel_name="salary.rule.code", string="Code", readonly=True)
    amount = fields.Float(string="Amount", readonly=True)
    pay_order = fields.Integer(string="Pay Order", readonly=True)
    pay_type = fields.Selection(PAY_TYPE, string='Pay Type', readonly=True)
    payslip_id = fields.Many2one(comodel_name="pay.slip", string="payslip")

    _sql_constraints = [('salary_details_uniq', 'unique(code, payslip_id)', 'Salary details should not duplicated')]



