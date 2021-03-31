#-*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    delivery_percentage = fields.Many2one("porcentaje de entrega",compute="_deliveri_p")
    
    invoice_percentage = fields.Many2one("porcentage pagado",Compute="_invoice_p")

    @api.depends("order_line")
    def _deliveri_p(self):
        self.delivery_percentage= 0    
        for rec in self.order_line:
            self.delivery_percentage += abs(rec.qty_delivered / rec.product_uom_qty )*100
    
    
    @api.depends("order_line")
    def _invoice_p(self):
        self.invoice_percentage= 0    
        for rec in self.order_line:
            total_Quantity += (rec.qty_invoice)
            if total_Quantity:
                self.invoice_percentage = (rec.total_Quantity / rec.amount_total)*100
    
    