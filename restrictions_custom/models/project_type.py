# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PurchaseApproval(models.Model):
    _name = "project.type.custom"

    proj_type_name = fields.Char(string="Project Type")
