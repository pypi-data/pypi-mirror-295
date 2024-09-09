from typing import List
from django.conf import settings


def get_feature_flags_by_group_name(group_name: str) -> List[str]:
    assert hasattr(settings, "FEATURE_FLAGS"), "FEATURE_FLAGS not found in settings"
    assert group_name in settings.FEATURE_FLAG_GROUPS, f"Group {group_name} not found"
    return settings.FEATURE_FLAG_GROUPS[group_name]
