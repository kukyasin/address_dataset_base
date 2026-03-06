from odoo import api, fields, models

HIDE_COORDINATES_PARAM = "address_dataset_base.hide_coordinates"


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_latitude = fields.Float(string="Geo Latitude", digits=(10, 7), default=False)
    partner_longitude = fields.Float(string="Geo Longitude", digits=(10, 7), default=False)

    neighborhood_id = fields.Many2one(
        comodel_name="address.dataset.location",
        string="Neighborhood",
    )
    hide_coordinates = fields.Boolean(compute="_compute_hide_coordinates")

    def _get_neighborhood_domain(self):
        self.ensure_one()
        if not self.country_id:
            return [("id", "=", 0)]

        domain = [("country_id", "=", self.country_id.id)]
        if self.state_id:
            domain.append(("state_id", "=", self.state_id.id))
        if self.city_id:
            domain.append(("city_id", "=", self.city_id.id))
        if self.zip:
            domain.append(("zip", "=", self.zip))
        return domain

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if "partner_latitude" in fields_list:
            values["partner_latitude"] = False
        if "partner_longitude" in fields_list:
            values["partner_longitude"] = False
        return values

    def _compute_hide_coordinates(self):
        hidden = self.env["ir.config_parameter"].sudo().get_param(
            HIDE_COORDINATES_PARAM, "0"
        ) in ("1", "true", "True")
        for partner in self:
            partner.hide_coordinates = hidden

    @api.onchange("neighborhood_id")
    def _onchange_neighborhood_id(self):
        for partner in self:
            neighborhood = partner.neighborhood_id
            if not neighborhood:
                continue
            partner.country_id = neighborhood.country_id
            partner.state_id = neighborhood.state_id
            partner.city_id = neighborhood.city_id
            partner.zip = neighborhood.zip
            partner.partner_latitude = neighborhood.lat or False
            partner.partner_longitude = neighborhood.long or False

    @api.onchange("country_id", "state_id", "city_id", "zip")
    def _onchange_address_scope(self):
        for partner in self:
            neighborhood = partner.neighborhood_id
            if not neighborhood:
                continue
            mismatch = (
                neighborhood.country_id != partner.country_id
                or neighborhood.state_id != partner.state_id
                or neighborhood.city_id != partner.city_id
                or (partner.zip and neighborhood.zip != partner.zip)
            )
            if mismatch:
                partner.neighborhood_id = False
                partner.partner_latitude = False
                partner.partner_longitude = False

        if len(self) == 1:
            return {"domain": {"neighborhood_id": self._get_neighborhood_domain()}}

    @api.onchange("country_id", "state_id", "city_id", "zip", "neighborhood_id")
    def _onchange_auto_fill_from_scope(self):
        for partner in self:
            if partner.neighborhood_id:
                continue

            domain = partner._get_neighborhood_domain()

            if domain == [("id", "=", 0)]:
                continue

            matches = self.env["address.dataset.location"].search(domain, limit=2)
            if len(matches) == 1:
                partner.neighborhood_id = matches.id
                partner.country_id = matches.country_id
                partner.state_id = matches.state_id
                partner.city_id = matches.city_id
                partner.zip = matches.zip
                partner.partner_latitude = matches.lat or False
                partner.partner_longitude = matches.long or False
