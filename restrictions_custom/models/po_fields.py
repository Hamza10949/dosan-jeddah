from odoo import models, fields, api
from odoo.exceptions import UserError


class po_fields_value(models.Model):
    _inherit = "purchase.order"

    total_amnt_rem = fields.Monetary(
        compute="_total_proj_val_remaining", string="amount remaining ")

    def _total_proj_val_remaining(self):

        # if self.order_line:
        #     if self.order_line.account_analytic_id:
        #         for i in self.order_line:

        #             self.total_amnt_rem = ((i.account_analytic_id.proj_val) -
        #                                    (i.account_analytic_id.Received_Client_Payment))
        self.total_amnt_rem = 34344
