#-*- coding: utf-8 -*-
from odoo import models, fields, api

class partner(models.Model):
    _inherit = "res.partner"
 
    l10n_mx_edi_payment_method_id = fields.Many2one(
        'l10n_mx_edi.payment.method',
        string='Payment Way',
        help='Indicates the way the payment was/will be received, where the '
        'options could be: Cash, Nominal Check, Credit Card, etc.')
     
    @api.onchange('partner_id')
    def onchange_partner_id(self):  
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return {}
        value = { 'payment_method_id': self.partner_id.l10n_mx_edi_paymen_method_id and self.partner_id.l10n_mx_edi_paymen_method_id.id or False}
        self.update(value)

