from odoo import models, fields, api
from odoo.exceptions import UserError


class Inherit_PurchaseReq(models.Model):
    _inherit = "purchase.requisition.line"
    contractor = fields.Many2one(
        'res.partner', string="Contractor", domain="[('category_id', '=', 6)]")
