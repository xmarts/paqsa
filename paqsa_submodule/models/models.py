# -*- coding: utf-8 -*-
from odoo import models, fields, api
class SaleOrderLine(models.Model):
  _inherit = 'sale.order.line'
    
  #Delivery_percentage = fields.Float()
   
#  @api.onchange('partner_id')
 # def onchange_partner_id(self):  
  #  for product_id in self:
   #     self.update({
    #        'partner_invoice_id': False,
     #       'partner_shipping_id': False,
      #      'fiscal_position_id': False,
       # })
       #return {}
   # value = {'payment_method_id': self.partner_id.l10n_mx_edi_paymen_method_id and self.partner_id.l10n_mx_edi_paymen_method_id.id or False}
    #self.update(value)

            