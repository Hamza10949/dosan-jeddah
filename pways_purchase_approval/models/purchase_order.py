# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Purchase Approval"

    state = fields.Selection(selection_add=[('wait_approval', 'Waiting For Approval'),
                                            ('approval', 'Approval'),
                                            ('rejected', 'Rejected'),
                                            ('partial_approve', 'Partial Approved')])
    has_approval = fields.Boolean(compute="_compute_has_approval")

    purchase_history_ids = fields.One2many(
        'purchase.approval.history', 'purchase_id', string="Purchase History", readonly=True)
    reject_reason = fields.Text(string="Reject Reason", copy=False)
    purchase_approval = fields.Boolean(compute="_compute_purchase_approval")
    # custom field
    po_type = fields.Selection(
        [('service', 'Service'), ('material', 'Material'), ('rent', 'Rent')], 'Type')

    def _compute_purchase_approval(self):
        for purchase in self:

            approval_lines = self.env['purchase.approval.lines'].search([
                ('limit', '<=', purchase.amount_total),
            ])
            if purchase.purchase_history_ids and all([line.status == ('approve') for line in purchase.purchase_history_ids]):
                purchase.purchase_approval = False
            elif approval_lines:
                purchase.purchase_approval = True
            else:
                purchase.purchase_approval = False
            # custom work
            approval_vendor_line = self.env['purchase.approval'].search([
                ("custom_vendor", '=', purchase.partner_id.name)
            ])
            if approval_vendor_line:
                purchase.purchase_approval = True
            else:
                purchase.purchase_approval = True

            approval_vendor_line = self.env['purchase.approval'].search([
                ("new_po_type", '=', purchase.po_type)
            ])
            if approval_vendor_line:
                purchase.purchase_approval = True
            else:
                purchase.purchase_approval = True

    def _compute_has_approval(self):
        for purchase in self:
            approval_sequence = self.env.company.sequence_approval
            if approval_sequence:
                user_id = self.env['res.users']

                approval_id = purchase.purchase_history_ids.filtered(
                    lambda x: x.status == 'pending')
                if approval_id:
                    user_id = approval_id.mapped('user_id')[0]
                is_rejected = any(
                    [status == 'reject' for status in purchase.purchase_history_ids.mapped('status')])
                if is_rejected:
                    purchase.write({'state': 'rejected'})
                if not is_rejected and (purchase.state == 'wait_approval' or purchase.state == 'partial_approve' ) and user_id and user_id.id == self.env.user.id:

                    purchase.has_approval = True
                else:
                    purchase.has_approval = False
            else:

                approval_id = purchase.purchase_history_ids.filtered(
                    lambda x: x.status == 'pending' and x.user_id.id == self.env.user.id)
                is_rejected = any(
                    [status == 'reject' for status in purchase.purchase_history_ids.mapped('status')])

                if not is_rejected and (purchase.state == 'wait_approval' or purchase.state == 'partial_approve' ) and approval_id and approval_id.status == 'pending':
                    purchase.has_approval = True
                else:
                    purchase.has_approval = False

    def action_approval(self):

        pending_approval = self.purchase_history_ids.filtered(
            lambda x: x.user_id.id == self.env.user.id and x.status == 'pending')
        pending_approval.write(
            {'status': 'approve', 'date_done': datetime.now()})

        if self.purchase_history_ids and all([line.status == 'approve' for line in self.purchase_history_ids]):
            self.write({'state': 'approval'})
        elif self.purchase_history_ids and [line.status == 'approve' for line in self.purchase_history_ids]:
            self.write({'state': 'partial_approve'})
        
       

    def too_approve(self):

        data = [(5, 0, 0)]
        # approval_lines = self.env['purchase.approval.lines'].search([
        #     ('limit', '<=', self.amount_total),
        #     ('approval_id.document_type', '=', 'purchase'),
        # ])
        approval = self.env['purchase.approval'].search(
            ["|",('custom_vendor', '=', self.partner_id.id),
             ('document_type', '=', 'purchase'), ("new_po_type", '=', self.po_type)])
        if not approval:
            approval = self.env['purchase.approval'].search(
                [('custom_vendor', '=', False),
                 ("new_po_type", '=', False),
                 ('document_type', '=', 'purchase')])
        # raise UserError(approval)
        for ai in approval:
            approval_lines = self.env['purchase.approval.lines'].search([
                ('limit', '<=', self.amount_total), ('approval_id', '=', ai.id)
                # ('approval_id.document_type', '=', 'purchase'),
            ])
            # raise UserError(approval_lines)
            if approval_lines:
                for line in approval_lines:
                    data.append((0, 0, {'user_id': line.user_id.id}))
                self.purchase_history_ids = data
                self.write({'state': 'wait_approval'})
            else:
                self.write({'state': 'approval'})

        # if not approval:
        #     approval2 = self.env['purchase.approval'].search(
        #         [('custom_vendor', '=', '')])
        #     for ai in approval2:
        #         approval_lines2 = self.env['purchase.approval.lines'].search([
        #             ('limit', '<=', self.amount_total), ('approval_id', '=', ai.id)
        #             ('approval_id.document_type', '=', 'purchase'), ])

        #         if approval_lines2:
        #             for line in approval_lines2:
        #                 data.append((0, 0, {'user_id': line.user_id.id}))
        #             self.purchase_history_ids = data
        #             self.write({'state': 'wait_approval'})
        #         else:
        #             self.write({'state': 'approval'})

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'approval']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True


class PurchaseApprovalsHistory(models.Model):
    _name = "purchase.approval.history"
    _description = "Approval History"

    purchase_id = fields.Many2one('purchase.order', string="Purchase Request")
    user_id = fields.Many2one('res.users', string="Approver")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approve', 'Approved'),

        ('reject', 'Rejected')], default='pending', copy=False, string="Status")
    date_done = fields.Datetime(string="Date")


class SiteRequest(models.Model):
    _inherit = "purchase.requisition"
    po_type_site = fields.Selection(
        [('service', 'Service'), ('material', 'Material'),('rent', 'Rent') ], 'Type')
