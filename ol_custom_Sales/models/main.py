from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class sale_custom_fields(models.Model):
    _inherit = "sale.order"
    Client_approval_date = fields.Date(string='Client approval date')
    Project_Start_Date = fields.Date(string='Project Start Date')
    Project_Completion_Date = fields.Date(string='Project Completion Date')
