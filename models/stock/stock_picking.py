# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
PICKING_TYPE = [("in", "IN"), ("internal", "Internal"), ("out", "OUT")]


# Stock Picking
class StockPicking(surya.Sarpam):
    _name = "stock.picking"

    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference", readonly=True)
    date = fields.Date(string="Date", required=True)
    picking_type = fields.Selection(selection=PICKING_TYPE, string="Picking Type", required=True)
    source_location_id = fields.Many2one(comodel_name="stock.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="stock.location",
                                              string="Destination location",
                                              required=True)
    picking_detail = fields.One2many(comodel_name="stock.move",
                                     inverse_name="picking_id",
                                     string="Stock Move")
    progress = fields.Selection(selection=PICKING_TYPE, string="Progress")
