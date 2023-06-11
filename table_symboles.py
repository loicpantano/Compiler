class SymbolTable:
    def __init__(self):
        self.symbolstype = {}
        self.symbolsmemory = {}
        self.symbolargstype = {}


        self.current_function = None

    def add_symbol(self, name, type, args):
        self.symbolstype[name] = type
        self.symbolargstype[name] = [param.type for param in args]
        self.symbolsmemory[name] = len(self.symbolsmemory) * 4


    def get_type(self, name):
        return self.symbolstype.get(name)
    
    def get_nbArgs(self, name):
        return len(self.symbolargstype.get(name))

    def set_current_function(self, function_name):
        self.current_function = function_name

    def generate_function_code(self, function):
        self.set_current_function(function['name'])
        code = f"{function['type']} {function['name']}() {{\n"
        for statement in function['statements']:
            if statement['type'] == 'return':
                code += self.generate_return_statement(statement)
            elif statement['type'] == 'write':
                code += f"\twrite({statement['expression']}) ;\n"
            elif statement['type'] == 'function_call':
                code += self.generate_function_call(statement)
        code += "}\n"
        self.set_current_function(None)
        return code

    def generate_return_statement(self, statement):
        if self.current_function is None:
            raise ValueError("Return statement found outside a function.")
        expected_type = self.get_type(self.current_function)
        actual_type = self.get_type(statement['expression'])
        if expected_type != actual_type:
            raise ValueError(f"Return type mismatch in function {self.current_function}.")
        return f"\treturn {statement['expression']} ;\n"

    def generate_function_call(self, statement):
        function_name = statement['function_name']
        function_type = self.get_type(function_name)
        if function_type is None:
            raise ValueError(f"Function {function_name} is not defined.")
        if self.current_function is not None:
            expected_type = self.get_type(self.current_function)
            if expected_type != function_type:
                raise ValueError(f"Function call type mismatch in function {self.current_function}.")
            return f"\t{function_name}() ;\n"
        return f"\t{statement['expression']} = {function_name}() ;\n"

