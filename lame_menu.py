from builtins import str
from builtins import input
from builtins import object


# effect => Enter i to --> 'option'  /// i is the index of the corresponding option + 1
# Enetr 1 to --> Login as an existing user

class Menu(object):
    def __init__(self, options=None, title=None, message=None, b4_num = "Enter",
                 after_num = "to -->", prompt=">>>", refresh=lambda: None, 
                 invalid_msg = "Invalid input, please enter a valid"+
                 " number to select the corresponding option."):
        '''Example: m = Menu(options=[("Login as Admin",login,True),("Login as User",login,False)])
        This is an example of an option called Login as Admin and the other option called Login as 
        User And U have a function login which takes an argument is_admin to see as what is the 
        customer trying to login. If the function required more arguments, u can write it one after
        another separated by commas right after the function name'''
        if options is None:
            options = []
        self.options = None
        self.title = None
        self.is_title_enabled = None
        self.message = None
        self.is_message_enabled = None
        self.b4_num = None
        self.after_num = None
        self.prompt = None
        self.is_prompt_enabled = None
        self.refresh = None
        self.invalid_msg = None

        self.set_options(options)
        self.set_title(title)
        self.set_message(message)
        self.set_b4_num(b4_num)
        self.set_after_num(after_num)
        self.set_prompt(prompt)
        self.set_refresh(refresh)
        self.set_invalid_msg(invalid_msg)

    def set_options(self, options):
        original = self.options
        self.options = []
        try:
            for option in options:
                if not isinstance(option, tuple):
                    raise TypeError(option, "option is not a tuple")
                if len(option) == 0:
                    raise ValueError(option, "option is missing a string describing the option and a handler")
                elif len(option) == 1:
                    raise ValueError(option, "option is missing a handler")
                args = tuple([arg for arg in option[2:]]) if len(option) >= 3 else ()
                self.add_option(option[0], option[1], *args)
        except (TypeError, ValueError) as e:
            self.options = original
            raise e

    def set_title(self, title):
        self.title = title
        self.is_title_enabled = title is not None

    def set_message(self, message):
        self.message = message
        self.is_message_enabled = message is not None

    def set_b4_num(self, b4_num):
        self.b4_num = b4_num
        
    def set_after_num(self, after_num):
        self.after_num = after_num

    def set_prompt(self, prompt):
        self.prompt = prompt
        self.is_prompt_enabled = prompt is not None

    def set_refresh(self, refresh):
        if not callable(refresh):
            raise TypeError(refresh, "refresh should be callable, but yours is not")
        self.refresh = refresh

    def set_invalid_msg(self, invalid_msg):
        self.invalid_msg = invalid_msg

    def add_option(self, name, handler, *args):
        if not callable(handler):
            raise TypeError(handler, "handler should be callable, but yours is not")
        self.options += [(name, handler, args)]

    # use the menu
    def use(self):
        '''menu.use() returns handler(arguments), also let's menu start and work'''
        self.refresh()
        func_args = self.key_press()
        func = func_args[0]
        args = func_args[1]
        print()
        return func(*args)

    # show the menu
    def show(self):
        if self.is_title_enabled:
            print(self.title)
        if self.is_message_enabled:
            print(self.message)
        for (index, option) in enumerate(self.options):
            print(self.b4_num + " " + str(index + 1) + " " + self.after_num + " " + option[0])
        print()
        if self.is_prompt_enabled:
            print(self.prompt + " ",end="")
        
    # get the option index from a user input
    # return the corresponding option handler
    def key_press(self):
        self.show()
        while 1:
            try:
                index = int(input()) - 1
                if index == -1:
                    raise IndexError()
                option = self.options[index]
                handler = option[1]
                args = option[2]
                return handler, args
            except (ValueError, IndexError):
                print(self.invalid_msg)
                if self.is_prompt_enabled:
                    print(self.prompt + " ",end="")