import qrcode
import base64

from io import BytesIO

from odoo import models, fields, _
from odoo.exceptions import UserError


class AssetQrGenerator(models.Model):
    _inherit = 'account.asset'

    qr_code = fields.Binary("QR Code")
    img = fields.Binary("Image")

    def generate_asset_qr(self):
        if self.name:
            if self.id:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                qr.add_data(self.name)
                qr.add_data('\n')
                qr.add_data(self.id)
                qr.make(fit=True)
                img = qr.make_image()
                tmp = BytesIO()
                img.save(tmp, format="PNG")
                qr_img = base64.b64encode(tmp.getvalue())
                self.qr_code = qr_img
            else:
                raise UserError(
                    _('Check if Employee Name and Job title empty'))
