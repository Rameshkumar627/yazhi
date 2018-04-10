# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock Move
class StockMove(surya.Sarpam):
    _name = "stock.Move"

    name = fields.Char(string="Name", required=True)
    reference = fields.Char(string="Reference", readonly=True)
    date = fields.Date(string="Date")
    back_order_id = fields.Many2one(comodel_name="stock.picking", string="Back Order")
    source_location_id = fields.Many2one(comodel_name="stock.location",
                                         string="Source Location",
                                         required=True)
    destination_location_id = fields.Many2one(comodel_name="stock.location",
                                              string="Destination location",
                                              required=True)
