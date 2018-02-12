# Utility functions

def unique(list):
    return [x for i, x in enumerate(list) if x not in list[:i]]
