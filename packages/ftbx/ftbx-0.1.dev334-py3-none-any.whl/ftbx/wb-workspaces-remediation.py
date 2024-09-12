from datetime import datetime
from src._environment import Environment
from src._objects import ObjectType, Objects
from tqdm import tqdm
import pandas
import time

WORKSPACE_ID = 303

xmls = []
proxies = []
unknown = []
sequences = []
tars = []
remed = []

wb_prod = environment = Environment.from_env_file("wb-prod")
object_request = Objects(
    object_type=ObjectType.ASSETS,
    filters={"workspaceId": WORKSPACE_ID, "createdTo": "23 Jul 2024", "assetType": "File", "fileType": "Media"},
    sub_items=["parentGroups"],
    mode="full",
)

assets = object_request.get_from(wb_prod)

# asset.id, workspace.id, objectType.name, parent.id, parent.workspace.id, action
now = datetime.now()
df = pandas.DataFrame(
    columns=[
        "asset.id",
        "workspace.id",
        "objectType.name",
        "category",
        "parent.id",
        "parent.workspace.id",
        "action",
        "job.id",
    ]
)
for asset in tqdm(assets, "Remediating workspace"):
    # PACKAGES
    if (
        asset.parentGroups is not None
        and asset.parentGroups["memberships"]
        and "_ingest.xml" not in asset.name
    ):
        object_workspace_id = asset.workspace["id"]
        parent_workspace_id = asset.parentGroups["memberships"][0]["asset"][
            "workspaceId"
        ]
        if object_workspace_id != parent_workspace_id:
            instance = wb_prod.session.request(
                method="POST",
                url=f"{environment.url}/api/jobs",
                data={
                    "assetId": asset.id,
                    "actionId": 273759434,
                    "stringVariables": {"workspaceId": parent_workspace_id},
                },
            )
            row = pandas.DataFrame(
                [
                    {
                        "asset.id": asset.id,
                        "workspace.id": object_workspace_id,
                        "objectType.name": asset.objectType["name"],
                        "category": "PACKAGE",
                        "parent.id": asset.parentGroups["memberships"][0]["asset"][
                            "id"
                        ],
                        "parent.workspace.id": parent_workspace_id,
                        "action": f"MOVED",
                        "job.id": instance.get("id"),
                    }
                ]
            )
            df = pandas.concat([df, row], ignore_index=True)
            # print(
            #     f"Moved asset id {asset.id} from {object_workspace_id} to {parent_workspace_id} with job id {instance.get('id')}. "
            # )
            time.sleep(0.3) 
        else:
            row = pandas.DataFrame(
                [
                    {
                        "asset.id": asset.id,
                        "workspace.id": object_workspace_id,
                        "objectType.name": asset.objectType["name"],
                        "category": "PACKAGE",
                        "parent.id": asset.parentGroups["memberships"][0]["asset"][
                            "id"
                        ],
                        "parent.workspace.id": parent_workspace_id,
                        "action": f"IGNORED",
                        "job.id": None,
                    }
                ]
            )
            df = pandas.concat([df, row], ignore_index=True)
            # print(f"Ignoring asset id {asset.id} (PACKAGE)")
    # INGEST XML
    elif "_ingest.xml" in asset.name:
        row = pandas.DataFrame(
            [
                {
                    "asset.id": asset.id,
                    "workspace.id": asset.workspace["id"],
                    "objectType.name": asset.objectType["name"],
                    "category": "INGEST XML",
                    "parent.id": None,
                    "parent.workspace.id": None,
                    "action": f"IGNORED",
                    "job.id": None,
                }
            ]
        )
        df = pandas.concat([df, row], ignore_index=True)
        # print(f"Ignoring asset id {asset.id} (INGEST XML)")
    # PROXIES
    elif "proxy" in asset.assetOrigin.lower():
        row = pandas.DataFrame(
            [
                {
                    "asset.id": asset.id,
                    "workspace.id": asset.workspace["id"],
                    "objectType.name": asset.objectType["name"],
                    "category": "PROXY",
                    "parent.id": asset.parentAsset["id"],
                    "parent.workspace.id": asset.parentAsset["workspaceId"],
                    "action": f"IGNORED",
                    "job.id": None,
                }
            ]
        )
        df = pandas.concat([df, row], ignore_index=True)
        # print(f"Ignoring asset id {asset.id} (PROXY)")
    # PROXIES OR UNKNOWN
    elif "referenceName" in asset.__dict__:
        if "proxy" in asset.referenceName.lower():
            row = pandas.DataFrame(
                [
                    {
                        "asset.id": asset.id,
                        "workspace.id": asset.workspace["id"],
                        "objectType.name": asset.objectType["name"],
                        "category": "PROXY",
                        "parent.id": asset.parentAsset["id"],
                        "parent.workspace.id": asset.parentAsset["workspaceId"],
                        "action": f"IGNORED",
                        "job.id": None,
                    }
                ]
            )
            df = pandas.concat([df, row], ignore_index=True)
            # print(f"Ignoring asset id {asset.id} (PROXY)")
        else:
            row = pandas.DataFrame(
                [
                    {
                        "asset.id": asset.id,
                        "workspace.id": asset.workspace["id"],
                        "objectType.name": asset.objectType["name"],
                        "category": "UNKNOWN",
                        "parent.id": None,
                        "parent.workspace.id": None,
                        "action": f"IGNORED",
                        "job.id": None,
                    }
                ]
            )
            df = pandas.concat([df, row], ignore_index=True)
            # print(f"Ignoring asset id {asset.id} (UNKNOWN)")
    # SEQUENCE
    elif asset.objectType["name"] == "sequence":
        row = pandas.DataFrame(
            [
                {
                    "asset.id": asset.id,
                    "workspace.id": asset.workspace["id"],
                    "objectType.name": asset.objectType["name"],
                    "category": "SEQUENCE",
                    "parent.id": None,
                    "parent.workspace.id": None,
                    "action": f"IGNORED",
                    "job.id": None,
                }
            ]
        )
        df = pandas.concat([df, row], ignore_index=True)
        # print(f"Ignoring asset id {asset.id} (SEQUENCE)")
    # TARS
    elif (
        asset.objectType["name"] == "tar-asset"
        and not asset.parentGroups["memberships"]
    ):
        row = pandas.DataFrame(
            [
                {
                    "asset.id": asset.id,
                    "workspace.id": asset.workspace["id"],
                    "objectType.name": asset.objectType["name"],
                    "category": "TAR",
                    "parent.id": None,
                    "parent.workspace.id": None,
                    "action": f"IGNORED",
                    "job.id": None,
                }
            ]
        )
        df = pandas.concat([df, row], ignore_index=True)
        # print(f"Ignoring asset id {asset.id} (TAR)")
    # OTHER
    else:
        row = pandas.DataFrame(
            [
                {
                    "asset.id": asset.id,
                    "workspace.id": asset.workspace["id"],
                    "objectType.name": asset.objectType["name"],
                    "category": "UNKNOWN",
                    "parent.id": None,
                    "parent.workspace.id": None,
                    "action": f"IGNORED",
                    "job.id": None,
                }
            ]
        )
        df = pandas.concat([df, row], ignore_index=True)
        # print(f"Ignoring asset id {asset.id} (UNKNOWN)")

# print("\n")
# print(f"XMLS: {len(xmls)}")
# print(f"PROXIES: {len(proxies)}")
# print(f"SEQUENCE: {len(sequences)}")
# print(f"TARS: {len(tars)}")
# print(f"UNKNOWN: {len(unknown)} {[asset.id for asset in unknown]}")
#
# print(f"TOTAL TO REMED: {len(remed)}")

df.to_csv(f"wb-workspace-remed/remed_{now.strftime("%Y-%m-%dT%H-%M-%S")}")
