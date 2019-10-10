

def get_semantic_types(apidesc, annotation_type, property_type, annot, whattosearch):
    if isinstance(apidesc, list):
        for elem in apidesc:
            get_semantic_types(elem, annotation_type, property_type, annot, whattosearch)
    elif isinstance(apidesc, dict):
        for k, v in apidesc.items():
            if k in ["parameters", "responses"]:
                annotation_type = k
            if isinstance(v, dict):
                if "responses" in v.keys():  # distinguish annotation of each response ex "200" "404" etc.
                    if "parameters" in v.keys():
                        get_semantic_types(v["parameters"], "parameters", property_type, annot, whattosearch)
                    for resp_kay, resp_value in v["responses"].items():
                        resp_annot = {resp_kay: []}
                        annot["responses"].append(resp_annot)
                        annotation_type = resp_kay
                        get_semantic_types(resp_value, annotation_type, property_type, annot, whattosearch)
                elif "properties" in v.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
                    prop = {v[whattosearch]: []}
                    annot[annotation_type].append(prop)
                    annotation_type = v[whattosearch]
                    for prop_elem in v["properties"]:
                        get_semantic_types(prop_elem, annotation_type, property_type, annot, whattosearch)
                else:
                    print('--------------', annot)
                    get_semantic_types(v, annotation_type, property_type, annot, whattosearch)
            else:
                print('FFFFFFFFFFFFFFFFF', annot)
                if k == whattosearch:
                    print("FFFFFFFFFFFFF  ", k, ":", v, "    ", annotation_type, annot)
                    insert_annotation(annot, annotation_type, v)



def get_semantic_types(apidesc, descpart, annotation_type, property_type, annot, whattosearch):
    if annotation_type == 'object':
        print("------------", descpart)
    #if isinstance(descpart, dict):
    #    print(descpart.keys())
    if isinstance(descpart, list):
        for elem in descpart:
            get_semantic_types(apidesc, elem, annotation_type, property_type, annot, whattosearch)
    elif isinstance(descpart, dict):
        if isinstance(descpart, dict) and "properties" in descpart.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
            prop = {descpart[whattosearch]: []}
            returned_annot = {annotation_type:[]}
            get_annotation_type(annot,annotation_type, returned_annot)
            returned_annot[annotation_type].append(prop)
            annotation_type = descpart[whattosearch]
            for k, prop_elem in descpart["properties"].items():
                get_semantic_types(apidesc, prop_elem, annotation_type, property_type, annot, whattosearch)
        else:
            for k, v in descpart.items():
                if k == "parameters":
                    get_semantic_types(apidesc, v, "parameters", property_type, annot, whattosearch)
                elif k == "responses":
                    for resp_kay, resp_value in v.items():
                        resp_annot = {resp_kay: []}
                        annot["responses"].append(resp_annot)
                        annotation_type = resp_kay
                        get_semantic_types(apidesc, resp_value["content"], annotation_type, property_type, annot, whattosearch)
                elif isinstance(v, dict) and "properties" in v.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
                    prop = {v[whattosearch]: []}
                    annot[annotation_type].append(prop)
                    annotation_type = v[whattosearch]
                    for prop_elem in v["properties"]:
                        get_semantic_types(apidesc, prop_elem, annotation_type, property_type, annot, whattosearch)
                elif k == "$ref":
                    refpath = v.split("/")
                    refdesc = apidesc
                    for i in range(1, len(refpath)):
                        refdesc = refdesc.get(refpath[i])
                    get_semantic_types(apidesc, refdesc, annotation_type, property_type, annot, whattosearch)
                elif k == whattosearch:
                    # print("FFFFFFFFFFFFF  ", k, ":", v, "    ", annotation_type, annot)
                    insert_annotation(annot, annotation_type, v)
                else:
                    # print('--------------', annot)
                    get_semantic_types(apidesc, v, annotation_type, property_type, annot, whattosearch)
    else:
        print(type(descpart))
        pass

##############################################################08-10-19 at 16h

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


def get_semantic_types(apidesc, descpart, annotation_type, property_type, annot, whattosearch):
    if annotation_type == 'object':
        print("------------", descpart)
    #if isinstance(descpart, dict):
    #    print(descpart.keys())
    if isinstance(descpart, list):
        for elem in descpart:
            get_semantic_types(apidesc, elem, annotation_type, property_type, annot, whattosearch)
    elif isinstance(descpart, dict):
        if isinstance(descpart, dict) and "properties" in descpart.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
            prop = {descpart[whattosearch]: []}
            returned_annot = {annotation_type:[]}
            get_annotation_type(annot,annotation_type, returned_annot)
            returned_annot[annotation_type].append(prop)
            annotation_type = descpart[whattosearch]
            for k, prop_elem in descpart["properties"].items():
                get_semantic_types(apidesc, prop_elem, annotation_type, property_type, annot, whattosearch)
        else:
            for k, v in descpart.items():
                if k == "parameters":
                    get_semantic_types(apidesc, v, "parameters", property_type, annot, whattosearch)
                elif k == "responses":
                    for resp_kay, resp_value in v.items():
                        resp_annot = {resp_kay: []}
                        annot["responses"].append(resp_annot)
                        annotation_type = resp_kay
                        get_semantic_types(apidesc, resp_value["content"], annotation_type, property_type, annot, whattosearch)
                elif isinstance(v, dict) and "properties" in v.keys():  # each ibject should be annotated as an object by defintnion of object class and classes of its properties
                    prop = {v[whattosearch]: []}
                    annot[annotation_type].append(prop)
                    annotation_type = v[whattosearch]
                    for prop_elem in v["properties"]:
                        get_semantic_types(apidesc, prop_elem, annotation_type, property_type, annot, whattosearch)
                elif k == "$ref":
                    refpath = v.split("/")
                    refdesc = apidesc
                    for i in range(1, len(refpath)):
                        refdesc = refdesc.get(refpath[i])
                    get_semantic_types(apidesc, refdesc, annotation_type, property_type, annot, whattosearch)
                elif k == whattosearch:
                    # print("FFFFFFFFFFFFF  ", k, ":", v, "    ", annotation_type, annot)
                    insert_annotation(annot, annotation_type, v)
                else:
                    # print('--------------', annot)
                    get_semantic_types(apidesc, v, annotation_type, property_type, annot, whattosearch)
    else:
        print(type(descpart))
        pass
