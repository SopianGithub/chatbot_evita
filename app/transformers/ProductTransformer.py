def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array

def transformEdit(items):
    array = []

    for item in items:
        array.append(singleTransformEdit(item))
    return array

def tranformFiles(items):
    array = []

    for item in items:
        array.append(fileTransform(item))
    return array

def listToString(s):
    str1 = "; "
    return (str1.join(s))

def singleTransform(values):
    return {
        "id": str(values.id),
        "name": values.name,
        "desc": values.desc,
        "alias": listToString(values.alias),
        "productfile": tranformFiles(values.productfile)
    }

def fileTransform(values):
    return {
        "type_file" : values.type_file,
        "url_file" : values.url_file
    }

def singleTransformEdit(values):
    return {
        "id": str(values.id),
        "name": values.name,
        "desc": values.desc,
        "benefit": values.benefit,
        "alias": values.alias,
        "productfile": tranformFiles(values.productfile)
    }