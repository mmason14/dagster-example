from dagster import (
    Definitions, 
    load_assets_from_modules,
    define_asset_job,
    ScheduleDefinition,
)

from the_project import assets
import os


all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    schedules=[
        ScheduleDefinition(
            job=define_asset_job(name="every_five_minutes", selection="*"),
            cron_schedule="*/5 * * * *"
        )
    ],

)
