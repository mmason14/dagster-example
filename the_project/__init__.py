from dagster_aws.s3.io_manager import s3_pickle_io_manager
from dagster_aws.s3.resources import s3_resource

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
    resources={
        # With this I/O manager in place, your job runs will store data passed between assets
        # on S3 in the location s3://<bucket>/dagster/storage/<asset key>.
        "io_manager": s3_pickle_io_manager.configured({"s3_bucket": {"env": "S3_BUCKET"}}),
        "s3": s3_resource,
    },
    schedules=[
        ScheduleDefinition(
            job=define_asset_job(name="every_five_minutes", selection="*"),
            cron_schedule="*/5 * * * *"
        )
    ],

)
