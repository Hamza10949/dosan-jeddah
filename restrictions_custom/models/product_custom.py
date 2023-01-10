from odoo import models, fields, api
from odoo.exceptions import UserError


class prod_cat(models.Model):
    _inherit = "product.category"
    product_code = fields.Char(string='Product Code')

    @api.onchange('parent_id')
    def check_brand(self):
        check_product_cat = self.env['product.category'].search(
            [('name', '=', self.parent_id.name)])

        if self.parent_id:
            self.product_code = check_product_cat.product_code

        else:
            self.product_code = ''
