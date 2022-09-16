# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # picking_ids = fields.Many2many('account.payment', compute='_compute_payment_count', string='Payments')
    cout_payment = fields.Integer(compute='_compute_payment_count')

    @api.depends('partner_id')
    def _compute_payment_count(self):
        totalpay = self.env['account.payment'].search([('ref', '=', self.name)])
        self.cout_payment=len(totalpay)
        # for rec in self:
        #     payment = self.env['account.payment'].search([('ref', '=', rec.name)])
        #     if payment:
        #         for pay in payment:
        #             rec.picking_ids = [(4,pay.id)]
        #         totalpay = self.env['account.payment'].search([('ref', '=', rec.name)])
        #         rec.cout_payment=len(totalpay)
        #     else:
        #         rec.cout_payment = 0
        #         rec.picking_ids = False
    
    def action_bill(self):
        return {
            'name': _('New Form'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'view_id': self.env.ref('account.view_account_payment_form').id,            
            'type': 'ir.actions.act_window',
            'context': {'default_partner_id': self.partner_id.id,
                        'default_partner_type': 'supplier',
                        'default_ref':self.name,
                        'default_payment_type':'outbound',
                        'default_amount':self.amount_total}
        }

    def action_payments(self):
        
        action = self.env.ref('account.action_account_payments_payable')
        
        result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'binding_view_types': action.binding_view_types,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
            'domain':[('ref','=',self.name)]

		}
        return result





        # return {
        #     # 'domain': [('ref', 'in', self.name)],
        #     'name': _('New Form'),
        #     'view_type': 'tree',
        #     'view_mode': 'tree',
        #     'res_model': 'account.payment',
        #     'view_id': self.env.ref('account.view_account_supplier_payment_tree').id, 
        #     'type': 'ir.actions.act_window'
        # }

class CreateInvoice(models.Model):
    _name='purchase.down'
    name = fields.Char(string="Name")
    # @api.multi
    # def action_bill(self):
    #     raise UserError("Ata he")
        # self.write({'state': 'in_payment'})
        # '''return {
        #     #'name': self.order_id,
        #     'res_model': 'pickabite.payment',
        #     'type': 'ir.actions.act_window',
        #     'context': {},
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'view_id': self.env.ref("pickabite.payment_form_view"),
        #     'target': 'new'
        # } '''
