from odoo import models
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    def _search_exact(self, search_details, search, limit, order):
        """
                Overriding '_search_exact' for change base domain in
                loading products to shop .
        """
        all_results = []
        total_count = 0
        website = request.env['website'].get_current_website()
        for rec in search_details:
            if rec['model'] == 'product.template':
                rec['base_domain'][0] = ['&', ('sale_ok', '=', True), ('allowed_website_ids', 'in', (False, website.id))]
        for search_detail in search_details:
            model = self.env[search_detail['model']]
            results, count = model._search_fetch(search_detail, search, limit, order)
            search_detail['results'] = results
            total_count += count
            search_detail['count'] = count
            all_results.append(search_detail)
        return total_count, all_results

