from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


                        
   
class CustomModel(models.Model):
 _inherit = "account.analytic.account"


 @api.model_create_multi
 def create(self, vals_list):
    for vals in vals_list:
        if vals['name']:
            exists=self.env["account.analytic.account"].search([("name",'=',vals['name'])])
            if exists:
                raise UserError("Duplication : Project with this name already exists!")
            else:
                res= super(CustomModel, self).create(vals_list)
                return res
   
    # raise UserError(str(vals_list))

