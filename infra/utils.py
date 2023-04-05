def remove_keys_from_dict(base_dict, keys_to_remove):
    if not keys_to_remove: # for [] or None
        return base_dict
    key = keys_to_remove[0] # pop one
    if key in base_dict:
        if len(keys_to_remove) == 1:
            del base_dict[key] #works because we pass be reference
        else:
            remove_keys_from_dict(base_dict[key], keys_to_remove[1:])
    return base_dict