import hashlib

class HashTable():
    def __init__(self, length=20):
        self.array = [None] * length
    
    def hash(self, key):
        length = len(self.array)
        hashing = hashlib.sha1(key.encode('utf8'))
        return int(hashing.hexdigest(), 16) % length
        
    def add(self, key, value):
        index = self.hash(key)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    return
            self.array[index].append([key, value])
        else:
            self.array[index] = []
            self.array[index].append([key, value])
    
    def get(self, key):
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]
            raise KeyError()
    
    def remove(self, key):
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            self.array[index][:] = [x for x in self.array[index] if not key == x[0]]

    def __setitem__(self, key, value):
        self.add(key, value)
    
    def __getitem__(self, key):
        return self.get(key)


if __name__ == "__main__":
    myhash = HashTable()
    
    myhash['k1'] = '1'
    myhash['k2'] = '2'
    myhash['k3'] = '3'

    print(myhash['k1'])
    print(myhash['k2'])
    print(myhash['k3'])

    myhash['k1'] = '11'
    
    print(myhash['k1'])

    myhash.remove('k2')
    print(myhash['k1'])
    print(myhash['k3'])

