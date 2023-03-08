from odoo import models, _, fields
from odoo.addons.delivery_dhl.models.delivery_dhl import DHLProvider


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def _rate_shipment_vals(self, order=False, picking=False):
        if picking:
            warehouse_partner_id = picking.picking_type_id.warehouse_id.partner_id
            currency_id = picking.sale_id.currency_id or picking.company_id.currency_id
            destination_partner_id = picking.partner_id
            total_value = sum(sml.sale_price for sml in picking.move_line_ids)
        else:
            warehouse_partner_id = order.warehouse_id.partner_id
            currency_id = order.currency_id or order.company_id.currency_id
            total_value = sum(
                line.price_reduce_taxinc * line.product_uom_qty for line in
                order.order_line.filtered(lambda l: l.product_id.type in (
                'consu', 'product') and not l.display_type))
            destination_partner_id = order.partner_shipping_id

        rating_request = {}
        srm = DHLProvider(self.log_xml, request_type="rate",
                          prod_environment=self.prod_environment)
        check_value = srm.check_required_value(self, destination_partner_id,
                                               warehouse_partner_id,
                                               order=order, picking=picking)
        if check_value:
            return {'success': False,
                    'price': 0.0,
                    'error_message': check_value,
                    'warning_message': False}
        site_id = self.sudo().dhl_SiteID
        password = self.sudo().dhl_password
        rating_request['Request'] = srm._set_request(site_id, password)
        rating_request['From'] = srm._set_dct_from(warehouse_partner_id)
        if picking:
            packages = self._get_packages_from_picking(picking,
                                                       self.dhl_default_package_type_id)
        else:
            packages = self._get_packages_from_order(order,
                                                     self.dhl_default_package_type_id)
        rating_request['BkgDetails'] = srm._set_dct_bkg_details(self, packages)
        rating_request['To'] = srm._set_dct_to(destination_partner_id)
        if self.dhl_dutiable:
            rating_request['Dutiable'] = srm._set_dct_dutiable(total_value,
                                                               currency_id.name)
        real_rating_request = {}
        InsuredValue = rating_request['BkgDetails']['InsuredValue']
        print(rating_request)
        rating_request['BkgDetails']['InsuredValue'] = round(InsuredValue, 3)
        real_rating_request['GetQuote'] = rating_request
        real_rating_request['schemaVersion'] = 2.0
        self._dhl_add_custom_data_to_request(rating_request, 'rate')
        response = srm._process_rating(real_rating_request)
        print(response)

        available_product_code = []
        shipping_charge = False
        qtd_shp = response.findall('GetQuoteResponse/BkgDetails/QtdShp')
        print(qtd_shp)
        if qtd_shp:
            for q in qtd_shp:
                charge = q.find('ShippingCharge').text
                global_product_code = q.find('GlobalProductCode').text
                if global_product_code == self.dhl_product_code and charge:
                    shipping_charge = charge
                    shipping_currency = q.find('CurrencyCode') or False
                    shipping_currency = shipping_currency and shipping_currency.text
                    break
                else:
                    available_product_code.append(global_product_code)
        else:
            condition = response.find('GetQuoteResponse/Note/Condition')
            if condition:
                condition_code = condition.find('ConditionCode').text
                if condition_code == '410301':
                    return {
                        'success': False,
                        'price': 0.0,
                        'error_message': "%s.\n%s" % (
                        condition.find('ConditionData').text,
                        _("Hint: The destination may not require the dutiable option.")),
                        'warning_message': False,
                    }
                elif condition_code in ['420504', '420505', '420506',
                                        '410304'] or \
                        response.find(
                            'GetQuoteResponse/Note/ActionStatus').text == "Failure":
                    return {
                        'success': False,
                        'price': 0.0,
                        'error_message': "%s." % (
                            condition.find('ConditionData').text),
                        'warning_message': False,
                    }
        if shipping_charge:
            if order:
                order_currency = order.currency_id
            else:
                order_currency = picking.sale_id.currency_id or picking.company_id.currency_id
            if not shipping_currency or order_currency.name == shipping_currency:
                price = float(shipping_charge)
            else:
                quote_currency = self.env['res.currency'].search(
                    [('name', '=', shipping_currency)], limit=1)
                price = quote_currency._convert(float(shipping_charge),
                                                order_currency,
                                                order.company_id if order else picking.company_id,
                                                order.date_order if order else fields.Date.today())
            return {'success': True,
                    'price': price,
                    'error_message': False,
                    'warning_message': False}

        if available_product_code:
            return {'success': False,
                    'price': 0.0,
                    'error_message': _(
                        "There is no price available for this shipping, you should rather try with the DHL product %s",
                        available_product_code[0]),
                    'warning_message': False}
