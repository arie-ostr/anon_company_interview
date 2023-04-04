
class TypeValidator():
    """
    This is just a funny idea I had at the moment,  given that I am needed
    to test data
    """

    @staticmethod
    def get_type_comp(o):
        """
        returns a lambda function that checks type , to be used in mask values.
        """
        return lambda x: isinstance(x, type(o))
    

    @staticmethod
    def _create_mask(item):
        if isinstance(item,dict):
            # we use recursion for nested dicts
            return TypeValidator.create_mask(item)
        elif isinstance(item,list):
            rl = []
            for item in v:
                rl.append(TypeValidator.create_mask(item))
                return rl
        else:
            return TypeValidator.get_type_comp(item)
    
    @staticmethod
    def create_mask(example_dict:dict)-> dict:
        """
        takes a normal dict and replaces all values with funcs for mask use
        """
        rd = {}
        for k,v in example_dict.items():
            rd[k] = TypeValidator._create_mask(v)
            
        return rd
    
    def __init__(self, tested_dict:dict,mask:dict):
        self.tested_dict = tested_dict
        self.mask = dict
        self.res = {"keys_missing" : [],
                    "keys_extra" : [],
                    "keys_wrong_type" : []}

    def validate(self):
        assert False, "Not implemented yet"

    