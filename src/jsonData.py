import json
import copy
from cst import cst

class jsonData:

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None
        self.act_dict = {} 
        with open(file_name, "r") as f:
            self.data = json.load(f)
        with open(file_name+".bak", "w") as f:
            json.dump(self.data, f)

    def save(self, file_name=""):
        if file_name == "":
            file_name = self.file_name
        with open(file_name, "w") as f:
            json.dump(self.data, f)

    def len(self):
        length = len(self.getActDict().items())
        return length

    '''CURD related
    '''
    def add(self, cur_entry):
        for entry in self.data:
            if self.sameEntry(entry, cur_entry):
                return False
        self.data.append(cur_entry)
        return True

    def remove(self, idx):
        if idx >= len(self.data):
            return False
        del self.data[idx]
        return True

    def renew(self, idx, entry):
        if idx >= len(self.data):
            return False
        self.data[idx] = entry
        print("Successfully updated entry {}.".format(idx))
        return True

    ''' Choose related
    '''
    def getActDict(self):
        if self.act_dict == {}:
            act_dict = {}
            for idx,each in enumerate(self.data):
                act_dict[idx] = each
            self.setActDict(act_dict)
            return self.act_dict
        return self.act_dict

    def setActDict(self, act_dict): 
        self.act_dict = act_dict

    def contain(self, entry_arr, seach_arr):
        for entry_item in entry_arr:
            if type(entry_item) == str:
                for search_item in seach_arr:
                    if search_item.strip().lower() in entry_item.lower():
                        return True
            elif type(entry_item) == list:
                if self.contain(entry_item, seach_arr):
                    return True
            elif type(entry_item) == int:
                if entry_item in seach_arr:
                    return True
        return False

    def choose(self, key, arr):
        act_dict = self.getActDict()
        for idx,entry in copy.copy(act_dict).items():
            if not self.contain(entry[key], arr):
                del act_dict[idx]
        print("{} entries selected.".format(len(act_dict)))
        self.setActDict(act_dict)

    def unchoose(self):
        length = self.len()
        self.setActDict({})
        print("Successfully unchoose {} entries.".format(length))

    '''Display related
    '''
    def assemb(self, entry, key):
        if key not in entry: return []
        arr = entry[key]
        res = [""]
        for item in arr:
            if type(item) == str: # For sent str
                for i in range(len(res)):
                    res[i] += item.strip()
            elif type(item) == list: # For sent lit
                n_res = []
                for res_sent in res:
                    for eachItem in item:
                        n_res.append(res_sent + " |"+eachItem.strip() +"| ")
                res = n_res
            elif type(item) == int: # For keys
                res.append(cst[key][item])
        return [item for item in res if item != ""]

    def display(self):
        act_dict = self.getActDict()
        for i,entry in act_dict.items():
            print("{}-th entry:".format(i))
            for key in ['cats', 'secs','tags', 'sent']:
                 print("\t{}:".format(key))
                 for each in self.assemb(entry, key):
                    print('\t\t{}'.format(each))

    def displayRaw(self, idx):
        if idx >= len(self.data):
            return False
        entry = self.data[idx]
        print("{}-th entry raw:".format(idx))
        print("\t{}".format(entry))

    def displayKey(self, key):
        key_d = {"cats": "categories", "secs":"sections", "tags":"tags"}
        print("In the key of '{}' in cst file:".format(key_d[key]))
        for idx,item in cst[key].items():
            print("\t{}: {}".format(idx, item))


    '''Currently obsolete
    def sameEntry(self, entry1, entry2):
        if len(entry1['sent']) != len(entry2['sent']):
            return False
        for item1,item2 in zip(entry1["sent"], entry2["sent"]):
            if type(item1) != type(item2):
                return False
            if type(item1) != str:
                continue
            if item1.strip() != item2.strip():
                return False
        return True

    def remove(self, cur_entry):
        for i in range(len(self.data)):
            entry = self.data[i]
            if self.sameEntry(entry, cur_entry):
                del self.data[i]
                return True
        return False

    def update(self, cur_entry):
        for i in range(len(self.data)):
            entry = self.data[i]
            if self.sameEntry(entry, cur_entry):
                self.data[i] = cur_entry
                return True
        return False

    args:   idx -- index in self.data; 
            subidx -- element index in "sent" to be replaced; 
            arr -- elements in replacement of subidx, single replacement just use arr with length=1; 
    def updateSent(self, idx, subidx, arr):
        if idx >= len(self.data):
            return False
        entry = self.data[idx]
        # If there's no subindex elemnet
        if subidx >= len(entry["sent"]):
            for each in arr:
                entry["sent"].append(each)
            return True
        # If there's subindex
        del entry["sent"][subidx]
        # Concatenate arr in the position of subindex
        arr.reverse()
        for each in arr:
            entry["sent"].insert(subidx, each)
        return True

    def update(self, idx, key, arr):
        if idx >= len(self.data):
            return False
        entry = self.data[idx]
        entry[key] = arr
        return True

    
    def display(self):
        for i,entry in enumerate(self.data):
            print("{}-th entry:".format(i))
            print("\tsent:\t {}".format(entry['sent']))
            print("\ttags:\t {}".format(entry['tags']))


    def assembList(self, arr):
        for i,entry in enumerate(arr):
            res = self.assembEntry(entry)
            print("{}-th entry sentences: Tags = {}".format(i, str(entry["tags"])))
            for res_sent in res:
                print("\t{}".format(res_sent))

    def assemb(self, key, arr):
        res = []
        for each in arr:
            if each in cst[key]:
                res.append(cst[key][each])
        return res

    def removeLast(self):
        del self.data[-1] 
    '''

if __name__ == "__main__":
    file_name = "struct.json"
    cur_entry = \
    {   "sent": ["X is",
               ],
        "tags": ["part", "+"]}
    jd = jsonData(file_name)
    jd.choose("sent", ["midst"])
    for i in range(6):
        jd.update(i, "cats", [1])
    jd.display()
    # jd.displayKey("secs")
    # jd.removeLast()
    # res = jd.update(cur_entry)
    #jd.updateSent(0, 2, [["cuaes", "reason", "account", "incentive","origin"], "of Y"])
    #jd.updateSent(0, 2, [""])
    # jd.updateSent(0, 2, [])
    #jd.updateSent(6, 5, ["more vital part"])
    # jd.display()
    #jd.assembList(jd.data)
    #print(res)
    jd.save()
    # print(data)