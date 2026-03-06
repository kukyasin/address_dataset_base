from odoo import _, api, fields, models

HIDE_COORDINATES_PARAM = "address_dataset_base.hide_coordinates"


class AddressDatasetLocation(models.Model):
    _name = "address.dataset.location"
    _description = "Address Dataset Location"
    _order = "zip, country_id, state_id, city_id, neighborhood"
    _rec_name = "neighborhood"

    zip = fields.Char(required=True, index=True)
    neighborhood = fields.Char(required=True, index=True)
    lat = fields.Float(string="Latitude", digits=(10, 6))
    long = fields.Float(string="Longitude", digits=(10, 6))
    country_id = fields.Many2one(
        comodel_name="res.country",
        required=True,
        index=True,
    )
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        required=True,
        index=True,
        domain="[('country_id', '=', country_id)]",
    )
    city_id = fields.Many2one(
        comodel_name="res.city",
        required=True,
        index=True,
        domain="[('country_id', '=', country_id), ('state_id', '=', state_id)]",
    )
    name = fields.Char(compute="_compute_name", store=True)
    hide_coordinates = fields.Boolean(compute="_compute_hide_coordinates")

    _address_dataset_unique_key = models.Constraint(
        "UNIQUE(country_id, state_id, city_id, zip, neighborhood)",
        "Postal address line must be unique.",
    )

    @api.depends("zip", "neighborhood", "city_id", "state_id")
    def _compute_name(self):
        for record in self:
            city = record.city_id.name or ""
            state = record.state_id.name or ""
            record.name = f"{record.zip or ''} - {record.neighborhood or ''} ({city}, {state})"

    def _compute_hide_coordinates(self):
        hidden = self.env["ir.config_parameter"].sudo().get_param(
            HIDE_COORDINATES_PARAM, "0"
        ) in ("1", "true", "True")
        for record in self:
            record.hide_coordinates = hidden

    @api.model
    def action_open_locations(self):
        hidden = self.env["ir.config_parameter"].sudo().get_param(
            HIDE_COORDINATES_PARAM, "0"
        ) in ("1", "true", "True")
        return {
            "type": "ir.actions.act_window",
            "name": _("Address Dataset"),
            "res_model": "address.dataset.location",
            "view_mode": "list,form",
            "views": [
                (self.env.ref("address_dataset_base.view_address_dataset_location_list").id, "list"),
                (self.env.ref("address_dataset_base.view_address_dataset_location_form").id, "form"),
            ],
            "search_view_id": self.env.ref("address_dataset_base.view_address_dataset_location_search").id,
            "context": {
                "address_dataset_hide_coordinates": hidden,
            },
        }
