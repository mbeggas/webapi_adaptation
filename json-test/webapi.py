import yaml
import maintest


class WebApiEndpoint:
    # self.apidesc
    # self.semantic_annotation
    # self.syntactic_annotation
    # self.at_context   for jsol-ld context

    # api_path ex: "paths#/pets/{petId}#get"
    def __init__(self, descfile, api_path):
        with open(descfile, "r") as file:
            self.desc = yaml.load(file, Loader=yaml.FullLoader)
        path_elements = api_path.split("#")
        self.apidesc = self.desc
        for i in range(0, len(path_elements)):
            self.apidesc = self.apidesc.get(path_elements[i])

        self.at_context = None
        if "@context" in self.desc:
            self.at_context = self.desc["@context"]

        self.postcondition = self.apidesc["postcondition"] if "postcondition" in self.apidesc.keys() else None
        self.precondition = self.apidesc["precondition"] if "precondition" in self.apidesc.keys() else None
        self.semantic_annotation = {"parameters": [], "responses": []}
        self.syntactic_annotation = {"parameters": [], "responses": []}

        self.parameters = None
        self.responses = None
        self.response200 = None

        self.__retrieve_annotations()
        self.__retrieve_parameters_responses()

        # end of method __init__

    def __retrieve_annotations(self):
        maintest.get_semantic_types(self.desc, self.apidesc, "", "", self.syntactic_annotation, "type")
        maintest.get_semantic_types(self.desc, self.apidesc, "", "", self.semantic_annotation, "@type")
        if self.at_context is not None:
            maintest.replace_context_by_uri(self.semantic_annotation, self.at_context)

    def __retrieve_parameters_responses(self):
        self.parameters = self.semantic_annotation["parameters"]
        self.responses = self.semantic_annotation["responses"]
        self.response200 = None
        for response in self.responses:
            if "200" in response.keys():
                self.response200 = response["200"]
            elif 200 in response.keys():
                self.response200 = response[200]

    # TODO : adding semantic matching method between input-output
    def semantic_inout_matching(self, annotation_tomatch_with):
        # TODO in out
        #  object <=> object same same type --> direct validation
        #                    different type  --> validate by object properties
        #  slcalrs <=> sclarsme   ---> direct validation
        #  object <=> sclarsme  --->  scalar vs object properties
        pass

    def syntactic_inout_matching(self, annotation_to_match_with):
        pass

    def goal_postcondition_validation(self, goal):
        pass

    def __str__(self):
        return str(self.apidesc)


api2 = WebApiEndpoint("apifiles/getimage-api.yaml", "paths#/images#get")


print(api2.syntactic_annotation)
print(api2.semantic_annotation)
print(api2.postcondition)
print(api2.precondition)


class MyClass:
    def __init__(self, x=None):
        self.x = x

    def set_x(self, x):
        self.x = x
