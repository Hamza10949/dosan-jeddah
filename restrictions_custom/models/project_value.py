from odoo.exceptions import UserError
from odoo import models, fields, api, exceptions


class Inherit_PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    compute_project_value = fields.Monetary(
        string="Project Value Recieved", compute="_compute_total")

    def _compute_total(self):
        for record in self:
            for line in record.order_line:
                project_id = line.account_analytic_id.project_ids.id
                po_project = self.env['project.project'].search(
                    [('id', '=', project_id)])
                if po_project.proj_value and po_project.Received_Client_Payment != 0:
                    record.compute_project_value = (
                        po_project.proj_value)-(po_project.Received_Client_Payment)
                else:
                    record.compute_project_value = 0


class Invisible_field(models.Model):
    _inherit = "purchase.order"
    po_bill_state = fields.Char(string="Bill state", compute="po_billstate")

    def po_billstate(self):

        for records in self:
            if records.invoice_ids:
                vendor_bill = records.invoice_ids
                for inv in vendor_bill:
                    records.po_bill_state = inv.payment_state
            else:
                records.po_bill_state = 'no vendor bill'


class Project_field(models.Model):
    _inherit = "purchase.requisition"

    project_lv = fields.Char(string="Project")

    # @api.onchange('line_ids')
    # def _student_onchange(self):
    #     for rec in self.line_ids:
    #         PRL = self.env['account.analytic.account'].search(
    #             [('id', '=', rec.account_analytic_id.id)])
    #         self.project_lv = PRL.name
    #         break

    # if self.line_ids:
    #     for i in self.line_ids:
    #         #rec.project_lv = i.account_analytic_id.name
    #         PRL = self.env['account.analytic.account'].search(
    #             [('id', '=', i.account_analytic_id.id)])
    #         self.project_lv = PRL.name
    #         #raise UserError(PRL.name)
