#-*- coding: utf-8 -*-
from odoo import models, fields, api
from ast import literal_eval
from datetime import date
from operator import itemgetter
import time
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES

class StockPicking(models.Model):
    _inherit = "stock.picking"

    total_sum = fields.One2many(
        'sum.product',
        'picking_id',
        string='Categories',
        readonly=True
    )
    
    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        res.get_sum()
        return res

    def get_sum(self):
        for rec in self:
            params = dict()
            for move in rec.move_ids_without_package:
                product = move.product.idproduct_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
                if product:
                    if product in params:
                        params[product]['quantity'] += move.quantity
                    else:
                        params[product]['quantity'] = move.quantity
            for element in params:
                self.env['sum.product'].create(
                {   
                    'product' : element,
                    'total_weight_per_uom': params[element]['quantity'],
                    'picking_id': rec.id
                    
                }
            )
    
    

    show_check_availability = fields.Boolean(,
        help='Technical field used to compute whether the check availability button should be shown.')
    
    immediate_transfer = fields.Boolean(False)


    def action_assign(self):
        """ Check availability of picking moves.
        This has the effect of changing the state and reserve quants on available moves, and may
        also impact the state of the picking as it is computed based on move's states.
        @return: True
        """
        self.filtered(lambda picking: picking.state == 'draft').action_confirm()
        moves = self.mapped('move_lines').filtered(lambda move: move.state not in ('draft', 'cancel', 'done'))
        if not moves:
            raise UserError(_('Nothing to check the availability for.'))
        # If a package level is done when confirmed its location can be different than where it will be reserved.
        # So we remove the move lines created when confirmed to set quantity done to the new reserved ones.
        package_level_done = self.mapped('package_level_ids').filtered(lambda pl: pl.is_done and pl.state == 'confirmed')
        package_level_done.write({'is_done': False})
        moves._action_assign()
        package_level_done.write({'is_done': True})
        return True