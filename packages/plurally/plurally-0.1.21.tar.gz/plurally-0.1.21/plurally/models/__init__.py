from plurally.models import crm  # noqa: F403
from plurally.models import email  # noqa: F403
from plurally.models import eshop  # noqa: F403
from plurally.models import logic  # noqa: F403
from plurally.models import table  # noqa: F403
from plurally.models import triggers  # noqa: F403
from plurally.models.action import ai  # noqa: F403
from plurally.models.action import arithmetic  # noqa: F403
from plurally.models.action import format  # noqa: F403
from plurally.models.action.ai import *  # noqa: F403
from plurally.models.action.arithmetic import *  # noqa: F403
from plurally.models.action.format import *  # noqa: F403
from plurally.models.email import *  # noqa: F403
from plurally.models.flow import Flow  # noqa: F401
from plurally.models.logic import *  # noqa: F403
from plurally.models.node import Node  # noqa: F401
from plurally.models.source import constant  # noqa: F403
from plurally.models.source.constant import *  # noqa: F403
from plurally.models.source.schedule import *  # noqa: F403

GROUPS = [
    ("Email", email),
    ("Table", table),
    ("AI", ai),
    ("CRM", crm),
    ("Eshop", eshop),
    ("Transforms", format),
    ("Constant Value", constant),
    ("Logic", logic),
    ("Maths", arithmetic),
    ("Triggers", triggers),
]

MAP = {}
for group_name, module in GROUPS:
    for kls_name in module.__all__:
        kls = getattr(module, kls_name)
        MAP[kls_name] = (kls, kls.InitSchema, group_name)


def create_node(**json_payload):
    node_kls = json_payload.pop("kls")
    return MAP[node_kls][0].parse(**json_payload)
