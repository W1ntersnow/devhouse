def get_attrs_n_values(obj):
    return {att.replace('_id', ''): val for att, val in obj.__dict__.items() if not att.startswith('_')}