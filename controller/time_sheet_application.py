# -*- coding: utf-8 -*-

from odoo.http import Controller, route, request
from odoo.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect


class TimeSheetApplication(Controller):
    @route('/yazhi/time_sheet_application', type="http", auth='none')
    def application_time_sheet(self):
        return "Ramesh"
