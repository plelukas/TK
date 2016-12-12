
class Memory:

    def __init__(self, name, parent=None): # memory name
        self.name = name
        self.dict = {}
        self.parent = parent

    def has_key(self, name):  # variable name
        return name in self.dict

    def has_stack_key(self, name):
        if self.parent is None:
            return self.has_key(name)
        else:
            return self.parent.has_stack_key(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.dict[name] = value

    def set(self, name, value):
        if self.parent is None:
            self.dict[name] = value
        else:
            if self.has_key(name):
                self.dict[name] = value
            else:
                self.parent.put(name, value)

    def get(self, name):    # gets from memory current value of variable <name>
        if self.parent is None:
            return self.dict.get(name)
        else:
            return self.dict.get(name) if self.has_key(name) else self.parent.get(name)

    def get_parent(self):
        return self.parent


class MemoryStack:

    def __init__(self, memory=Memory('root')):  # initialize memory stack with memory <memory>
        self.stack = []
        self.stack.append(memory)

    def get(self, name):             # gets from memory stack current value of variable <name>
        # for i in range(len(self.stack) - 1, -1, -1): # reversed loop
        #     if self.stack[i].has_key(name):
        #         return self.stack[i].get(name)
        # return None
        if self.stack[-1].has_stack_key(name):
            return self.stack[-1].get(name)
        else:
            return self.stack[0].get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        # for i in range(len(self.stack) - 1, -1, -1): # reversed loop
        #     if self.stack[i].has_key(name):
        #         self.stack[i].put(name, value)
        #         break
        if self.stack[-1].has_stack_key(name):
            self.stack[-1].set(name, value)
        else:
            self.stack[0].set(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def push_scope(self, memory):
        self.stack[-1] = memory

    def pop_scope(self):
        x = self.stack[-1]
        self.stack[-1] = x.get_parent()
        return x

