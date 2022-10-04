def ELFhash(strings):
    hashcode = 0
    x = 0
    str_len = len(strings)
    for i in range(str_len):

        hashcode = (hashcode << 4) + ord(strings[i])
        x = hashcode & 0xF000000000000000
        if x:
            hashcode ^= (x >> 56)
            hashcode &= ~x
    return hashcode


class HashTable:
    def __init__(self, list_size=1):
        self.length = 0
        self.element_list = [[] for i in range(list_size)]

    def __getHashCode(self, key):
        list_size = len(self.element_list)
        hashcode = ELFhash(key) * 1317
        hashcode = (hashcode % list_size + list_size) % list_size
        hashcode_origin = hashcode
        while len(self.element_list[hashcode]) != 0 and self.element_list[hashcode][0] != key:
            hashcode += 1
            hashcode %= list_size
            if hashcode_origin == hashcode:
                break
        return hashcode

    def insert(self, key, value):
        list_size = len(self.element_list)
        if self.length * 100 >= list_size:
            newHashTable = HashTable(10 * list_size)
            for item in self.element_list:
                if not item:
                    continue
                [key_old, value_old] = item
                newHashTable.insert(key_old, value_old)
            self.element_list = newHashTable.element_list
        hashcode = self.__getHashCode(key)
        self.element_list[hashcode] = [key, value]
        self.length += 1

    def delete(self, key):
        hashcode = self.__getHashCode(key)
        if self.element_list == [] or self.element_list[hashcode][0] == key:
            self.element_list[hashcode] = []

    def update(self, key, value):
        hashcode = self.__getHashCode(key)
        if self.element_list == [] or self.element_list[hashcode][0] == key:
            self.element_list[hashcode] = [key, value]

    def get(self, key):
        hashcode = self.__getHashCode(key)
        if len(self.element_list[hashcode]) == 0:
            return None
        elif self.element_list[hashcode][0] == key:
            return self.element_list[hashcode][1]
        else:
            return None

    def items(self):
        items = []
        for item in self.element_list:
            if len(item) != 0:
                key, value = item
                items.append([key, value])
        return items

    def keys(self):
        keys = []
        for item in self.element_list:
            if len(item) != 0:
                key, value = item
                keys.append(key)
        return keys

    def values(self):
        values = []
        for item in self.element_list:
            if len(item) != 0:
                key, value = item
                values.append(value)
        return values

    def len(self):
        return self.length


class Trie_Tree:
    def __init__(self, character=""):
        self.hash_table = HashTable()
        self.character = character
        self.has_the_word = False

    def insert(self, key):
        if key == "":
            self.has_the_word = True
            return
        ch = key[0]
        subTree = self.hash_table.get(ch)
        if subTree is None:
            newTree = Trie_Tree(ch)
            self.hash_table.insert(ch, newTree)
            subTree = newTree
        subTree.insert(key[1:])

    def delete(self, key):
        if key == "":
            self.has_the_word = False
            return
        ch = key[0]
        subTree = self.hash_table.get(ch)
        if subTree is None:
            return
        subTree.delete(key[1:])

    def get(self, key):
        if key == "":
            return self.has_the_word
        ch = key[0]
        subTree = self.hash_table.get(ch)
        if subTree is None:
            return False
        return subTree.get(key[1:])


class Trie_Tree_origin:
    def __init__(self, character=""):
        self.element_list = []
        self.character = character
        self.has_the_word = False

    def getSubTree(self, key):
        for tree in self.element_list:
            if tree.character == key:
                return tree

    def insert(self, key):
        if key == "":
            self.has_the_word = True
            return
        ch = key[0]
        subTree = self.getSubTree(ch)
        if subTree is None:
            newTree = Trie_Tree(ch)
            self.element_list.append(newTree)
            subTree = newTree
        subTree.insert(key[1:])

    def delete(self, key):
        if key == "":
            self.has_the_word = False
            return
        ch = key[0]
        subTree = self.getSubTree(ch)
        if subTree is None:
            return
        subTree.delete(key[1:])

    def get(self, key):
        if key == "":
            return self.has_the_word
        ch = key[0]
        subTree = self.getSubTree(ch)
        if subTree is None:
            return False
        return subTree.get(key[1:])
