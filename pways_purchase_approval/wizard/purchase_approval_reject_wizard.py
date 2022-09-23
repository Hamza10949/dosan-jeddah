# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class PurchaseRejectReasonWizard(models.TransientModel):
    _name = "purchase.reject.reason.wizard"
    _description = "Reject Reason Wizard"

   # reject_reason = fields.Text(string="Reject Reason")
    reject_reason = fields.Text(string="Type Rejection Reason")
    reject_reason_sel = fields.Selection(
        [('expensive', 'Expensive'), ('material', 'Material quality is not good'), ], 'Choose a Reason')

    @api.onchange('reject_reason_sel')
    def set_reject_reason(self):
        code = self._fields['reject_reason_sel'].selection
        code_dict = dict(code)
        name = code_dict.get(self.reject_reason_sel)
        self.reject_reason = name

    def action_reject(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env[active_model].browse(
            self.env.context.get('active_id'))
        history_ids = self.env['purchase.approval.history'].search(
            [('status', '=', 'pending'), ('purchase_id', '=', active_id.id), ('user_id', '=', self.env.user.id)])
        history_ids.write({'status': 'reject', 'date_done': datetime.now()})
        active_id.write({'reject_reason': self.reject_reason})
