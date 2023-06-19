def create_entities_json(data, fields, required_field={}, partial_update=False):
    entities_count = data.get('last_related_count').split(',')
    r_data = []
    for count in entities_count:
        t_data = {**required_field}
        for field in fields:
            if field == 'order':
                t_data[field] = count
            else:
                t_data[field] = data.get(f'{count}_{field}', None)
        r_data.append(t_data)
    return r_data