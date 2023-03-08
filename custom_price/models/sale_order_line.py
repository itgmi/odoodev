from odoo import models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_base_price(self, product, quantity, uom, date, target_currency):
        """ Compute the base price for a given rule

        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param target_currency: pricelist currency

        :returns: base price, expressed in provided pricelist currency
        :rtype: float
        """
        target_currency.ensure_one()

        rule_base = self.base or 'list_price'
        if rule_base == 'pricelist' and self.base_pricelist_id:
            price = self.base_pricelist_id._get_product_price(product, quantity, uom, date)
            src_currency = self.base_pricelist_id.currency_id
        elif rule_base == "standard_price":
            src_currency = product.cost_currency_id
            price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
        else:
            src_currency = product.currency_id
            price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
        if product._name == 'product.product':
            if product.product_tmpl_id.gr_currency_id:
                src_currency = product.product_tmpl_id.gr_currency_id
        elif product._name == 'product.template':
            if product.gr_currency_id:
                src_currency = product.gr_currency_id
        if src_currency != target_currency:
            price = src_currency._convert(price, target_currency, self.env.company, date, round=False)
        return price