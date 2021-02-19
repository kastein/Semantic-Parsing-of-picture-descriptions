
class BackAndForth_Iterator:
    def __init__(self,somelist):
        self.index = -1
        self.list = somelist

    def next(self):
        if self.list == []:
            raise StopIteration
        index += 1
        if index >= len(self.list):
            index = 0
        return self.list[index]

    def previous(self):
        if self.list == []:
            raise StopIteration
        index -= 1
        if index < 0:
            index = len(self.somelist)-1
        return self.list[index]
    
        
