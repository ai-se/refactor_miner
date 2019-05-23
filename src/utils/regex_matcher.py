import re
import platform
import pandas as pd


class regex_matcher(object):

    def __init__(self):
        self.expression = None

    def case_statements(self):

        switcher = {
        "Extract Method": "Extract Method (.+) extracted from (.+) in class (.+)",
        "Rename Class":"Rename Class (.+) renamed to (.+)",
        "Move Attribute": "Move Attribute (.+) from class (.+) to class (.+)",
        "Move And Rename Attribute": "Move And Rename Attribute (.+) renamed to (.+) and moved from class (.+) to class (.+)",
        "Replace Attribute": "Replace Attribute (.+) from class (.+) with (.+) from class (.+)",
        "Rename Method": "Rename Method (.+) renamed to (.+) in class (.+)",
        "Inline Method": "Inline Method (.+) inlined to (.+) in class (.+)",
        "Move Method": "Move Method (.+) from class (.+) to (.+) from class (.+)",
        "Pull Up Method": "Pull Up Method (.+) from class (.+) to (.+) from class (.+)",
        "Move Class": "Move Class (.+) moved to (.+)",
        "Move And Rename Class": ".+",
        "Move Source Folder": "Move Source Folder (.+) to (.+)",
        "Pull Up Attribute": "Pull Up Attribute (.+) from class (.+) to class (.+)",
        "Push Down Attribute": "Push Down Attribute (.+) from class (.+) to class (.+)",
        "Push Down Method": "Push Down Method (.+) from class (.+) to (.+) from class (.+)",
        "Extract Interface": "Extract Interface (.+) from classes \\[(.+)\\]",
        "Extract Superclass": "Extract Superclass (.+) from classes \\[(.+)\\]",
        "Extract Subclass": "Extract Subclass (.+) from class (.+)",
        "Extract Class": "Extract Class (.+) from class (.+)",
        "Merge Method": ".+",
        "Extract And Move Method": "Extract And Move Method (.+) extracted from (.+) in class (.+) & moved to class (.+)",
        "Convert Anonymous Class to Type": ".+",
        "Introduce Polymorphism": ".+",
        "Change Package": "Change Package (.+) to (.+)",
        "Change Method Signature": "Change Method Signature (.+) to (.+) in class (.+)",
        "Extract Variable": "Extract Variable (.+) in method (.+) from class (.+)",
        "Inline Variable": "Inline Variable (.+) in method (.+) from class (.+)",
        "Rename Variable": "Rename Variable (.+) to (.+) in method (.+) from class (.+)",
        "Rename Parameter": "Rename Parameter (.+) to (.+) in method (.+) from class (.+)",
        "Rename Attribute": "Rename Attribute (.+) to (.+) in class (.+)",
        "Merge Variable": "Merge Variable \\[(.+)\\] to (.+) in method (.+) from class (.+)",
        "Merge Parameter": "Merge Parameter \\[(.+)\\] to (.+) in method (.+) from class (.+)",
        "Merge Attribute": "Merge Attribute \\[(.+)\\] to (.+) in class (.+)",
        "Split Variable": "Split Variable (.+) to \\[(.+)\\] in method (.+) from class (.+)",
        "Split Parameter": "Split Parameter (.+) to \\[(.+)\\] in method (.+) from class (.+)",
        "Split Attribute": "Split Attribute (.+) to \\[(.+)\\] in class (.+)",
        "Replace Variable With Attribute": "Replace Variable With Attribute (.+) to (.+) in method (.+) from class (.+)",
        "Parameterize Variable": "Parameterize Variable (.+) to (.+) in method (.+) from class (.+)",
        "Change Return Type": "Change Return Type (.+) to (.+) in method (.+) from class (.+)",
        "Change Variable Type": "Change Variable Type (.+) to (.+) in method (.+) from class (.+)",
        "Change Parameter Type": "Change Parameter Type (.+) to (.+) in method (.+) from class (.+)",
        "Change Attribute Type": "Change Attribute Type (.+) to (.+) in class (.+)"
        }
