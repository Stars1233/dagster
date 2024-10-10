from pathlib import Path

from dagster_sdf import SdfCliResource, SdfWorkspace, sdf_assets

import dagster as dg

workspace_dir = Path(__file__).joinpath("..", "./my_sdf_workspace").resolve()
target_dir = workspace_dir.joinpath(
    "sdf_dagster_out"
)  # The destination for outputs generated by SDF during execution
environment = "dbg"  # Replace with your environment, e.g. "prod"

workspace = SdfWorkspace(
    workspace_dir=workspace_dir,
    target_dir=target_dir,
    environment=environment,
)


@sdf_assets(workspace=workspace)
def my_sdf_assets(context: dg.AssetExecutionContext, sdf: SdfCliResource):
    yield from sdf.cli(
        ["run", "--save", "info-schema"],
        target_dir=target_dir,
        environment=environment,
        context=context,
    ).stream()


defs = dg.Definitions(
    assets=[my_sdf_assets],
    resources={
        "sdf": SdfCliResource(workspace_dir=workspace_dir),
    },
)
