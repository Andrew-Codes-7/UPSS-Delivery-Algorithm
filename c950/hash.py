
#Create hash table class
class CreateHash:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    #Inserts a new item into the hash table
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #Update if not already in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        #If not already in bucket, insert item to end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True


    def search_hash(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1] #Value
        return None  #No matches

    def remove_hash(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #if present, removes item
        if key in bucket_list:
            bucket_list.remove(key)


