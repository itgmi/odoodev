# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models,api
from datetime import date


class SaleOrderPricelistWizard(models.Model):
    _name = 'sale.order.pricelist.wizard'
    _description = 'Pricelist Wizard'
    
    bi_wizard_pricelist_id = fields.Many2one('product.pricelist',string="Pricelist")
    pricelist_line = fields.One2many('sale.order.pricelist.wizard.line','pricelist_id',string='PricelistLine Id')
    
    @api.model
    def default_get(self, fields):
        res = super(SaleOrderPricelistWizard, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        if res_ids[0]:
            so_line = res_ids[0]
            so_line_obj = self.env['sale.order.line'].browse(so_line)
            categ_id = so_line_obj.product_id.categ_id.id
            pricelist_list = []
            pricelists_items = self.env['product.pricelist.item'].sudo().search([
                ('categ_id', '=', categ_id)])
            lists = []
            for rec in pricelists_items:
                if rec.pricelist_id.id not in lists:
                    lists.append(rec.pricelist_id.id)
            pricelists = self.env['product.pricelist'].sudo().browse(lists)
            if pricelists:
                for pricelist in pricelists:
                    price_unit =pricelist._compute_price_rule(so_line_obj.product_id, so_line_obj.product_uom_qty, date=date.today(), uom_id=so_line_obj.product_uom.id)[so_line_obj.product_id.id][0]
                    margin = price_unit - so_line_obj.product_id.standard_price
                    if price_unit != 0.0:
                        margin_per = (100 * (price_unit - so_line_obj.product_id.standard_price))/price_unit
                             
                        wz_line_id = self.env['sale.order.pricelist.wizard.line'].create({'bi_pricelist_id' :pricelist.id,
                                                                                       'bi_unit_price':price_unit,
                                                                                       'bi_unit_measure':so_line_obj.product_uom.id,
                                                                                       'bi_unit_cost':so_line_obj.product_id.standard_price,
                                                                                       'bi_margin':margin,
                                                                                       'bi_margin_per':margin_per,
                                                                                       'line_id': so_line,})
                         
                        pricelist_list.append(wz_line_id.id)
            res.update({
                
                'pricelist_line':[(6,0,pricelist_list)],
            })
        return res
        
        
        
class SaleOrderPricelistWizardLine(models.Model):
    _name = 'sale.order.pricelist.wizard.line'
    _description = 'Pricelist Wizard'
    
    pricelist_id = fields.Many2one('sale.order.pricelist.wizard',"Pricelist Id")
    bi_pricelist_id = fields.Many2one('product.pricelist',"Pricelist",required=True)
    bi_unit_measure = fields.Many2one('uom.uom','Unit')
    bi_unit_price = fields.Float('Unit Price')
    bi_unit_cost = fields.Float('Unit Cost')
    bi_margin = fields.Float('Margin')
    bi_margin_per = fields.Float('Margin %')
    line_id =fields.Many2one('sale.order.line')
      
    def update_sale_line_unit_price(self):
        if self.line_id:
            self.line_id.write({'price_unit':self.bi_unit_price})
        
              