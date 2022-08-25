# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class PurchaseRejectReasonWizard(models.TransientModel):
    _name = "purchase.reject.reason.wizard"
    _description = "Reject Reason Wizard"

    reject_reason = fields.Text(string="Reject Reason")

    def action_reject(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env[active_model].browse(self.env.context.get('active_id'))
        history_ids = self.env['purchase.approval.history'].search([('status', '=', 'pending'), ('purchase_id', '=', active_id.id), ('user_id', '=', self.env.user.id)])
        history_ids.write({'status': 'reject', 'date_done': datetime.now()})
        active_id.write({'reject_reason': self.reject_reason})
