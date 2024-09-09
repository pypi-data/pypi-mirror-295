This app helps to add feature flags to your django app

## Installation

```bash
pip install django-feature-flags
```

## Usage

Add `feature_flags` to your `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    'feature_flags',
    ...
]
```

Add your feature flags and feature flag groups in your `settings.py`

```python

FEATURE_FLAGS = {
    'feature1': {
        'description': 'This is a feature flag',
    },
    'feature2': {
        'description': 'This is a feature flag',
    },
    'feature3': {
        'description': 'This is a feature flag',
    },
}

FEATURE_FLAG_GROUPS = {
    'group1': ['feature1', 'feature2'],
    'group2': ['feature3'],
}
FEATURE_FLAG_DEFAULT_GROUP = 'group1'

```

Add the feature flag group to your tenant model

```python

from feature_flags.utils import get_feature_flags_by_group_name

class Tenant(models.Model):
    ...
    feature_flags_group = models.CharField(
        max_length=255,
        choices=FEATURE_FLAG_GROUPS.items(),
        default=FEATURE_FLAG_DEFAULT_GROUP,
    )
    ...

    @property
    def feature_flags(self):
        return get_feature_flags_by_group_name(self.feature_flags_group)

```
