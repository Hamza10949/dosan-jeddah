from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class Inherit_PurchaseOrder_rfq(models.Model):
    _inherit = "purchase.order"
    project_slv=fields.Char(string="Project",compute="_purchase_order_project")

    def _purchase_order_project(self):
        self.project_slv=''
        for rec in self:
            if rec.requisition_id:
                project= rec.requisition_id.line_ids
                if project:
                    for lines in project:
                    rec["project_slv"]=lines.account_analytic_id.name
                        
    



class Inherit_PurchaseReq(models.Model):
    _inherit = "purchase.requisition.line"
    contractor = fields.Many2one(
        'res.partner', string="Contractor", domain="[('category_id', '=', 6)]")


class Inherit_PurchaseRequi(models.Model):
    _inherit = "purchase.requisition"
    project_lv = fields.Char(string="Project")
    project_plv = fields.Char(string="Project",compute="_site_req_project")
    
    



    def _site_req_project(self):
        self.project_plv=''
        for rec in self:
            if rec.line_ids:
                project= rec.line_ids
                for lines in project:
                    rec["project_plv"]=lines.account_analytic_id.name
                    
            


    def create_aljazira_rfq(self):
        aljazira = self.env['res.partner'].search([('id', "=", 15)])
        for record in self:
            if record.vendor_id == aljazira and record.order_count == 0:

                new_rfq = self.env['purchase.order'].create({
                    'state': 'draft',
                    'requisition_id': self.id,
                    'partner_id': self.vendor_id.id,
                    'currency_id': self.currency_id.id,
                    'date_planned': datetime.today(),
                    'date_order': datetime.today(),
                    'po_type': self.po_type_site,



                })
                for mov_id in self.line_ids:
                    rfq_lines = self.env['purchase.order.line'].create({
                        'order_id': new_rfq.id,
                        'product_id': mov_id.product_id.id,
                        'product_onhand_po': mov_id.product_onhand,
                        'product_code_po': mov_id.product_code,
                        'name': mov_id.product_id.name,
                        'product_qty': mov_id.product_qty,
                        'price_unit': mov_id.product_id.lst_price,
                        'account_analytic_id': mov_id.account_analytic_id.id,
                        'date_planned': datetime.today(),
                        'price_subtotal': mov_id.product_qty*mov_id.price_unit,


                    })
