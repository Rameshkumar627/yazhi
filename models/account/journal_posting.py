# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class JournalType(surya.Sarpam):
    _name = "journal.posting"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    type_details = fields.One2many(comodel_name="journey.type.detail",
                                   inverse_name="type_id",
                                   string="Journal Type Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress")


class JournalTypeDetail(surya.Sarpam):
    _name = "journey.type.detail"

    name = fields.Many2one(comodel_name="account.account", string="Account", required=True)
    type_id = fields.Many2one(comodel_name="journal.type", string="Journal Type")
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress", related="type_id.progress")
