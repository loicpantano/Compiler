class table_symboles:

    tableVariable = {}

    def add_variable(self, name, type):
        self.tableVariable[name] = type

    def add_function(self, name, type):
        self.tableVariable[name] = type