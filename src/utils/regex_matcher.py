import re
import platform
import pandas as pd


class regex_matcher(object):

    def __init__(self):
        self.expression = None

    def case_statements(self,ref_type,refactoring_details):

        switcher = {
        "Extract Method":{
            'text':"Extract Method (.+) extracted from (.+) in class (.+)",
            'strings':['in class']
            },
        "Rename Class":{
            'text':"Rename Class (.+) renamed to (.+)",
            'strings':['Rename Class','renamed to']
            },
        "Move Attribute":{
            'text':"Move Attribute (.+) from class (.+) to class (.+)",
            'strings':['from class','to class']
            },
        "Move And Rename Attribute":{
            'text':"Move And Rename Attribute (.+) renamed to (.+) and moved from class (.+) from class (.+)",
            'strings':['from class','from class']
            },
        "Replace Attribute":{
            'text':"Replace Attribute (.+) from class (.+) with (.+) from class (.+)",
            'strings':['from class','with','from class']
            },
        "Rename Method":{
            'text':"Rename Method (.+) renamed to (.+) in class (.+)",
            'strings':['in class']
            },
        "Inline Method":{
            'text':"Inline Method (.+) inlined to (.+) in class (.+)",
            'strings':['in class']
            },
        "Move Method":{
            'text':"Move Method (.+) from class (.+) to (.+) from class (.+)",
            'strings':['from class','to','from class']
            },
        "Pull Up Method":{
            'text':"Pull Up Method (.+) from class (.+) to (.+) from class (.+)",
            'strings':['from class','to','from class']
            },
        "Move Class":{
            'text':"Move Class (.+) moved to (.+)",
            'strings':['Move Class','moved to']
            },
        "Move And Rename Class":{
            'text':".+",
            'strings':[]
            },
        "Move Source Folder":{ #check if this applies
            'text':"Move Source Folder (.+) to (.+)", 
            'strings':[]
            },
        "Pull Up Attribute":{
            'text':"Pull Up Attribute (.+) from class (.+) to class (.+)",
            'strings':['from class','to class']
            },
        "Push Down Attribute":{
            'text':"Push Down Attribute (.+) from class (.+) to class (.+)",
            'strings':['from class','to class']
            },
        "Push Down Method":{
            'text':"Push Down Method (.+) from class (.+) to (.+) from class (.+)",
            'strings':['from class','from class']
            },
        "Extract Interface":{
            'text':"Extract Interface (.+) from classes \\[(.+)\\]",
            'strings':['from classes']
            },
        "Extract Superclass":{
            'text':"Extract Superclass (.+) from classes \\[(.+)\\]",
            'strings':['from classes']
            },
        "Extract Subclass":{
            'text':"Extract Subclass (.+) from class (.+)",
            'strings':['from class']
            },
        "Extract Class":{
            'text':"Extract Class (.+) from class (.+)",
            'strings':['Extract Class','from class']
            },
        "Merge Method":{
            'text':".+",
            'strings':[]
            },
        "Extract And Move Method":{
            'text':"Extract And Move Method (.+) extracted from (.+) in class (.+) & moved to class (.+)",
            'strings':['in class','& moved to class']
            },
        "Convert Anonymous Class to Type":{
            'text':".+",
            'strings':[]
            },
        "Introduce Polymorphism":{
            'text':".+",
            'strings':[]
            },
        "Change Package":{
            'text':"Change Package (.+) to (.+)",
            'strings':[]
            },
        "Change Method Signature":{
            'text':"Change Method Signature (.+) to (.+) in class (.+)",
            'strings':['in class']
            },
        "Extract Variable":{
            'text':"Extract Variable (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Inline Variable":{
            'text':"Inline Variable (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Rename Variable":{
            'text':"Rename Variable (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Rename Parameter":{
            'text':"Rename Parameter (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Rename Attribute":{
            'text':"Rename Attribute (.+) to (.+) in class (.+)",
            'strings':['in class']
            },
        "Merge Variable":{
            'text':"Merge Variable \\[(.+)\\] to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Merge Parameter":{
            'text':"Merge Parameter \\[(.+)\\] to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Merge Attribute":{
            'text':"Merge Attribute \\[(.+)\\] to (.+) in class (.+)",
            'strings':['in class']
            },
        "Split Variable":{
            'text':"Split Variable (.+) to \\[(.+)\\] in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Split Parameter":{
            'text':"Split Parameter (.+) to \\[(.+)\\] in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Split Attribute":{
            'text':"Split Attribute (.+) to \\[(.+)\\] in class (.+)",
            'strings':['in class']
            },
        "Replace Variable With Attribute":{
            'text':"Replace Variable With Attribute (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Parameterize Variable":{
            'text':"Parameterize Variable (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Change Return Type":{
            'text':"Change Return Type (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Change Variable Type":{
            'text':"Change Variable Type (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Change Parameter Type":{
            'text':"Change Parameter Type (.+) to (.+) in method (.+) from class (.+)",
            'strings':['from class']
            },
        "Change Attribute Type":{
            'text':"Change Attribute Type (.+) to (.+) in class (.+)",
            'strings':['in class']
            },
        "Rename Package":{
            'text':"Rename Package (.+)",
            'strings':[]
        }
        }
        splitter = switcher[ref_type]['strings']
        if len(splitter) == 1:
            before_class = refactoring_details.split(splitter[0],1)[1].strip()
            before_class = before_class.split('[')
            if len(before_class) == 1:
                before_class = before_class[0]
            else:
                before_class = before_class[1].split(']')[0]
            after_class = before_class
        elif len(splitter) == 2:
            first_split = refactoring_details.split(splitter[0],1)
            second_split = first_split[1].split(splitter[1],1)
            before_class = second_split[0].strip()
            after_class = second_split[1].strip()
        elif len(splitter) == 3:
            first_split = refactoring_details.split(splitter[0],1)
            second_split = first_split[1].split(splitter[1],1)
            before_class = second_split[0].strip()
            third_split = second_split[1].split(splitter[2],1)
            after_class = third_split[1].strip()
        else:
            before_class,after_class = None,None

        return before_class,after_class

