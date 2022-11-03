from odoo import models, fields, api
from odoo.exceptions import UserError


class po_fields(models.Model):
    _inherit = "purchase.requisition.line"

    product_code = fields.Char(
        string="Product Code ", related='product_id.default_code')


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
