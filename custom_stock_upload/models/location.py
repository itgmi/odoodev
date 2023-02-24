from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Location(models.Model):
    _inherit = 'stock.location'

    city = fields.Char('City')

    @api.onchange('city')
    def city_onchange(self):
        if self.city:
            if len(self.city) > 14:
                raise ValidationError('City must less than 14 Characters')
            else:
                self.city = self.city.upper()
