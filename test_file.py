import unittest

#import Class I want to test
import ged_parser
import sys


class Test(unittest.TestCase):

    sprint = ged_parser.Parser_Class() #instantiates the Sprint1Class

################## USER STORY: List living single ##################

    '''Test that the amount of individuals listed do not exceed the amount of individuals in the gedcom file'''
    def test_0_Singles_Size(self):
        print("Starting to test: Singles_Size",end="\n\n")

        # get actual output from class
        actual = self.sprint.getSingles()

        #get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list does not exceed the amount of individuals in the gedcom file
        self.assertTrue(len(actual) <= len(indi))
        print("Number of total individuals: " + str(len(indi)))
        print("Number of singles: " + str(len(actual)), end="\n\n")        

        print("Finished testing: Singles_Size",end="\n\n")


    '''Test that the amount of individuals listed is not less than 0'''
    def test_1_Singles_Size2(self):
        print("Starting to test: Singles_Size2",end="\n\n")

        # get actual output from class
        actual = self.sprint.getSingles()

        #get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list does not exceed the amount of individuals in the gedcom file
        self.assertTrue(len(actual) >= 0)
        print("Number of singles: " + str(len(actual)), end="\n\n")
        
        print("Finished testing: Singles_Size2",end="\n\n")


    '''Test that all individuals listed are single'''
    #TODO
    def test_2_Singles(self):
        print("Starting to test: Singles",end="\n\n")

        # Get actual output from class
        actual = self.sprint.getSinglesElem()

        # iterate through each element in the list
        for i in actual:
            # and assert that each one returns false
            self.assertFalse(self.sprint.isMarr(i))

        # An indiviudal counts as single if they do not have the tag 'FAMS'
        

        print("Finished testing: Singles",end="\n\n")


    '''Test that all individuals listed are living'''
    #TODO
    def test_3_Singles_Alive(self):
        print("Starting to test: Singles_Alive",end="\n\n")
        
        # Get the return list of individuals listed
        actual = self.sprint.getSinglesElem()

        # iterate through each element in the list
        for i in actual:
            # and assert that each one returns False when checking if they are dead
            self.assertFalse(self.sprint.isDead(i))
        print("Finished testing: Singles_Alive",end="\n\n")


    '''Test that all individuals listed match the expected output'''
    #TODO
    def test_4_Singles_Value(self):
        print("Starting to test: Singles_Value",end="\n\n")

        # get actual output from class
        actual = self.sprint.getSingles()

        # expected output
        expected = ['I4', 'I8', 'I22', 'I23', 'I24', 'I25', 'I28', 'I29', 'I30', 'I31', 'I32', 'I33', 'I34', 'I35', 'I36', 'I37', 'I38', 'I39', 'I40', 'I41', 'I42']

        print("Expected: " + str(expected))
        print("Actual: " + str(actual),end="\n\n")

        #check that the actual matched the expected output
        self.assertEqual(actual, expected)
        


################### USER STORY: List multiple births ##################

    # Test that the amount of siblings who have the same birthday do not exceed the amount of individuals in the gedcom file
    def test_0_Multiples_Size(self):
        print("Starting to test: Multiples_Size",end="\n\n")

        # get actual output from class
        actual = self.sprint.getMultipleBirths()

        # get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        self.assertTrue(len(actual) <= len(indi))
        print("Number of total individuals: " + str(len(indi)))
        print("Number of multiple births: " + str(len(actual)), end="\n\n") 

        print("Finished testing: Multiples_Size",end="\n\n")

# Test that the amount of siblings who have the same birthday is not less than 0
    def test_1_Multiples_Size2(self):
        print("Starting to test: Multiples_Size2",end="\n\n")

        # get actual output from class
        actual = self.sprint.getMultipleBirths()

        # get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        self.assertTrue(len(actual) >= 0)
        print("Number of singles: " + str(len(actual)), end="\n\n")

        print("Finished testing: Multiples_Size2",end="\n\n")


# Test that all siblings in a group have the same birthday
    def test_2_Multiples_Birthday(self):
        print("Starting to test: Multiples_Birthday",end="\n\n")

        # get actual output from class
        actual = self.sprint.getMultipleBirthsElem()
        # iterate through each sibling group
        for sg in actual[:-1]:
            # check that the surrent individual has the same birthday as the next individual
            for i in range(len(sg)):
                if i != len(sg)-1:
                    self.assertEqual(self.sprint.getBirthDates(sg[i]), self.sprint.getBirthDates(sg[i+1]))

        print("Finished testing: Multiples_Birthday",end="\n\n")

# Test that all individuals in the list are actually siblings
    def test_3_Multiples_Siblings(self):
        print("Starting to test: Multiples_Siblings",end="\n\n")

        # get output from class
        actual = self.sprint.getMultipleBirthsElem()

        # iterate through each sibling group
        for sg in actual[:-1]:
            # iterate through each sibling in the group
            for i in range(len(sg)):
                # and assert that each one is a sibling of the next individual by seeing they are both children of the same family
                if i != len(sg)-1:
                    self.assertEqual(self.sprint.getChildFamily(sg[i]), self.sprint.getChildFamily(sg[i+1]))
                
        print("Finished testing: Multiples_Siblings",end="\n\n")


    # Test that all siblings who have the same birthday are listed in a list of lists
    def test_4_Multiples(self):
        print("Starting to test: Multiples",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getMultipleBirths()

        # Expected output from class
        expected = [['I1','I4'],['I24','I25'], ['I29','I30'], ['I31','I33'],['I35','I36'],['I38','I39'],['I40','I41']]
        print("Expected: " + str(expected))
        print("Actual: " + str(actual), end="\n\n")
        # Assert that actual matches expected output
        self.assertEqual(actual, expected)
        

        print("Finished testing: Multiples",end="\n\n")


################### USER STORY: List all deceased ##################

    '''Test that the amount of individuals listed do not exceed the amount of individuals in the gedcom file'''
    def test_0_Deceased_Size(self):
        print("Starting to test: Deceased_Size",end="\n\n")

        # Get actual output from class
        actual = self.sprint.getDead()

        # Get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list does not exceed the amount of individuals in the gedcom file
        self.assertTrue(len(actual) <= len(indi))
        print("Number of total individuals: " + str(len(indi)))
        print("Number of deceased: " + str(len(actual)), end="\n\n")

        print("Finished testing: Deceased_Size",end="\n\n")

    '''Test that the amount of individuals listed is not less than 0'''
    def test_1_Deceased_Size2(self):
        print("Starting to test: Deceased_Size2",end="\n\n")

        # Get actual output from class
        actual = self.sprint.getDead()

        # Get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list is not less than 0
        self.assertTrue(len(actual) >= 0)
        print("Number of deceased: " + str(len(actual)), end="\n\n")

        print("Finished testing: Deceased_Size2",end="\n\n")


    '''Test that all individuals in the list are actually deceased'''
    def test_2_Deceased_Dead(self):
        print("Starting to test: Deceased_Dead",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getDeadElem()

        # iterate through each individual in the list
        for i in actual:
            # and assert that each one is deceased
            self.assertTrue(self.sprint.isDead(i))

        print("Finished testing: Deceased_Dead",end="\n\n")

    # Test that all individuals in the list are actually individuals
    def test_3_Deceased_Individual(self):
        print("Starting to test: Deceased_Individual",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getDead()
        individuals = self.sprint.individuals_dict.keys()
        
        # Check if each individual exists as a key in the individuals dictionary
        for i in actual:
            self.assertTrue(i in individuals)
    
        print("Finished testing: Deceased_Individual",end="\n\n")


    '''Test that all individuals listed match the expected output'''
    def test_4_Deceased_Value(self):
        print("Starting to test: Deceased_Value",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getDead()

        # Expected output from class
        expected = ['I5', 'I7', 'I15', 'I16', 'I17', 'I18']

        # Assert that actual matches expected output
        self.assertEqual(actual, expected)
        print("Expected: " + str(expected))
        print("Actual: " + str(actual), end="\n\n")

        print("Finished testing: Deceased_Value",end="\n\n")


################### USER STORY: List living married ##################

    '''Test that the amount of individuals listed do not exceed the amount of individuals in the gedcom file'''
    def test_0_LivingMarried_Size(self):
        print("Starting to test: LivingMarried_Size",end="\n\n")

        # Get actual output from class
        actual = self.sprint.getLivingMarried()

        # Get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list does not exceed the amount of individuals in the gedcom file
        self.assertTrue(len(actual) <= len(indi))
        print("Number of total individuals: " + str(len(indi)))
        print("Number of living married: " + str(len(actual)), end="\n\n")

        print("Finished testing: LivingMarried_Size",end="\n\n")

    '''Test that the amount of individuals listed is not less than 0'''
    def test_1_LivingMarried_Size2(self):
        print("Starting to test: LivingMarried_Size2",end="\n\n")

        # Get actual output from class
        actual = self.sprint.getLivingMarried()

        # Get all the individuals in the gedcom file
        indi = self.sprint.individuals_dict

        #check that the list is not less than 0
        self.assertTrue(len(actual) >= 0)
        print("Number of living married: " + str(len(actual)), end="\n\n")

        print("Finished testing: LivingMarried_Size2",end="\n\n")
        

    '''Test that all individuals in the list are actually living'''
    def test_2_LivingMarried_Alive(self):
        print("Starting to test: LivingMarried_Alive",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getLivingMarriedElem()

        # iterate through each individual in the list
        for i in actual:
            # and assert that each one is living
            self.assertFalse(self.sprint.isDead(i))
        
        print("Finished testing: LivingMarried_Alive",end="\n\n")
        
    '''Test that all individuals in the list are married'''
    def test_3_LivingMarried_Married(self):
        print("Starting to test: LivingMarried_Married",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getLivingMarriedElem()

        # iterate through each individual in the list
        for i in actual:
            # and assert that each one is married
            self.assertTrue(self.sprint.isMarr(i))

        print("Finished testing: LivingMarried_Married",end="\n\n")

    '''Test that all individuals listed match the expected output'''

    def test_4_LivingMarried_Value(self):
        print("Starting to test: LivingMarried_Value",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getLivingMarried()

        # Expected output from class
        expected = ['I1', 'I2', 'I3', 'I6', 'I9', 'I10', 'I11', 'I12', 'I13', 'I14', 'I19', 'I20', 'I21', 'I26', 'I27']

        # Assert that actual matches expected output
        self.assertEqual(actual, expected)
        print("Expected: " + str(expected))
        print("Actual: " + str(actual), end="\n\n")

        print("Finished testing: LivingMarried_Value",end="\n\n")

    def test_1_ageDifference(self):
        print("Starting to test: Couples age difference 1",end="\n\n")
        indi = self.sprint.getMultipleSpouseTwiceAge()
        self.assertEqual(indi,[['I5', 'I6'], ['I7', 'I6']])
        
        print("Expected:", indi)
        print("Actual:",[['I5', 'I6'], ['I7', 'I6']])
        print("Finished testing: couples",end="\n\n")

    def test_2_ageDifference(self):
        print("Starting to test: Couples age difference 2",end="\n\n")
        indi = self.sprint.getMultipleSpouseTwiceAge()
        self.assertNotEqual(indi,[['I9', 'I10'], ['I7', 'I6']])
        
        print("Expected:", indi)
        print("Actual:",[['I9', 'I10'], ['I5', 'I6'], ['I7', 'I6']])
        print("Finished testing: couples age difference 2",end="\n\n")


    def test_3_orphans(self):
        print("Starting to test: orphans test 1",end="\n\n")
        orphans = self.sprint.getMultipleOrphans()
        self.assertEqual(orphans,['I8'])

        print("Expected:", orphans)
        print("Actual:",['I8'])
        print("Finished testing: orphans test 1",end="\n\n")

    def test_4_orphans(self):
        print("Starting to test: orphans test 2",end="\n\n")
        orphans = self.sprint.getMultipleOrphans()
        self.assertNotEqual(orphans,['I8','I20'])

        print("Expected:", orphans)
        print("Actual:",['I8'])
        print("Finished testing: orphans test 2",end="\n\n")


    ############### Refactored Code 1 ###############

    # Check that cleanString works as expected
    def test_0_cleanString(self):
        given = "@I12@"
        expected = "I12"
        actual = self.sprint.cleanString(given)
        self.assertEqual(actual, expected)
        print("Expected: " + str(expected))
        print("Actual: " + str(actual))

    ################### User Story: Include ages when listing individuals ##################
    ''' Test that an int is returned'''
    def test_0_returnInt(self):
        print("Starting to test: return int",end="\n\n")

        # Test Individual
        indi = 'I11'

        # Get individual's actual listed age
        actual = self.sprint.individuals_age.get(indi)

        # Check that individual's age is an int
        self.assertTrue(isinstance(actual, int))
        
        print("Finished testing: return int",end="\n\n")

    ''' Test that when given an individual's ID, the correct age is returned '''
    def test_1_correctAge(self):
        print("Starting to test: correct age",end="\n\n")

        # Test Individual
        indi = 'I11'

        # Get individual's actual listed age
        actual = self.sprint.individuals_age.get(indi)

        # Get individual's expected age
        expected = 50

        # Assert that actual and expected match
        self.assertEqual(actual, expected)

        # Print results
        print("Expected: " + str(expected))
        print("Actual: " + str(actual))

        print("Finished testing: correct age",end="\n\n")


################### User Story: Living couples with upcoming anniversaries ##################
    ''' Test that the amount of couples returned does not exceed the amount of couples in the gedcom file'''
    def test_0_amountCouples(self):
        print("Starting to test: amount of couples",end="\n\n")

        # Count the amount of families in the gedcom file
        famCount = len(self.sprint.Families)

        # Count the amount of couples whose anniversary is coming up
        couplesCount = len(self.sprint.getUpcomingAnniversaries())

        # Compare
        self.assertTrue(couplesCount <= famCount)

        # Print results
        print("Number of Families: " + str(famCount))
        print("Number of Couples: " + str(couplesCount))

        print("Finished testing: amount of couples",end="\n\n")


    ''' Test that when given an individual's ID, the correct age is returned '''
    def test_1_upcomingAnniversaries(self):
        print("Starting to test: upcoming anniversaries",end="\n\n")
        anniversaries = self.sprint.getUpcomingAnniversaries()
        expected = [('I3','I2'), ('I26','I27')]

        self.assertEqual(anniversaries, expected)

        print("Expected:", expected)
        print("Actual:", anniversaries)

        print("Finished testing: upcoming anniversaries",end="\n\n")


    def test_1_marriageBeforeBirth(self):
        print(" Starting to test: people who married before birth",end="\n\n")
        peopleBornBeforeMariage = self.sprint.MarriageBeforeBirth()
        res = sorted([*set(peopleBornBeforeMariage)])
        print("Expected:", res)
        print("Actual:",['I1', 'I20'])
        self.assertEqual(res,['I1', 'I19'],'Marriage before birth')
        print("Finished testing: people who married before birth",end="\n\n")


    def test_2_marriageBeforeBirth(self):
        print(" Starting to test: people who did not marry before birth",end="\n\n")
        peopleBornBeforeMariage = self.sprint.MarriageBeforeBirth()
        res = sorted([*set(peopleBornBeforeMariage)])
        print("Expected:", res)
        print("Actual:",['I5'])
        self.assertNotEqual(res,['I5'],'Marriage not before birth')
        print("Finished testing: people who did not marry before birth",end="\n\n")


    def test_1_oldParents(self):
        print(" Starting to test: parents too old",end="\n\n")
        parentsList = self.sprint.parentsTooOld('I9','I10', ['I2'])
        res = parentsList[0]
        print("Expected:",res)
        print("Actual:",[['I9', 'I10']])
        self.assertEqual(res,['I9', 'I10'],'Parents too old')
        print("Finished testing: parents too old",end="\n\n")


    def test_2_oldParents(self):
        print(" Starting to test: parents too old",end="\n\n")
        parentsList = self.sprint.parentsTooOld('I9','I10', ['I2'])
        res = parentsList[0]
        print("Expected:",res)
        print("Actual:",[['I3']])
        self.assertNotEqual(res,['I3'],'Parents too old')
        print("Finished testing: parents too old",end="\n\n")

    def test_5_orphans(self):
        orphans = self.sprint.getMultipleOrphans()
        self.assertNotEqual(orphans,[ ], ' empty')

        print("Starting to test: orphans",end="\n\n")
        print("Expected:", orphans)
        print("Actual:",[['I9', 'I10'], ['I7', 'I6']])
        print("Finished testing: orphans",end="\n\n")

################## USER STORY: List upcoming birthdays ##################
    ''' Test for the expected number of birthdays '''
    def test_0_upcomingBirthdays(self):
        print("Starting to test: upcoming birthdays 0",end="\n\n")
        birthdays = self.sprint.getUpcomingBirthdays()

        # This value will actually change within a week, so this test will need to be updated in the near future
        self.assertEqual(len(birthdays), 4)

        print("Expected: 2")
        print("Actual:", len(birthdays))

        print("Finished testing: upcoming birthdays 0",end="\n\n")

    ''' Test for the expected birthdays '''
    def test_1_upcomingBirthdays(self):
        print("Starting to test: upcoming birthdays 1",end="\n\n")
        birthdays = self.sprint.getUpcomingBirthdays()

        # This value will actually change within a week, so this test will need to be updated in the near future
        self.assertEqual(birthdays, ['I10', 'I16', 'I38', 'I39'])

        print("Expected: []")
        print("Actual:", birthdays)

        print("Finished testing: upcoming birthdays 1",end="\n\n")

################## USER STORY: List recent survivors ##################
    ''' Test for the expected number of survivors '''
    def test_0_recentSurvivors(self):
        print("Starting to test: recent survivors 0",end="\n\n")
        survivors = self.sprint.getRecentSurvivors()

        # Will need to update test file to include this
        self.assertEqual(len(survivors), 0)

        print("Expected: 0")
        print("Actual:", len(survivors))

        print("Finished testing: recent survivors 0",end="\n\n")
        
    ''' Test for the expected survivors ''' 
    def test_1_recentSurvivors(self):
        print("Starting to test: recent survivors 1",end="\n\n")
        survivors = self.sprint.getRecentSurvivors()

        # Will need to update test file to include this
        self.assertEqual(survivors, [])

        print("Expected: []")
        print("Actual:", survivors)

        print("Finished testing: recent survivors 1",end="\n\n")
        

################## USER STORY: List siblings in families by decreasing age ##################
    def test_0_siblingList(self):
        siblingListOrdered = self.sprint.siblingPair()
        siblingListUnordered = self.sprint.siblingPairUnordered()
        self.assertEqual(siblingListOrdered,siblingListUnordered,'sibling list is ordered')
        print("Starting to test: siblings",end="\n\n")
        print("Expected:", siblingListOrdered)
        print("Actual:",siblingListUnordered)
        print("Finished testing: siblings",end="\n\n")


    def test_1_siblingList(self):
        siblingListOrdered = self.sprint.siblingPair()
        siblingListUnordered = [[]]
        self.assertNotEqual(siblingListOrdered,siblingListUnordered,'empty list')
        print("Starting to test: siblings",end="\n\n")
        print("Expected:", siblingListOrdered)
        print("Actual:",siblingListUnordered)
        print("Finished testing: siblings",end="\n\n")



################## USER STORY: Siblings should not marry one another ##################

    def test_0_marriedsiblings(self):
        marriedSibling = self.sprint.marriedSiblings()
        emptyList = []
        self.assertEqual(marriedSibling,emptyList,'No such siblings')
        print("Starting to test: married siblings",end="\n\n")
        print("Expected:", marriedSibling)
        print("Actual:",emptyList)
        print("Finished testing: married siblings",end="\n\n")

    def test_1_marriedsiblings(self):
        marriedSibling = self.sprint.marriedSiblings()
        actualSiblings = ['I3', 'I11']
        self.assertNotEqual(marriedSibling,actualSiblings,'siblings')
        print("Starting to test: married siblings",end="\n\n")
        print("Expected:", marriedSibling)
        print("Actual:",actualSiblings)
        print("Finished testing: married siblings",end="\n\n")

################## USER STORY: Unique IDs #########################################################
    ''' Check that a non-negative number of IDs are returned'''
    def test_0_UniqueNonNegative(self):
        print("Starting to test: Unique Non Negative",end="\n\n")
        actual = self.sprint.getDuplicateID()
        self.assertEqual(actual >= 0, True)
        print("Finished testing: Unique Non Negative",end="\n\n")

    ''' Check that number of IDs returned is correct'''
    def test_1_CorrectUniqueIDs(self):
        print("Starting to test: Correct Unique IDs",end="\n\n")
        expected = 0
        actual = self.sprint.getDuplicateID()
        print("Expected: ", expected)
        print("Actual: ", actual)
        self.assertEqual(expected, actual)
        print("Finished testing: Correct Unique IDs",end="\n\n")

################## USER STORY: Fewer than 15 siblings in a family ################## 
    def test_0_fewerThan15Siblings(self):
        print("Starting to test: fewer than 15 siblings 0",end="\n\n")
        expected = 1
        actual = len(self.sprint.getManySib())
        self.assertEqual(expected, actual)
        print("Finished testing: fewer than 15 siblings 0",end="\n\n")          



if __name__ == '__main__':
    # Write test file output to a file 
    try:
        sys.stdout = open("test_results.txt", "w")
    except FileNotFoundError:
        print("File not found. Please try again.")
        exit(0)
    # begin the unittest.main()
    unittest.main()