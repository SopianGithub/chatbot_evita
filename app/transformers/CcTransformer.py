import json

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

def segmenName(items):

    return items.name


def singleTransform(values):
    return {
        "id_cc": int(values.id_cc),
        "name": values.name,
        "segmen": segmenName(values.segmen),
        "alias": listToString(values.alias)
    }

def transformEdit(items):
    array = []

    for item in items:
        array.append(singleTransformEdit(item))
    return array

def singleTransformEdit(values):
    sgcc = {
        "id_segmen": values.segmen.id_segmen,
        "name": values.segmen.name,
        "descr": values.segmen.descr,
    }
    return {
        "id_cc": int(values.id_cc),
        "name": values.name,
        "segmen": sgcc,
        "alias": values.alias
    }

def transformmap(items):
    array = []

    for item in items:
        array.append(singleTransformMap(item))
    return array

def singleTransformMap(values):
    sgcc = {
        "id_segmen": values.segmen.id_segmen,
        "name": values.segmen.name,
        "descr": values.segmen.descr,
    }
    return {
        "id_cc": int(values.id_cc),
        "name": values.name,
        "segmen": sgcc,
        "alias": values.alias,
        "mapping": transformAM(values.mapping_am)
    }

def transformAM(items):
    array = []

    for item in items:
        array.append(singleTransformAM(item))
    return array


def singleTransformAM(values):
    return {
        "nik": values.nik,
        "name": values.name,
        "mobile": values.mobile
    }