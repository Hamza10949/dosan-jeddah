from odoo import models, fields, api
from odoo.exceptions import UserError


class inventory_fields(models.Model):
    _inherit = "stock.move"

    product_onhand_inv = fields.Char(
        string="On Hand qty ", compute="_get_qty_available")

    @api.depends('product_id')
    def _get_qty_available(self):
        qty_line_obj = self.env['product.template']
        for rec in self:
            qty_available_obj = qty_line_obj.search(
                [['name', '=', rec.product_id.name]])

            rec.product_onhand_inv = qty_available_obj.qty_available
