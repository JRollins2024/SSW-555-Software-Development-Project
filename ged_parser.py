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
import os
import sys

class Sprint1:
    #initialize tables
    fTable = PrettyTable() #table for families
    iTable = PrettyTable() #table for individuals
    iTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    fTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

    #Initialize Dictionaries
    individuals_dict, families_dict = {}, {}

    #Singles List
    Singles = [] # will hold the IDs of all individuals who are single
    Singles_elem = [] # will hold the full element of all individuals who are single

    #Multiples List
    Multiples = []

    #compare each individual's birthday and famc to every other individual's birthday and famc
    def compareBirthday(self,birthday, family, ID):
        mult = []
        multiples = False
        for e in gedcom_parser.get_root_child_elements():
            sameFam = False
            sameBirth = False
            samePerson = False
            #Get thid id of the individual you are comparing the given one to
            if e.get_tag() == "INDI":
                id = str(e)[2:].replace(str(e.get_tag()), '')
                id = id.replace("@", '')
                id = id.replace(" ", '')
                id = id.splitlines()
                id = id[0]
                if ID == id:
                    samePerson = True
            children = e.get_child_elements()
            for child in children:
                #Make sure siblings are children in the same family
                if child.get_tag() == "FAMC":
                    spawn = str(child)[2:].replace(str(child.get_tag()), '')
                    spawn = spawn.replace("@", '')
                    spawn = spawn.replace(" ", '')
                    spawn = spawn.splitlines()
                    spawn = spawn[0]
                    if spawn == family:
                        sameFam = True
                #Get birthday of each child to compare to given birthday
                if child.get_tag() == "BIRT":
                    dates = child.get_child_elements()
                    for d in dates:
                        if d.get_tag() == "DATE":
                            # separate date from rest of the line
                            bday = str(d)[2:].replace(str(d.get_tag()), '')
                            bday = bday.splitlines()
                            bday = bday[0]
                            if bday == birthday:
                                sameBirth = True
            if sameFam and sameBirth and not samePerson:
                multiples = True
                mult.append(id)
        if multiples == True:
            mult.append(ID)
            #check if this set of multiples has already been added to the list (including reversal)
            for m in self.Multiples:
                m.reverse()
                if m == mult:
                    return
            self.Multiples.append(mult)


    #elements at level 1 and deeper
    def child_helper(self,element,ID):
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
                    self.individuals_dict[ID] = name
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
                    #at this point birth day and family are identified
                    spawn = str(child)[2:].replace(str(child.get_tag()), '')
                    spawn = spawn.replace("@", '')
                    spawn = spawn.replace(" ", '')
                    spawn = spawn.splitlines()
                    spawn = spawn[0]
                    sprint1.compareBirthday(birthday,spawn,ID)
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
            self.iTable.add_row([str(ID),name,gender,birthday,age,alive,death,spawn,spouse])


    def family_helper(self,element, fID):
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
            hName = self.individuals_dict.get(hID)
            wName = self.individuals_dict.get(wID)
            self.fTable.add_row([fID,married,divorced,hID,hName,wID,wName,spawns])


    # is element married
    def isMarr(self,element):
        children = element.get_child_elements()
        for child in children:
            if child.get_tag() == "FAMS": # is the individual the spouse in a family
                return True
        return False

    #is element dead
    def isDead(self,element):
        children = element.get_child_elements()
        for child in children:
            if child.get_tag() == "DEAT":
                return True
        return False

    
    #Start parsing the file
    def parse(self):
        root_child_elements = gedcom_parser.get_root_child_elements()
        #elements at level 0
        for element in root_child_elements:
            if element.get_level() == 0:
                if element.get_tag() == "INDI":
                    married = sprint1.isMarr(element) # returns true if married, false if not
                    dead = sprint1.isDead(element) # returns true if dead, false if not
                    ID = str(element)[2:].replace(str(element.get_tag()), '')
                    ID = ID.replace("@", '')
                    ID = ID.replace(" ", '')
                    ID = ID.splitlines()
                    ID = ID[0]
                    if married == False and dead == False:
                        self.Singles.append(ID)
                        self.Singles_elem.append(element)
                    sprint1.child_helper(element,ID)
                
                if element.get_tag() == "FAM":
                    fID = str(element)[2:].replace(str(element.get_tag()), '')
                    fID = fID.replace("@", '')
                    fID = fID.replace(" ", '')
                    fID = fID.splitlines()
                    fID = fID[0]
                    sprint1.family_helper(element,fID)
    
    def getSingles(self):
        return self.Singles
    
    def getSinglesElem(self):
        return self.Singles_elem

    def getMultipleBirths(self):
        return self.Multiples



sprint1 = Sprint1()

    # Initialize the parser
gedcom_parser = Parser()

    # Get the file name from the user
print("Welcome to the GEDCOM file reader!\nType EXIT to exit the program.")

    # Find the file and parse it
while True:
    file_name = input("Please enter the name of the GEDCOM file to be processed: ")
    if file_name == "EXIT":
        print("Exiting program.")
        exit()
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        gedcom_parser.parse_file(file_path)
        break
    except:
        print("File not found. Please try again.")
    
sprint1.parse()

stdout_fileno = sys.stdout # Save the file descriptor for stdout

    # Open a file called "output.txt" for writing.
    # If the file cannot be opened, print an error message and terminate the program.
try:
    sys.stdout = open("output.txt", 'w')
except FileNotFoundError:
    print("File not found. Please try again.")
    exit(0)


print("Individual")
print(sprint1.iTable)

print("Families")
print(sprint1.fTable)

print("Individuals over 30 who have never been married", sprint1.getSingles())

print("Individuals who were born at the same time", sprint1.getMultipleBirths())

sys.stdout.close()

# Reset stdout to the original file descriptor
sys.stdout = stdout_fileno