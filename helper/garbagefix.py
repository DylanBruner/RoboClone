"""
A fix for the garbage collector when using Tkinter's PhotoImage class.
This class will act like a dictionary. When setting a value, if it doesn't already exist we create a list and add the value to it.
if the value already exists, we add the value to the list, and if the list is greater than 5 delete the first item in the list.
"""
class GarbageFix:
    def __init__(self, buffer_size: int = 5):
        self._dict = {}
        self._buffer_size = buffer_size

    def __getitem__(self, key):
        # return the last item in the list
        return self._dict[key][-1]
    
    def __setitem__(self, key, value):
        if key not in self._dict:
            self._dict[key] = [value]
        else:
            self._dict[key].append(value)
            if len(self._dict[key]) > self._buffer_size:
                del self._dict[key][0]
    
    def __delitem__(self, key):
        del self._dict[key]

    def __contains__(self, key):
        return key in self._dict
    
    def __len__(self):
        return len(self._dict)
    
    def __repr__(self):
        return repr(self._dict)