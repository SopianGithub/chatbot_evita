def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array

def listToString(s):
    # initialize an empty string
    str1 = "; "
    # return string
    return (str1.join(s))

def singleTransform(values):
    return {
        "nik": values.nik,
        "name": values.name,
        "mobile": values.mobile,
        "loker": {
            "title": values.loker.title,
            "bp": values.loker.bp,
            "divisi": values.loker.divisi,
            "unit": values.loker.unit,
            "sub_unit": values.loker.sub_unit,
            "alias": listToString(values.loker.alias),
        }
    }


def transformEdit(items):
    array = []

    for item in items:
        array.append(singleTransformEdit(item))
    return array

def singleTransformEdit(values):
    return {
        "nik": values.nik,
        "name": values.name,
        "mobile": values.mobile,
        "loker": {
            "id": str(values.loker.id),
            "title": values.loker.title,
            "bp": values.loker.bp,
            "divisi": values.loker.divisi,
            "unit": values.loker.unit,
            "sub_unit": values.loker.sub_unit,
            "alias": values.loker.alias,
        },
        "loker_select": values.loker.divisi+"||"+values.loker.divisi+"||"+values.loker.unit+"||"+values.loker.sub_unit
    }