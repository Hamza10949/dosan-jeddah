# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sequence_approval = fields.Boolean(related="company_id.sequence_approval", string="Sequence Wise Approval", readonly=False)

class ResCompany(models.Model):
    _inherit = 'res.company'

    sequence_approval = fields.Boolean(string="Sequence Wise Approval")
