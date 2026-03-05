from odoo import _, api, fields, models

HIDE_COORDINATES_PARAM = "address_dataset_base.hide_coordinates"


class AddressDatasetSettings(models.TransientModel):
    _name = "address.dataset.settings"
    _description = "Address Dataset Settings"

    name = fields.Char(default=lambda self: _("Configuration"))
    hide_coordinates = fields.Boolean(string="Hide Lat/Long")

    def _set_hide_coordinates_param(self, value):
        self.env["ir.config_parameter"].sudo().set_param(
            HIDE_COORDINATES_PARAM, "1" if value else "0"
        )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record, vals in zip(records, vals_list):
            if "hide_coordinates" in vals:
                record._set_hide_coordinates_param(vals["hide_coordinates"])
        return records

    def write(self, vals):
        result = super().write(vals)
        if "hide_coordinates" in vals:
            self[:1]._set_hide_coordinates_param(self[:1].hide_coordinates)
        return result

    @api.model
    def action_open_settings(self):
        hidden = self.env["ir.config_parameter"].sudo().get_param(
            HIDE_COORDINATES_PARAM, "0"
        ) in ("1", "true", "True")
        wizard = self.search([], order="id desc", limit=1)
        vals = {
            "name": _("Configuration"),
            "hide_coordinates": hidden,
        }
        if wizard:
            wizard.write(vals)
        else:
            wizard = self.create(vals)
        return {
            "type": "ir.actions.act_window",
            "name": _("Configuration"),
            "res_model": "address.dataset.settings",
            "view_mode": "form",
            "views": [
                (
                    self.env.ref("address_dataset_base.view_address_dataset_settings_form").id,
                    "form",
                )
            ],
            "res_id": wizard.id,
            "target": "current",
            "context": {"form_view_initial_mode": "edit"},
        }

    def action_save(self):
        self.ensure_one()
        self._set_hide_coordinates_param(self.hide_coordinates)
        return {"type": "ir.actions.client", "tag": "reload"}

    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if "hide_coordinates" in fields_list:
            values["hide_coordinates"] = self.env["ir.config_parameter"].sudo().get_param(
                HIDE_COORDINATES_PARAM, "0"
            ) in ("1", "true", "True")
        return values
