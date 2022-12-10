from functools import partial
from use_cases.validation_utils.concrete import is_same_user
from .is_access_allowed import is_access_allowed as __is_access_allowed

is_access_allowed = partial(
    __is_access_allowed,
    is_same_user_fn=is_same_user
)