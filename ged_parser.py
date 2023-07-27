#Jamie Rollins, Dominick Varano, David Rocha, Ruchita Paithankar
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
from datetime import date, timedelta
import datetime

class Parser_Class:
    #initialize time
    today = datetime.datetime.now()

    #initialize tables
    fTable = PrettyTable() #table for families
    iTable = PrettyTable() #table for individuals
    iTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    fTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

    #Initialize Dictionaries
    abbMonth_value = {"JAN":1, "FEB":2, "MAR":3, "APR":4,"MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
    month_value = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, 'August':8, "September":9, "October":10, "November":11, "December":12 }

    individuals_dict, individuals_age, is_alive, individuals_deathday = {}, {}, {}, {}
    individual_marriages, individual_births = {}, {}

    # Families List
    Families = [] # will hold the IDs of all families

    #Singles List
    Singles = [] # will hold the IDs of all individuals who are single
    Singles_elem = [] # will hold the full element of all individuals who are single

    #Multiples List
    Multiples = []
    Multiples_elem = []

    #Dead List
    Dead = []
    Dead_elem = []

    #LivingMarried List
    LivingMarried = []
    LivingMarried_elem = []

    #orphans
    orphansUnder18 = []

    #Spouses who are twice the age of their younger spouse
    SpouseTwiceTheAge = []
    
    # People who where born or died in the last 30 days
    recentbirths_list, recentdeaths_list = [], []

    # People who died before they were born
    DiedBeforeBorn = []

    # Marriages that took place after one of the spouses died
    DiedBeforeMarriage = []

    # Divorces that took place after one of the spouses died
    DiedBeforeDivorce = []

    # Wedding anniversary in the next 30 days
    upcomingAnniversaries = []



    # Birthday in the next 30 days
    upcomingBirthdays = []

    # Living spouses and descendants of people who died in the last 30 days
    recentSurvivors = []

    birthAfterMarriage = []

    oldParents = []


    #list of spawns
    checklist = spawnList = []

    #list of couples
    coupleList = []

    #list for recording couples who are sublings
    coupleError = []

    """ 
        Refactored code part 1
    A method to return cleaned up strings of variables so these lines don't have to be repeated
    """
    def cleanString(self, var):
        var = var.replace("@", '')
        var = var.replace(" ", '')
        var = var.splitlines()
        var = var[0]
        return var
    

    def siblingPairUnordered(self):
        return self.checklist 

    def siblingPair(self):
        now = datetime.datetime.now()
        for spawn in self.spawnList:
            if len(spawn) == 1:
                continue
                # age = datetime.datetime.strptime(self.individual_births[spawn[0]].strip(), '%d %b %Y')
                # print(spawn,'-',age)
            else: 
                age1 = now - datetime.datetime.strptime(self.individual_births[spawn[0]].strip(), '%d %b %Y')
                age2 = now - datetime.datetime.strptime(self.individual_births[spawn[1]].strip(), '%d %b %Y')
                if age2 > age1:
                    spawn[0],spawn[1] = spawn[1],spawn[0]
        return self.spawnList


    def marriedSiblings(self):
        for siblings in self.checklist:
            if siblings in self.coupleList:
                self.coupleError.append(siblings)

        return self.coupleError



    def MarriageBeforeBirth(self):
        for i in self.individual_marriages:
            if i in self.individual_births and self.individual_marriages[i]!='NA' and self.individual_births[i]!='NA':
                # print("Birth date:",self.individual_births[i], "   Marriage Date:",self.individual_marriages[i])
                marriageDate = datetime.datetime.strptime(self.individual_marriages[i].strip(), '%d %b %Y')
                birthdate = datetime.datetime.strptime(self.individual_births[i].strip(), '%d %b %Y')
                if birthdate > marriageDate:
                    self.birthAfterMarriage.append(i) 

        return self.birthAfterMarriage

        # print("ERROR: Individuals married before being born", self.birthAfterMarriage)


    def parentsTooOld(self, hID, wID, spawns):
        now = datetime.datetime.now()
        if self.individual_births[hID] !='NA' and self.individual_births[wID] !='NA':
            fatherBirth = datetime.datetime.strptime(self.individual_births[hID].strip(), '%d %b %Y')
            motherBirth = datetime.datetime.strptime(self.individual_births[wID].strip(), '%d %b %Y')
            for spawn in spawns:
                spawnBirth = datetime.datetime.strptime(self.individual_births[spawn].strip(), '%d %b %Y')

                ageDiffDad = now.year - fatherBirth.year - ((now.month, now.day) < (fatherBirth.month, fatherBirth.day)) - (now.year - spawnBirth.year - ((now.month, now.day) < (spawnBirth.month, spawnBirth.day)))
                ageDiffMom = now.year - motherBirth.year - ((now.month, now.day) < (motherBirth.month, motherBirth.day)) - (now.year - spawnBirth.year - ((now.month, now.day) < (spawnBirth.month, spawnBirth.day)))
                    # ageDiffDad = fatherBirth - spawnBirth
                    # ageDiffMom = motherBirth - spawnBirth
                if ageDiffDad > 79 and ageDiffMom > 59:
                    self.oldParents.append([hID,wID])
                        # self.oldParents.append([hID, wID])
        return self.oldParents

    def ageDifference(self,hID, wID):  
        """ This function returns the couples whose age difference is huge """
        
        ageDifferenceArray = []
        husbandAge  = self.individuals_age.get(hID)
        wifeAge = self.individuals_age.get(wID)
        husbandName = self.individuals_dict.get(hID)
        ages = [husbandAge, wifeAge]
        # print(husbandName, husbandAge)
        if husbandAge and wifeAge and max(ages)/min(ages) > 2:
            husbandName = self.individuals_dict.get(hID)
            wifeName = self.individuals_dict.get(wID)
            ageDifferenceArray.append(hID)
            ageDifferenceArray.append(wID)
        return ageDifferenceArray

    def orphans(self, hID, wID, chil):
        
        aliveFather = self.is_alive.get(hID)
        aliveMother = self.is_alive.get(wID)
        orphanChild = ""
        if (aliveFather == 'False' or aliveFather == None) and (aliveMother == 'False' or aliveMother == None) and self.individuals_age.get(chil):
            if self.individuals_age.get(chil) < 18:
                orphanChild = chil
                self.orphansUnder18.append(chil)
        return orphanChild

    def UniqueIndividualID(self, id):
        """ This function checks that before an individual is added to a dictionary it's ID is not already in it """
        takenIDs = list(self.individuals_dict.keys())
        if id in takenIDs:
            return False # this ID has already been used by another individual
        else:
            return True
    
    def UniqueFamilyID(self, id):
        """ This function checks that before a family is added to a dictionary it's ID is not already in it """
        
        if id in Families:
            return False
        else:
            return True

    #compare each individual's birthday and famc to every other individual's birthday and famc
    def compareBirthday(self,birthday, family, ID):
        mult = []
        mult_elem = []
        multiples = False
        for e in gedcom_parser.get_root_child_elements():
            sameFam = False
            sameBirth = False
            samePerson = False
            #Get thid id of the individual you are comparing the given one to
            if e.get_tag() == "INDI":
                id = str(e)[2:].replace(str(e.get_tag()), '')
                id = sprint1.cleanString(id)
                if ID == id:
                    samePerson = True
            children = e.get_child_elements()
            for child in children:
                #Make sure siblings are children in the same family
                if child.get_tag() == "FAMC":
                    spawn = str(child)[2:].replace(str(child.get_tag()), '')
                    spawn = sprint1.cleanString(spawn)
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
                mult_elem.append(e)
        if multiples == True:
            mult.append(ID)
            #check if this set of multiples has already been added to the list (including reversal)
            for m in self.Multiples:
                m.reverse()
                if m == mult:
                    return
            self.Multiples.append(mult)
            self.Multiples_elem.append(mult_elem)


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
                    # Check that ID is not already in individuals_dict
                    if self.UniqueID(ID): # if not taken, then this returns true
                        self.individuals_dict[ID] = name
                    else:
                        print("ERROR: ID already taken")
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
                            self.individuals_deathday[ID] = death
                self.is_alive[ID]=alive
                # This individual is the child of the this family ID
                if child.get_tag() == "FAMC":
                    #at this point birth day and family are identified
                    spawn = str(child)[2:].replace(str(child.get_tag()), '')
                    spawn = sprint1.cleanString(spawn)
                    sprint1.compareBirthday(birthday,spawn,ID)
                # This individual is the spouse of this family ID
                if child.get_tag() == "FAMS":
                    spouse = str(child)[2:].replace(str(child.get_tag()), '')
                    spouse = sprint1.cleanString(spouse)
            # If the individual is NOT dead subtract birth year from current year
            if death != "NA":
                age = int(death_year) - int(birth_year)
            else:
                # Else subtract from the year of death
                age = 2023 - int(birth_year)
            self.individuals_age[ID] = age
            self.individual_births[ID] = birthday
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
        mday = "NA"
        dday = "NA"
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
                            married = married[0] # marriage date
                            # make sure marriage takes place before death of either spouse
                            mday = date(int(married[-4:]), self.abbMonth_value[married.split(" ")[2]], int(married.split(" ")[1]))
                if child.get_tag() == "DIV":
                    #go down to level 2
                    dates = child.get_child_elements()
                    for d in dates:
                        if d.get_tag() == "DATE":
                            divorced = str(d)[2:].replace(str(d.get_tag()), '')
                            divorced = divorced.splitlines()
                            divorced = divorced[0] # divorce date
                            # make sure divorce takes place before death of either spouse
                            dday = date(int(divorced[-4:]), self.abbMonth_value[divorced.split(" ")[2]], int(divorced.split(" ")[1]))
                if child.get_tag() == "HUSB":
                    #handles getting the husband's ID separated from rest of the line
                    hID = str(child)[2:].replace(str(child.get_tag()), '')
                    hID = sprint1.cleanString(hID)
                if child.get_tag() == "WIFE":
                    #handles getting the wife's ID separated from rest of the line
                    wID = str(child)[2:].replace(str(child.get_tag()), '')
                    wID = sprint1.cleanString(wID)
                    ageDifferenceVar = self.ageDifference(hID, wID)
                    if ageDifferenceVar:
                        self.SpouseTwiceTheAge.append(ageDifferenceVar)
                if child.get_tag() == "CHIL":
                    #Append all children's IDs to list
                    chil = str(child)[2:].replace(str(child.get_tag()), '')
                    chil = sprint1.cleanString(chil)
                    spawns.append(chil)
                    self.orphans(hID, wID, chil)
            #look up husband and wife IDs in dictionary
            hName = self.individuals_dict.get(hID)
            wName = self.individuals_dict.get(wID)
            #if list is not empty then append to spawn list
            if len(spawns) != 0: self.spawnList.append(spawns)
            self.fTable.add_row([fID,married,divorced,hID,hName,wID,wName,spawns])

            # Check that husband and wife are married before either of them die
            if hID in self.individuals_deathday:
                # Husband's death
                death = self.individuals_deathday.get(hID)
                h_dday = date(int(death[-4:]), self.abbMonth_value[death.split(" ")[2]], int(death.split(" ")[1]))

                # Wedding day
                if mday != "NA":
                    if mday > h_dday:
                        self.DiedBeforeMarriage.append(hID)
                
                
                # Divorce day
                if dday != "NA":
                    if dday > h_dday:
                        self.DiedBeforeDivorce.append(hID)

                # If husband died recently, put wife and children in recentSurvivors if they're alive
                if hID in self.recentdeaths_list:
                    # Put wife in recentSurvivors, if she's alive
                    if wID not in self.individuals_deathday:
                        self.recentSurvivors.append(wID)
                    
                    # If there are any children in the family and they're alive, put them in recentSurvivors
                    if len(spawns) > 0:
                        for child in spawns:
                            if child not in self.individuals_deathday:
                                self.recentSurvivors.append(child)
                        
            if wID in self.individuals_deathday:
                # Wife's death
                death = self.individuals_deathday.get(wID)
                w_dday = date(int(death[-4:]), self.abbMonth_value[death.split(" ")[2]], int(death.split(" ")[1]))

                # Wedding day
                if mday != "NA":
                    if mday > w_dday:
                        self.DiedBeforeMarriage.append(wID)

                # Divorce day
                if dday != "NA":
                    if dday > w_dday:
                        self.DiedBeforeDivorce.append(wID)
            if hID != 'NA' and wID !='NA': 
                self.parentsTooOld(hID, wID, spawns)
            if hID != 'NA' and married!='NA':self.individual_marriages[hID] = married
            if wID != 'NA' and married!='NA':self.individual_marriages[wID] = married 

            # If wife died recently, put husband and children in recentSurvivors if they're alive
            # Put husband in recentSurvivors, if he's alive
            if wID in self.recentdeaths_list:
                if hID not in self.individuals_deathday:
                    self.recentSurvivors.append(hID)
                
                # If there are any children in the family and they're alive, put them in recentSurvivors
                if len(spawns) > 0:
                    for child in spawns:
                        if child not in self.individuals_deathday and child not in self.recentSurvivors:
                            self.recentSurvivors.append(child)                

            if wID not in self.individuals_deathday and hID not in self.individuals_deathday:
                deadline=datetime.datetime.today()+timedelta(days=30)
                deadlineYear = deadline.strftime("%Y")
                deadlineMonth = deadline.strftime("%m")
                deadlineDay = deadline.strftime("%d")
                deadline = date(int(deadlineYear), int(deadlineMonth), int(deadlineDay))
                if mday.replace(year=int(deadlineYear)) > deadline:
                    self.upcomingAnniversaries.append((wID,hID))



    def isRecentlyBorn(self,element):
        children = element.get_child_elements()
        for child in children:
            if child.get_tag() == "BIRT": # birthday!
                d = child.get_child_elements()
                for x in d:
                    if x.get_tag() == "DATE":
                        #get individuals birthday
                        birthday = str(x)[2:].replace(str(x.get_tag()), '')
                        birthday = birthday.splitlines()
                        birthday = birthday[0] #EX: 10 JAN 2002
                        bday = date(int(birthday[-4:]), self.abbMonth_value[birthday.split(" ")[2]], int(birthday.split(" ")[1]))

                        todayYear  = self.today.year
                        todayMonth = self.today.month
                        todayDay   = self.today.day
                        date_today = date(todayYear, todayMonth, todayDay)
                        no_of_days = timedelta(days=30) # Create a delta of Thirty Days 
                        
                        #before_thirty_days = date_today - no_of_days # Use Delta for Past Date
                        #print('Before Thirty Days:', before_thirty_days)
                        if((date_today - bday).days < 30):
                            return True
        return False

    # is element recent dead
    def isRecentlyDead(self,element):
        children = element.get_child_elements()
        for child in children:
            if child.get_tag() == "DEAT": # is the individual dead
                d = child.get_child_elements()
                for x in d:
                    if x.get_tag() == "DATE":
                        #get individuals birthday
                        deathday = str(x)[2:].replace(str(x.get_tag()), '')
                        deathday = deathday.splitlines()
                        deathday = deathday[0] #EX: 10 JAN 2002
                        dday = date(int(deathday[-4:]), self.abbMonth_value[deathday.split(" ")[2]], int(deathday.split(" ")[1]))

                        #date_today  = today.strftime("%d %B %Y") #EX: June 15 2023
                        date_today = date(2023, 6, 16)
                        no_of_days = timedelta(days=30) # Create a delta of Thirty Days 
                        
                        #before_thirty_days = date_today - no_of_days # Use Delta for Past Date
                        #print('Before Thirty Days:', before_thirty_days)
                        if((date_today - dday).days < 30):
                            return True
        return False

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
    
    # Check that the individual has a birthday in the next 30 days
    def isUpcomingBirthday(self, element):
        children = element.get_child_elements()
        for child in children:
            if child.get_tag() == 'BIRT':
                d = child.get_child_elements()
                for x in d:
                    if x.get_tag() == 'DATE':
                        birthday = str(x)[2:].replace(str(x.get_tag()), '')
                        birthday = birthday.splitlines()
                        birthday = birthday[0]
                        todayYear  = self.today.year
                        bday = date(todayYear, self.abbMonth_value[birthday.split(" ")[2]], int(birthday.split(" ")[1]))

                        # date for today
                        todayYear  = self.today.year
                        todayMonth = self.today.month
                        todayDay   = self.today.day
                        date_today = date(todayYear, todayMonth, todayDay)

                        # See if bday falls within 30 days
                        no_of_days = timedelta(days=30) # Create a delta of Thirty Days
                        if((bday - date_today).days < 30 and (bday - date_today).days > 0):
                            return True
        return False

    # Check that individual dies AFTER they are born
    def checkDeadAfterBirth(self, element):
        ID = str(element)[2:].replace(str(element.get_tag()), '')
        ID = sprint1.cleanString(ID)
        if self.isDead(element):
            children = element.get_child_elements()
            for child in children:
                if child.get_tag() == "BIRT":
                    #compare death date to birthday
                    d = child.get_child_elements()
                    for x in d:
                        if x.get_tag() == "DATE":
                            birthday = str(x)[2:].replace(str(x.get_tag()), '')
                            birthday = birthday.splitlines()
                            birthday = birthday[0] #EX: 10 JAN 2002
                            bday = date(int(birthday[-4:]), self.abbMonth_value[birthday.split(" ")[2]], int(birthday.split(" ")[1]))
                elif child.get_tag() == "DEAT":
                    d = child.get_child_elements()
                    for x in d:
                        if x.get_tag() == "DATE":
                            deathday = str(x)[2:].replace(str(x.get_tag()), '')
                            deathday = deathday.splitlines()
                            deathday = deathday[0]
                            dday = date(int(deathday[-4:]), self.abbMonth_value[deathday.split(" ")[2]], int(deathday.split(" ")[1]))
            
            if dday < bday:
                # Add id birth before death list
                self.DiedBeforeBorn.append(ID)

    
    #Start parsing the file
    def parse(self):
        root_child_elements = gedcom_parser.get_root_child_elements()
        #elements at level 0
        for element in root_child_elements:
            if element.get_level() == 0:
                if element.get_tag() == "INDI":
                    married = sprint1.isMarr(element) # returns true if married, false if not
                    dead = sprint1.isDead(element) # returns true if dead, false if not
                    recently_born = sprint1.isRecentlyBorn(element) # returns true if recently born, false if not
                    recently_dead = sprint1.isRecentlyDead(element) # returns true if recently dead, false if not
                    upcoming_birthday = sprint1.isUpcomingBirthday(element) # returns true if upcoming birthday, false if not
                    ID = str(element)[2:].replace(str(element.get_tag()), '')
                    ID = sprint1.cleanString(ID)

                    if married and not dead:
                        self.LivingMarried.append(ID)
                        self.LivingMarried_elem.append(element)
                    if dead:
                        self.Dead.append(ID)
                        self.Dead_elem.append(element)
                    if married == False and dead == False:
                        self.Singles.append(ID)
                        self.Singles_elem.append(element)
                    if recently_born:
                # Add the ID to the recently born list
                        self.recentbirths_list.append(ID)
                    if recently_dead:
                # Add the ID to the recently dead list
                        self.recentdeaths_list.append(ID)
                    if upcoming_birthday:
                # Add the ID to the upcoming birthday list
                        self.upcomingBirthdays.append(ID)

                # Add the ID to the list of all people who died before they were born
                    self.checkDeadAfterBirth(element)

                    sprint1.child_helper(element,ID)
                
                
                if element.get_tag() == "FAM":
                    fID = str(element)[2:].replace(str(element.get_tag()), '')
                    fID = sprint1.cleanString(fID)
                    if self.UniqueFamilyID(fID):
                        self.Families.append(fID)
                    sprint1.family_helper(element,fID)
    
    def getBirthDates(self,element):
        children = element.get_child_elements()
        birthday = ""
        for child in children:
            if child.get_tag() == "BIRT":
                dates = child.get_child_elements()
                for d in dates:
                    if d.get_tag() == "DATE":
                        birthday = str(d)[2:].replace(str(d.get_tag()), '')
                        birthday = birthday.splitlines()
                        birthday = birthday[0]
                        return birthday
        return birthday

    def getChildFamily(self,element):
        children = element.get_child_elements()
        famc = ""
        for child in children:
            if child.get_tag() == "FAMC":
                famc = str(child)[2:].replace(str(child.get_tag()), '')
                famc = sprint1.cleanString(famc)
                return famc
        return famc
    
    def getSingles(self):
        return self.Singles
    
    def getSinglesElem(self):
        return self.Singles_elem

    def getMultipleBirths(self):
        return self.Multiples

    def getMultipleBirthsElem(self):
        return self.Multiples_elem
    
    def getLivingMarried(self):
        return self.LivingMarried
    
    def getLivingMarriedElem(self):
        return self.LivingMarried_elem
    
    def getDead(self):
        return self.Dead
    
    def getDeadElem(self):
        return self.Dead_elem
    
    def getMultipleOrphans(self):
        return self.orphansUnder18
    
    def getMultipleSpouseTwiceAge(self):
        return self.SpouseTwiceTheAge

    def getUpcomingAnniversaries(self):
        return self.upcomingAnniversaries
    
    def getUpcomingBirthdays(self):
        return self.upcomingBirthdays
    
    def getRecentSurvivors(self):
        return self.recentSurvivors


sprint1 = Parser_Class()

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

print("Individuals over 30 who have never been married:")
for i in sprint1.getSingles():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Individuals who were born at the same time:")
for i in sprint1.getMultipleBirths():
    print(i[0] + "(" + str(sprint1.individuals_age.get(i[0])) + ")" + " and " + i[1] + "(" + str(sprint1.individuals_age.get(i[1])) + ")")


print("Recent Births:")
for i in sprint1.recentbirths_list:
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Recent Deaths:")
for i in sprint1.recentdeaths_list:
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Individuals who are married:")
for i in sprint1.getLivingMarried():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Individuals who are dead:")
for i in sprint1.getDead():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Orphaned children (both parents dead and child < 18 years old) in a GEDCOM file:")
for i in sprint1.getMultipleOrphans():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Couples who were married when the older spouse was more than twice as old as the younger spouse:")
for i in sprint1.getMultipleSpouseTwiceAge():
    print(i[0] + "(" + str(sprint1.individuals_age.get(i[0])) + ")" + " and " + i[1] + "(" + str(sprint1.individuals_age.get(i[1])) + ")")

print("Living couples whose anniversaries are within the next 30 days:")
for i in sprint1.getUpcomingAnniversaries():
    print(i[0] + "(" + str(sprint1.individuals_age.get(i[0])) + ")" + " and " + i[1] + "(" + str(sprint1.individuals_age.get(i[1])) + ")")

print("Individuals whose birthdays occur in the next 30 days:")
if len(sprint1.getUpcomingBirthdays()) == 0:
    print("None")
for i in sprint1.getUpcomingBirthdays():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

print("Recent survivors of a deceased family member:")
if len(sprint1.getRecentSurvivors()) == 0:
    print("None")
for i in sprint1.getRecentSurvivors():
    print(i + "(" + str(sprint1.individuals_age.get(i)) + ")")

for i in sprint1.DiedBeforeBorn:
    print("Error: Individual " + i + "(" + str(sprint1.individuals_age.get(i)) + ")" + " DIED BEFORE THEY WERE BORN.")

for i in sprint1.DiedBeforeMarriage:
    print("Error: Individual " + i + "(" + str(sprint1.individuals_age.get(i)) + ")" + " DIED BEFORE THEY WERE MARRIED.")

for i in sprint1.DiedBeforeDivorce:
    print("Error: Individual " + i + "(" + str(sprint1.individuals_age.get(i)) + ")" + " DIED BEFORE THEY WERE DIVORCED.")

print("Mother is more than 60 years old and father is more than 80 years older than his children ", sprint1.oldParents)

print("Individuals married before birth", sprint1.MarriageBeforeBirth())

print("Ordered siblings by age: ",sprint1.siblingPair())

print("Siblings that are married: ",sprint1.marriedSiblings())

sys.stdout.close()

# Reset stdout to the original file descriptor
sys.stdout = stdout_fileno