from dj_rql.filter_cls import AutoRQLFilterClass

from toy_store.models import Customer


class CustomerFilterClass(AutoRQLFilterClass):
    MODEL = Customer
    FILTERS = [
        {
            "filter": "name",
            "lookups": {"exact", "icontains"},
        },
        {
            "filter": "email",
            "lookups": {"exact", "icontains"},
        },
    ]
