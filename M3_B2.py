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
from prettytable import PrettyTable

#initialize tables
fTable = PrettyTable() #table for families
iTable = PrettyTable() #table for individuals
iTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
fTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

#Initialize Dictionaries
individuals_dict, families_dict = {}, {}

#elements at level 1 and deeper
def child_helper(element,ID):
    name = "NA"
    gender = "NA"
    birthday = "NA"
    alive = "True"
    death = "NA"
    spawn = "NA"
    spouse = "NA"
    age = "0"
    birth_year = "0"
    death_year = "0"
    children = element.get_child_elements()
    if children:
        for child in children:
            #Look up name of individual
            if child.get_tag() == "NAME":
                #Separate name from rest of the line
                name = str(child)[2:].replace(str(child.get_tag()), '')
                name = name.splitlines()
                name = name[0]
                individuals_dict[ID] = name
            #Look up gender of individual
            if child.get_tag() == "SEX":
                #separate gender from rest of the line
                gender = str(child)[2:].replace(str(child.get_tag()), '')
                gender = gender.replace(" ", '')
                gender = gender.splitlines()
                gender = gender[0]
            # The line with this tage indicated birthday but not the actual date
            if child.get_tag() == "BIRT":
                #go a level deeper to find the DATE tag
                dates = child.get_child_elements()
                for d in dates:
                    if d.get_tag() == "DATE":
                        # separate date from rest of the line
                        birthday = str(d)[2:].replace(str(d.get_tag()), '')
                        birth_year = birthday[-6:]
                        birthday = birthday.splitlines()
                        birthday = birthday[0]
            # Indicates that this individual has died
            if child.get_tag() == "DEAT":
                alive = "False"
                #to get the actual date -> go a level deeper
                dates = child.get_child_elements()
                for d in dates:
                    if d.get_tag() == "DATE":
                        death = str(d)[2:].replace(str(d.get_tag()),'')
                        death_year = death[-6:]
                        death = death.splitlines()
                        death = death[0]
            # This individual is the child of the this family ID
            if child.get_tag() == "FAMC":
                spawn = str(child)[2:].replace(str(child.get_tag()), '')
                spawn = spawn.replace("@", '')
                spawn = spawn.replace(" ", '')
                spawn = spawn.splitlines()
                spawn = spawn[0]
            # This individual is the spouse of this family ID
            if child.get_tag() == "FAMS":
                spouse = str(child)[2:].replace(str(child.get_tag()), '')
                spouse = spouse.replace("@", '')
                spouse = spouse.replace(" ", '')
                spouse = spouse.splitlines()
                spouse = spouse[0]
        # If the individual is NOT dead subtract birth year from current year
        if death != "NA":
            age = int(death_year) - int(birth_year)
        else:
            # Else subtract from the year of death
            age = 2023 - int(birth_year)
        iTable.add_row([str(ID),name,gender,birthday,age,alive,death,spawn,spouse])

def family_helper(element, fID):
    # Variables
    married = "NA"
    divorced = "NA"
    hID = "NA"
    hName = "NA"
    wID = "NA"
    wName = "NA"
    spawns = []
    children = element.get_child_elements()
    #look at each child element (level 1)
    if children:
        for child in children:
            #Is there a marriage in the family
            if child.get_tag() == "MARR":
                #go down to level 2
                dates = child.get_child_elements()
                for d in dates:
                    if d.get_tag() == "DATE":
                        married = str(d)[2:].replace(str(d.get_tag()), '')
                        married = married.splitlines()
                        married = married[0]
            if child.get_tag() == "DIV":
                #go down to level 2
                dates = child.get_child_elements()
                for d in dates:
                    if d.get_tag() == "DATE":
                        divorced = str(d)[2:].replace(str(d.get_tag()), '')
                        divorced = divorced.splitlines()
            if child.get_tag() == "HUSB":
                #handles getting the husband's ID separated from rest of the line
                hID = str(child)[2:].replace(str(child.get_tag()), '')
                hID = hID.replace(" ", '')
                hID = hID.replace("@", '')
                hID = hID.splitlines()
                hID = hID[0]
            if child.get_tag() == "WIFE":
                #handles getting the wife's ID separated from rest of the line
                wID = str(child)[2:].replace(str(child.get_tag()), '')
                wID = wID.replace(" ", '')
                wID = wID.replace("@", '')
                wID = wID.splitlines()
                wID = wID[0]
            if child.get_tag() == "CHIL":
                #Append all children's IDs to list
                chil = str(child)[2:].replace(str(child.get_tag()), '')
                chil = chil.replace("@", '')
                chil = chil.replace(" ", '')
                chil = chil.splitlines()
                chil = chil[0]
                spawns.append(chil)
        #look up husband and wife IDs in dictionary
        hName = individuals_dict.get(hID)
        wName = individuals_dict.get(wID)
        fTable.add_row([fID,married,divorced,hID,hName,wID,wName,spawns])


# Path to your `.ged` file
folderPath = Path("C:/Users/JRoll/OneDrive - stevens.edu/Stevens/CS-555/Module2_AgileCultures_UseCases_UserStories/Rollins_Jamie_M2_B3_GEDCOM/")
file_path = folderPath / "CS_555_M1_B6.ged"

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()

#elements at level 0
for element in root_child_elements:
    if element.get_level() == 0:
        if element.get_tag() == "INDI":
            ID = str(element)[2:].replace(str(element.get_tag()), '')
            ID = ID.replace("@", '')
            ID = ID.replace(" ", '')
            ID = ID.splitlines()
            ID = ID[0]
            child_helper(element,ID)
        if element.get_tag() == "FAM":
            fID = str(element)[2:].replace(str(element.get_tag()), '')
            fID = fID.replace("@", '')
            fID = fID.replace(" ", '')
            fID = fID.splitlines()
            fID = fID[0]
            family_helper(element,fID)

print("Individual")
print(iTable)

print("Families")
print(fTable)



