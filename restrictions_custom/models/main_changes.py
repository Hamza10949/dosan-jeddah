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


class po_fields_invoice_lines(models.Model):
    _inherit = "purchase.order.line"

    product_code_po = fields.Char(
        string="Product Code ", related='product_id.default_code')

    product_onhand_po = fields.Char(
        string="On hand qty ", compute="_get_qty_available")

    @api.depends('product_id')
    def _get_qty_available(self):
        qty_line_obj = self.env['product.template']
        for rec in self:
            qty_available_obj = qty_line_obj.search(
                [['name', '=', rec.product_id.name]])

            rec.product_onhand_po = qty_available_obj.qty_available


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


class payment_register(models.TransientModel):
    _inherit = "account.payment.register"
    percentage = fields.Monetary(string="percentage %")

    @api.onchange('percentage')
    def _onchange_field_name(self):
        check_bill_amount = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('name', '=', self.communication)])

        check_vendor_bill_amount = self.env['account.move'].search(
            [('move_type', '=', 'in_invoice'), ('name', '=', self.communication)])

        if check_bill_amount:
            amnt = check_bill_amount.amount_residual
            #raise UserError(amnt)
            if self.percentage > 0:
                amount_per = 0
                amount_per = (self.percentage/100) * amnt
                #self.write({'amount': amount_per})
                self.amount = amount_per
            else:
                self.amount = amnt

        @api.model
        def _create_payments(self):

            payments = super(payment_register, self)._create_payments()

            for payment in payments:
                payment.percentage = self.percentage
            # payment.amount = (payment.percentage/payment.amount)*100
            return payments

        if check_vendor_bill_amount:
            amnt = check_vendor_bill_amount.amount_residual
            #raise UserError(amnt)
            if self.percentage > 0:
                amount_per = 0
                amount_per = (self.percentage/100) * amnt
                #self.write({'amount': amount_per})
                self.amount = amount_per
            else:
                self.amount = amnt

        @api.model
        def _create_payments(self):

            payments = super(payment_register, self)._create_payments()

            for payment in payments:
                payment.percentage = self.percentage
            # payment.amount = (payment.percentage/payment.amount)*100
            return payments

    # @api.onchange('percentage')
    # def _onchange_field_name(self):
    #     check_bill_amount = self.env['account.move'].search(
    #         [('move_type', '=', 'out_invoice'), ('name', '=', self.communication)])
    #     amnt = check_bill_amount.amount_residual

    #     if self.percentage:
    #         amount_per = 0
    #         amount_per = (self.percentage/100)*amnt
    #         #self.write({'amount': amount_per})
    #         self.amount = amount_per
    #     else:
    #         self.amount = amnt

    # @api.model
    # def _create_payments(self):

    #     payments = super(payment_register, self)._create_payments()

    #     for payment in payments:
    #         payment.percentage = self.percentage
    #        # payment.amount = (payment.percentage/payment.amount)*100
    #     return payments


class extpayment(models.Model):
    _inherit = "account.payment"
    percentage = fields.Monetary(string='Percentage %')

    @api.onchange('percentage')
    def _onchange_field_name(self):
        check_po_amount = self.env['purchase.order'].search(
            [('name', '=', self.ref)])
        amnt = check_po_amount.amount_total

        #raise UserError(amnt)
        if self.percentage > 0:
            amount_per = 0
            amount_per = (self.percentage/100) * amnt
            #self.write({'amount': amount_per})
            self.amount = amount_per
        else:
            self.amount = amnt
