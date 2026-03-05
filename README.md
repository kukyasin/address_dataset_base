<div align="center">

# Address Dataset Base

### Core Address Dataset Engine for Odoo 11.0 to 19.0 (Suite Foundation)

[![Odoo Version](https://img.shields.io/badge/Odoo-11.0%20to%2019.0-blue.svg)](https://www.odoo.com)
[![License](https://img.shields.io/badge/License-OPL--1-red.svg)](LICENSE)
[![Module Type](https://img.shields.io/badge/Type-Core%20Module-green.svg)](#)
[![Repo](https://img.shields.io/badge/GitHub-kukyasin%2Faddress__dataset__base-black.svg?logo=github)](https://github.com/kukyasin/address_dataset_base)
[![Support](https://img.shields.io/badge/Support-support%40algoritmetic.com-0d6e8a.svg)](mailto:support@algoritmetic.com)
[![Website](https://img.shields.io/badge/Website-algoritmetic.com-1f8a70.svg)](https://www.algoritmetic.com)

Reusable core module for country-specific address dataset addons.

</div>

---

## Overview

`address_dataset_base` is the shared foundation for multi-country address dataset modules in Odoo.

It provides:
- A generic address dataset model
- Partner form integration and auto-fill logic
- Latitude/longitude visibility controls
- Shared menus, views, and frontend field behavior

Country modules such as `l10n_tr_address_dataset`, `l10n_de_address_dataset`, `l10n_us_address_dataset` should depend on this module and only provide country-specific data import/load logic.

---

## Why This Architecture

- Clean separation between engine and country data
- Easier maintenance and upgrades
- Reusable implementation for new countries
- Odoo Apps friendly dependency model
- Better product strategy: free core + paid country datasets

---

## Key Features

### Generic Dataset Model
- Model: `address.dataset.location`
- Fields: country, state, city, neighborhood, zip, latitude, longitude
- SQL uniqueness protection on address key combination

### Partner Integration
- Adds neighborhood selection on partner form
- Auto-populates country/state/city/zip from selected neighborhood
- Keeps partner latitude/longitude synced with selected location
- Clears inconsistent values when address scope changes

### Coordinate Visibility Configuration
- Technical parameter: `address_dataset_base.hide_coordinates`
- Hides/shows coordinate fields in dataset and partner forms
- Centralized configuration UI

### Shared UI/UX Behavior
- Reusable list/form/search views for dataset records
- Menu entries for dataset management and configuration
- Many2one autocomplete behavior for controlled selection
- Float placeholder enhancement for coordinate fields

---

## Module Structure

```text
address_dataset_base/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── address_location.py
│   ├── res_partner.py
│   └── settings.py
├── security/
│   └── address_dataset_base_security.xml
├── views/
│   ├── address_dataset_views.xml
│   ├── address_dataset_settings_views.xml
│   └── res_partner_views.xml
└── static/
    ├── description/
    │   ├── index.html
    │   ├── icon.png
    │   └── main_screen.png
    └── src/
        ├── js/neighborhood_many2one_patch.js
        └── xml/float_field_placeholder.xml
```

---

## Data Model Reference

### `address.dataset.location`

| Field | Type | Description |
|------|------|-------------|
| `zip` | Char | Postal/ZIP code |
| `neighborhood` | Char | Neighborhood/area name |
| `country_id` | Many2one (`res.country`) | Country |
| `state_id` | Many2one (`res.country.state`) | State/Region |
| `city_id` | Many2one (`res.city`) | City |
| `lat` | Float | Latitude |
| `long` | Float | Longitude |
| `name` | Char (computed) | Display name |

### `address.dataset.settings`

| Field | Type | Description |
|------|------|-------------|
| `hide_coordinates` | Boolean | Hide/show lat/long in UI |

---

## Installation

### Requirements
- Odoo 11.0 to 19.0 (version-specific branch/package)
- Installed dependency: `base_address_extended`

### Steps
1. Put `address_dataset_base` in your addons path.
2. Restart Odoo.
3. Update Apps list.
4. Install **Address Dataset Base**.

---

## Usage

After installation:
- Go to **Address Dataset** menu.
- Manage location records under **Locations**.
- Configure coordinate visibility under **Configuration**.
- Open partner form and use the neighborhood field for auto-fill.

---

## Creating a Country Module

A country module should:
- Depend on `address_dataset_base`
- Contain only country dataset files + import hook
- Write into `address.dataset.location`

### Minimal Manifest Example

```python
{
    "name": "Turkey Address Dataset",
    "depends": ["address_dataset_base"],
    "data": [],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
```

### Hook Responsibilities
- Resolve country (`res.country`) by code
- Resolve/create states and cities as needed
- Upsert records in `address.dataset.location`
- Keep import idempotent

---

## Compatibility Notes

- The module line supports Odoo 11.0 through 19.0 via version-specific branches/packages.
- Use the branch/package matching your Odoo major version for production installations.

---

## Security

Internal users (`base.group_user`) are granted full CRUD on:
- `address.dataset.location`
- `address.dataset.settings`

Adjust access rules if your deployment requires stricter data governance.

---

## Support

For installation, customization, migration, and integrations:
- Email: `support@algoritmetic.com`
- Website: `https://www.algoritmetic.com`

---

## License

This module is licensed under **OPL-1**.
