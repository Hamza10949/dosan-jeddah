# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PurchaseApproval(models.Model):
    _name = "project.type.custom"

    proj_type_name = fields.Char(string="Project Type")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.proj_type_name))
        return result
