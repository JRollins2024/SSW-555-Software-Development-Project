import unittest

#import Class I want to test
import ged_parser


class Test(unittest.TestCase):

    sprint = ged_parser.Sprint1() #instantiates the Sprint1Class

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
        expected = ['I1', 'I4', 'I8', 'I13', 'I15']

        #check that the actual matched the expected output
        self.assertEqual(actual, expected)
        print("Expected: " + str(expected))
        print("Actual: " + str(actual),end="\n\n")


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
            for i in sg:
                self.assertEqual(self.sprint.getBirthDate(i), self.sprint.getBirthDate(sg[i+1]))

        print("Finished testing: Multiples_Birthday",end="\n\n")

# Test that all individuals in the list are actually siblings
    def test_3_Multiples_Siblings(self):
        print("Starting to test: Multiples_Siblings",end="\n\n")

        # get output from class
        actual = self.sprint.getMultipleBirthsElem()

        # iterate through each sibling group
        for sg in actual[:-1]:
            # iterate through each sibling in the group
            for i in sg:
                # and assert that each one is a sibling of the next individual by seeing they are both children of the same family
                self.assertEqual(self.sprint.getChildFamily(i), self.sprint.getChildFamily(sg[i+1]))
                
        print("Finished testing: Multiples_Siblings",end="\n\n")


    # Test that all siblings who have the same birthday are listed in a list of lists
    def test_4_Multiples(self):
        print("Starting to test: Multiples",end="\n\n")

        # Get the actual output from the class
        actual = self.sprint.getMultipleBirths()

        # Expected output from class
        expected = [['I1', 'I4']]

        # Assert that actual matches expected output
        self.assertEqual(actual, expected)
        print("Expected: " + str(expected))
        print("Actual: " + str(actual), end="\n\n")

        print("Finished testing: Multiples",end="\n\n")

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
