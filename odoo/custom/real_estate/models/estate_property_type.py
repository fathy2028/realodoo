from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'A property type name must be unique.'),
    ]
