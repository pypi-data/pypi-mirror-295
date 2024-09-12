from tqdm import tqdm
from src._environment import Environment
from src._objects import ObjectType, Objects, SubItems

environment = Environment.from_env_file("presales-ovh")

for object in tqdm(['actions','metadataDefinitions','profiles', 'resources', 'workflowDefinitions']): 
    object_type = ObjectType.from_string(object)

    print(f"Deleting {object_type}")
    objects = Objects(
        object_type=object_type,
        sub_items=SubItems.from_object_type(object_type),
        filters={},
        mode="partial",
    ).get_from(environment)

    for _ in objects:
        _.stop(environment)
        _.disable(environment)
        _.delete(environment)
