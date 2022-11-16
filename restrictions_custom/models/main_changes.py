from odoo import models, fields, api
from odoo.exceptions import UserError


class po_fields(models.Model):
    _inherit = "purchase.requisition.line"

    product_code = fields.Char(
        string="Product Code ", related='product_id.default_code')

    product_onhand = fields.Char(
        string="On hand qty ", compute="_get_qty_available")

    @api.depends('product_id')
    def _get_qty_available(self):
        qty_line_obj = self.env['product.template']
        for rec in self:
            qty_available_obj = qty_line_obj.search(
                [['name', '=', rec.product_id.name]])

            rec.product_onhand = qty_available_obj.qty_available


class product_selection(models.Model):
    _inherit = "product.product"

    def name_get(self):

        result = []
        for rec in self:
            result.append((rec.id, rec.name))
        return result

    # def po_product(self):
    #     name_prod=self.display_name
    #     name_prod.split


class proj_cus(models.Model):
    _inherit = "project.project"
    proj_value = fields.Monetary(string="Project Value")
    proj_loc = fields.Char(string="Project location")
    Received_Client_Payment = fields.Monetary(
        string="Received Client Payment ")
