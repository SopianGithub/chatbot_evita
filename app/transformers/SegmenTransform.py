def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array


def singleTransform(values):
    return {
        "id_segmen": values.id_segmen,
        "name": values.name,
        "descr": values.descr
    }