import ast
from cmd import Cmd
from jsonData import jsonData
from utils import try_deco
 
class MyPrompt(Cmd):
    prompt = '(Aca) '
    def __init__(self, file_name):
        super(MyPrompt, self).__init__()
        print("Wellcome to use xiaoda academic cmd app 1.0. Type help or ? to list commands.")
        print(
"::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\
:::'###:::::'######:::::'###::::::::::'##::::::::::'#####:::\n\
::'## ##:::'##... ##:::'## ##:::::::'####:::::::::'##.. ##::\n\
:'##:. ##:: ##:::..:::'##:. ##::::::.. ##::::::::'##:::: ##:\n\
'##:::. ##: ##:::::::'##:::. ##::::::: ##:::::::: ##:::: ##:\n\
 #########: ##::::::: #########::::::: ##:::::::: ##:::: ##:\n\
 ##.... ##: ##::: ##: ##.... ##::::::: ##:::'###:. ##:: ##::\n\
 ##:::: ##:. ######:: ##:::: ##:::::'######: ###::. #####:::\n\
..:::::..:::......:::..:::::..::::::......::...::::.....::::")
        self.jdata = jsonData(file_name)
        print("Using file: '{}', total entry length: {}.".format(file_name, self.jdata.len()))

    def do_exit(self, inp):
        print("Bye")
        return True

    @try_deco
    def do_save(self, inp):
        """Save to json data to file: SAVE"""
        self.jdata.save(inp.strip())

    @try_deco
    def do_len(self, inp):
        length = self.jdata.len()
        print("Current choosed data length: {}.".format(length))

    ''' CURD related
    '''
    @try_deco
    def do_add(self, inp):
        'Add entry to json data'
        entry = ast.literal_eval(inp)
        assert("sent" in entry)
        assert(type(entry["sent"])==list)
        self.jdata.add(entry)
        self.jdata.save()

    @try_deco
    def do_remove(self, inp):
        idx = int(inp)
        self.jdata.remove(idx)

    @try_deco
    def do_update(self, inp):
        args = inp.split(" ")
        idx = int(args[0])
        entry = ast.literal_eval(" ".join(args[1:]))
        assert("sent" in entry)
        self.jdata.renew(idx, entry)
        self.jdata.save()

    '''Choose related
    '''
    @try_deco
    def do_choose_sent(self, inp):
        arr = ast.literal_eval(inp)
        self.jdata.choose("sent", arr)

    @try_deco
    def do_choose_cats(self, inp):
        arr = ast.literal_eval(inp)
        self.jdata.choose("cats", arr)

    @try_deco
    def do_choose_secs(self, inp):
        arr = ast.literal_eval(inp)
        self.jdata.choose("secs", arr)

    @try_deco
    def do_choose_tags(self, inp):
        arr = ast.literal_eval(inp)
        self.jdata.choose("tags", arr)

    @try_deco
    def do_unchoose(self, inp):
        self.jdata.unchoose()

    ''' Display related
    '''
    @try_deco
    def do_dis(self, inp):
        self.jdata.display()

    @try_deco
    def do_disraw(self, inp):
        idx = int(inp)
        self.jdata.displayRaw(idx)

    @try_deco
    def do_discats(self, inp):
        # print("Adding '{}'".format(inp))
        self.jdata.displayKey("cats")

    @try_deco
    def do_dissecs(self, inp):
        # print("Adding '{}'".format(inp))
        self.jdata.displayKey("secs")

    @try_deco
    def do_distags(self, inp):
        self.jdata.displayKey("tags")


MyPrompt("struct.json").cmdloop()
# print("after")