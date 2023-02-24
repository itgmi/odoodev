from odoo import models, fields


class Channels(models.Model):
    _name = 'channels.gr'
    _description = 'Channels'

    name = fields.Char('Channel', required=True)
