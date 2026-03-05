# Address Dataset Base

Core engine module for country-specific address datasets.

## Technical Name

`address_dataset_base`

## What It Provides

- Generic dataset model: `address.dataset.location`
- Partner integration (country/state/city/neighborhood/zip auto-fill)
- Latitude/longitude fields on partner
- Coordinate visibility configuration
- Shared views, menu and helper UI logic

Country modules should only depend on this module and load/import their dataset.
