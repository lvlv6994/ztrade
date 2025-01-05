#!bin/python
class helloworld:
    def __init__(self):
        self.hello = {
                'hello':1,
                'world':2,
                }
        self.world = {
                "hello" : "hello",
                "world" : "world",
                }
        self.helloworld = "hello world"
        self.list = [1,2,3]
        self.set = {12,23}
        self.he = {"zhang":{"zhang":{"xiao":"min"}}}
        print(type(self.list))
        print(type(self.set))
        print(type(self.helloworld))
        print(type(self.hello))
        print(type(self.world))
        print(type(self.he))



print(helloworld().hello.get('hello'))
