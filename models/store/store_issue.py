# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"),
                 ("issued", "Issued")]


class StoreIssue(surya.Sarpam):
    _name = "store.issue"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    request_id = fields.Many2one(comodel_name="store.request", string="Store Request", readonly=True)
    issued_by = fields.Many2one(comodel_name="hr.employee", string="Approved By", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    issue_detail = fields.One2many(comodel_name="store.issue.detail",
                                   inverse_name="issue_id",
                                   string="Issue Detail")
    writter = fields.Text(string="Writter", track_visibility='always')

    _sql_constraints = [('unique_issue', 'unique (request_id)',
                         'Error! Issue is already done')]

    @api.multi
    def check_quantity(self):
        recs = self.issue_detail

        issued_quantity = 0
        for rec in recs:
            issued_quantity = issued_quantity + rec.issued_quantity

        if issued_quantity <= 0:
            raise exceptions.ValidationError("Error! No Products Found")

    @api.multi
    def generate_stock_picking(self):
        pass

    @api.multi
    def trigger_issue(self):
        self.check_quantity()

        issued_by = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        writter = "Issued by {0} on {1}".format(issued_by.name,
                                                datetime.now().strftime("%d-%m-%Y %H:%M"))

        self.generate_stock_picking()

        self.write({"progress": "confirmed",
                    "issued_by": issued_by.id,
                    "writter": writter})


class StoreIssueDetail(surya.Sarpam):
    _name = "store.issue.detail"

    product_id = fields.Many2one(comodel_name="product.product", string="Product", readonly=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Requested Quantity", readonly=True)
    issued_quantity = fields.Float(string="Issued Quantity")
    issue_id = fields.Many2one(comodel_name="store.issue", string="Store Issue")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="issue_id.progress")

    _sql_constraints = [('unique_issue_detail', 'unique (product_id, issue_id)',
                         'Error! Product should not be repeated')]