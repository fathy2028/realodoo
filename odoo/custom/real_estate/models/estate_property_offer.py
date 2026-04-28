from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            base = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - base).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals.get('property_id'))
            if prop.state in ('sold', 'canceled'):
                raise UserError("You cannot create an offer on a sold or canceled property.")
            if prop.offer_ids and vals.get('price', 0.0) < max(prop.offer_ids.mapped('price')):
                raise UserError(
                    "The offer must be higher than %.2f" % max(prop.offer_ids.mapped('price'))
                )
            if prop.state == 'new':
                prop.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            if 'accepted' in (offer.property_id.offer_ids - offer).mapped('status'):
                raise UserError("Another offer has already been accepted for this property.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
