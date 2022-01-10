def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array


def singleTransform(values):
    return {
        "nik": values.nik,
        "name": values.name,
        "mobile": values.mobile
    }

def transformEdit(items):
    array = []

    for item in items:
        array.append(singleTransformEdit(item))
    return array


def singleTransformEdit(values):
    return {
        "id": values.id,
        "name": values.name,
        "mobile": values.mobile
    }


def transformMapping(items):
    array = []

    for item in items:
        array.append(singleTransformMapping(item))
    return array


def singleTransformMapping(values):
    return {
        "nik": values.nik,
        "name": values.name,
        "mobile": values.mobile
    }