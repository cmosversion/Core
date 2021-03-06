#!/usr/bin/env python
# coding: utf8

class Core(object):
    def get_class(self, class_name=None):
        if class_name is None:
            return CoreUtil.get_class(self)
        return CoreUtil.get_class(class_name)

    def camel_case_to_underscore(self, string):
        words = []
        from_char_position = 0
        for current_char_position, char in enumerate(string):
            if char.isupper() and from_char_position < current_char_position:
                words.append(string[from_char_position:current_char_position].lower())
                from_char_position = current_char_position
        words.append(string[from_char_position:].lower())
        return '_'.join(words)

    def underscore_to_camel_case(self):
        splitted_string = string.split('_')
        # use string's class to work on the string to keep its type
        class_ = string.__class__
        return splitted_string[0] + class_.join('', map(class_.capitalize, splitted_string[1:]))

    def get_callable_methods(self):
        method_list = [method for method in dir(self) if callable(getattr(self, method))]
        return method_list
