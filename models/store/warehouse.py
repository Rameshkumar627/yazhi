# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class HospitalWarehouse(surya.Sarpam):
    _name = "hospital.warehouse"
    _rec_name = "location_id"

    product_id = fields.Many2one(comodel_name="hospital.product", string="Product")
    location_id = fields.Many2one(comodel_name="hospital.location", string="Location")
    quantity = fields.Float(string="Quantity")
    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")
