# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


# Tax
class TaxConfiguration(surya.Sarpam):
    _name = "tax.configuration"

    name = fields.Char(string="Name", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    tax_id = fields.Many2one(comodel_name="res.tax", string="Tax")
