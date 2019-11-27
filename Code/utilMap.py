# -*- coding: utf-8 -*-

class Map:
    def __init__(self, defaultReturn):
        self.m = dict()
        self.default = defaultReturn # what is returned in a failure to get key
    def ListKeys(self):
        return self.m.keys()
    def InMap(self,key):
        if key in self.m.keys():
            return True
    def Set(self, key, value):
        self.m[key] = value
    def Add(self, key, value):
        self.m[key] = value
    def Del(self,key):
        if self.InMap(key):
            self.m.pop(key)
    # set the default return to be used for now on
    def setDefaultReturn(self,defaultReturn):
        self.default = defaultReturn
    # 
    def Get(self,key):
        if self.InMap(key):
            return self.m[key]
        return self.default
    def DeepCopy(self):
        m = Map(self.default)
        List = self.ListKeys
        for key in List:
            m.Add(key,self.Get(key))
        return m

def CreateMapofEmptyInterfaces(ListOfKeys):
    m = Map("")
    for key in ListOfKeys:
        m.Add(key,EmptyInterface())
    return m
    
# wanted something similar to an empty interface obj in go
def EmptyInterface():
    return type('', (), {})()