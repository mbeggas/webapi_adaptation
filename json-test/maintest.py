import json
import yaml


def replace_annotation_text(semantic_annotation, at_context):
    at_type = semantic_annotation["@type"]
    if isinstance(at_context, dict):
        splited_at_type = at_type.split(":")
        prefix = at_context[splited_at_type[0]]
        semantic_annotation["@type"] = prefix + splited_at_type[1]
    else:
        semantic_annotation["@type"] = at_context + at_type


def replace_context_by_uri(semantic_annotation, at_context):
    if isinstance(semantic_annotation, dict):
        if "@type" in semantic_annotation.keys():
            replace_annotation_text(semantic_annotation, at_context)
        else:
            for key, value in semantic_annotation.items():
                replace_context_by_uri(value, at_context)
    else:
        if isinstance(semantic_annotation, list):
            for annotation in semantic_annotation:
                replace_context_by_uri(annotation, at_context)


def get_annotation_type(annotpart, annotation_type, returned_annot):
    if isinstance(annotpart, list):
        for elem in annotpart:
            get_annotation_type(elem, annotation_type, returned_annot)
    elif isinstance(annotpart, dict):
        if annotation_type in annotpart.keys():
            returned_annot[annotation_type] = annotpart[annotation_type]
        else:
            for k, elem in annotpart.items():
                get_annotation_type(elem, annotation_type, returned_annot)
    else:
        pass


def get_semantic_types(apidesc, descpart, annotation_type, field_name, annot, whattosearch):
    if isinstance(descpart, list):
        for elem in descpart:
            get_semantic_types(apidesc, elem, annotation_type, field_name, annot, whattosearch)
    elif isinstance(descpart, dict):
        if isinstance(descpart,
                      dict) and "properties" in descpart.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
            propname = ""
            if "name" in descpart.keys():
                propname = descpart["name"]
            prop = {descpart[whattosearch]: {"name": propname, whattosearch: descpart[whattosearch], "properties": []}}
            returned_annot = {annotation_type: []}
            get_annotation_type(annot, annotation_type, returned_annot)
            returned_annot[annotation_type].append(prop)
            annotation_type = "properties"  # descpart[whattosearch]
            for propk, prop_elem in descpart["properties"].items():
                field_name = propk
                get_semantic_types(apidesc, prop_elem, annotation_type, field_name, returned_annot, whattosearch)
        elif isinstance(descpart, dict) and whattosearch in descpart.keys():
            # print(field_name, ":", descpart)
            insert_annotation(annot, annotation_type, {"name": field_name, whattosearch: descpart[whattosearch]})
        else:
            for k, v in descpart.items():
                # print("FFFFFFFFFFFFF  ", v)
                if k == "parameters":
                    get_semantic_types(apidesc, v, "parameters", field_name, annot, whattosearch)
                elif k == "responses":
                    for resp_kay, resp_value in v.items():
                        resp_annot = {resp_kay: []}
                        annot["responses"].append(resp_annot)
                        annotation_type = resp_kay
                        get_semantic_types(apidesc, resp_value["content"], annotation_type, field_name, annot,
                                           whattosearch)
                # elif isinstance(v, dict) and "properties" in v.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
                #     prop = {v[whattosearch]: []}
                #     annot[annotation_type].append(prop)
                #     annotation_type = v[whattosearch]
                #     for prop_elem in v["properties"]:
                #         get_semantic_types(apidesc, prop_elem, annotation_type, field_name, annot, whattosearch)
                elif k == "$ref":
                    refpath = v.split("/")
                    if refpath[0] != '#':
                        raise Exception("External $Ref is not supported")
                    refdesc = apidesc
                    for i in range(1, len(refpath)):
                        refdesc = refdesc.get(refpath[i])
                    get_semantic_types(apidesc, refdesc, annotation_type, field_name, annot, whattosearch)
                # elif isinstance(v, dict) and whattosearch in v.keys():
                #     # print(field_name, ":", v)
                #     insert_annotation(annot, annotation_type, {"name": field_name, whattosearch: v[whattosearch]})
                else:
                    # print('--------------', annot)
                    if k == "name":
                        field_name = v
                    get_semantic_types(apidesc, v, annotation_type, field_name, annot, whattosearch)
    # else:
    #     pass


def insert_annotation(annotations, anntation_type, type_value):
    if isinstance(annotations, dict):
        if anntation_type in annotations.keys():
            annotations[anntation_type].append(type_value)
        else:
            for enntry, value in annotations.items():
                insert_annotation(value, anntation_type, type_value)
    elif isinstance(annotations, list):
        for value in annotations:
            insert_annotation(value, anntation_type, type_value)


if __name__ == "__main__":
    import urllib.request

    x = urllib.request.urlopen(
        'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')
    print(yaml.load(x.read(), Loader=yaml.FullLoader))

    with open("apifiles/getimage-api.yaml", "r") as file:
        imagedesc = yaml.load(file, Loader=yaml.FullLoader)

    # getsemantictypes-(getimDescGetMethod)
    imagedesc_getmethod = imagedesc["paths"]["/images"]["get"]
    annot = {"parameters": [], "responses": []}
    # get_semantic_types(imagedesc, imagedesc_getmethod, "", "", annot, "@type")
    print(annot)

    with open("apifiles/petstore-v3.yaml", "r") as file:
        petdesc = yaml.load(file, Loader=yaml.FullLoader)
    annot2 = {"parameters": [], "responses": []}
    get_semantic_types(petdesc, petdesc["paths"]["/pets/{petId}"]["get"], "", "", annot2, "type")
    print(annot2)
