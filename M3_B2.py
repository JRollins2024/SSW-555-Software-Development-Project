#Jamie Rollins
#M2_B3 GEDCOM Data
#I pledge my honor that I have abided by the Stevens Honor System.

#Save information about individuals and families as lists (or collections)

from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from pathlib import Path
from gedcom.element.element import Element
from gedcom.element.family import FamilyElement
import json

#elements at level 1 and deeper
def child_helper(element):
    children = element.get_child_elements()
    if children:
        for child in children:
            print("--> " + str(child))
            if child.get_tag() in Tags:
                isValid = "Y"
            else:
                isValid = "N"
            argument = str(child)[2:]
            argument = argument.replace(str(child.get_tag()), '')
            print("<-- " + str(child.get_level()) + "|" + child.get_tag() + "|" + isValid + "|" + argument[1:])
            child_helper(child)

# Path to your `.ged` file
folderPath = Path("C:/Users/JRoll/OneDrive - stevens.edu/Stevens/CS-555/Module2_AgileCultures_UseCases_UserStories/Rollins_Jamie_M2_B3_GEDCOM/")
file_path = folderPath / "CS_555_M1_B6.ged"

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()

#Valid Tag List
Tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

#elements at level 0
for element in root_child_elements:
    if element.get_level() == 0:
    #print("<-- " + str(element.get_level()) + "|" + element.get_tag() + "|" + isValid + "|" + argument[1:])
    #child_helper(element)


individuals_dict, families_dict = {}, {}

# Populate dictionary information

# Individuals
with open("individuals.json", "w") as ind:
    json.dump(individuals_dict, ind)

ind.close()

# Families
with open("families.json", "w") as fam:
    json.dump(families_dict, fam)

fam.close()


