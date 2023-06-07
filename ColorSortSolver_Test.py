##imports
import unittest

import math
import ColorSortSolver as CSS

class TestMapData(unittest.TestCase):
    

    def test_map_data_with_no_data_values(self):
        CSS.map_data_persistent = []
        self.assertFalse(CSS.map_data("flask")) #test the values before it gets data
        self.assertFalse(CSS.map_data("Flask"))
        self.assertFalse(CSS.map_data("ball"))
        self.assertFalse(CSS.map_data("Balls"))
        
    def test_map_data_with_no_data_type(self):
        self.assertRaises(ValueError, CSS.map_data, "flk") #invalid input
        self.assertRaises(ValueError, CSS.map_data, "bal") 
        self.assertRaises(TypeError, CSS.map_data, [3,5])
        self.assertRaises(TypeError, CSS.map_data, 12)
        
    def test_set_map_data(self):
        CSS.set_map_data(2,5)
        self.assertEqual(CSS.map_data_persistent, [2, 5])
        self.assertEqual(CSS.map_data("Balls"), 5)
        self.assertEqual(CSS.data, [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]])

    def test_set_map_data_errors(self):
        self.assertRaises(ValueError, CSS.set_map_data, -1,5)
        self.assertRaises(ValueError, CSS.set_map_data, -1,-36)
        self.assertRaises(TypeError, CSS.set_map_data, "number")
        self.assertRaises(TypeError, CSS.set_map_data, 1.3 , 7)

    def test_movement(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertFalse(CSS.move(0,1))
        self.assertEqual(CSS.move(0,3), [0,4,3,0])
        self.assertEqual(CSS.data, [["red","red","red","red",0],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],["red",0,0,0,0]])
        self.assertFalse(CSS.move(1,3))
        self.assertEqual(CSS.move(1,3,True), [1,4,3,1])
        self.assertEqual(CSS.data, [["red","red","red","red",0],["blue3","blue3","blue3","blue3",0],[0,0,0,0,0],["red","blue3",0,0,0]])
        CSS.data = [["red","red","red",0,"red"],["blue3","blue3","blue3","blue3","blue3"],["red",0,0,0,0],[0,0,0,0,0]]
        self.assertEqual(CSS.move(0,2), [0,4,2,1])
        self.assertEqual(CSS.data, [["red","red","red",0,0],["blue3","blue3","blue3","blue3","blue3"],["red","red",0,0,0],[0,0,0,0,0]])


    def test_movement_errors(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.move, "test",1)
        self.assertRaises(TypeError, CSS.move, 0,1,2)
        self.assertRaises(ValueError, CSS.move, -1,1)
        self.assertRaises(ValueError, CSS.move, 0,4)

    def test_check_victory(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertTrue(CSS.check_complete())
        CSS.data = [[0,"red","red","red",0],["blue3","blue3","blue3","blue3","blue3"],[0,0,"red",0,0],[0,0,0,"red",0]]
        self.assertEqual(CSS.check_complete(), 3)
        CSS.data = [[0,"red","red","red",0],[0,"blue3","blue3",0,"blue3"],[0,"blue3","red",0,0],[0,"blue3",0,"red",0]]
        self.assertEqual(CSS.check_complete(), 4)

    def test_detect_loop(self):
        CSS.map_data_persistent = [2, 5]
        self.assertEqual(CSS.detect_loop([3,2,0,1,1,0,0,1,1,0]),4)
        self.assertEqual(CSS.detect_loop([0,1,1,0,0,1,1,0]),4)
        self.assertEqual(CSS.detect_loop([0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0]),8)
        self.assertFalse(CSS.detect_loop([]))
        self.assertFalse(CSS.detect_loop([0,1,1,2,2,0]))
        
    def test_detect_loop_errors(self):
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.detect_loop, "list")
        self.assertRaises(TypeError, CSS.detect_loop, 12.5)
        self.assertRaises(TypeError, CSS.detect_loop, [2.4,2.3])
        self.assertRaises(ValueError, CSS.detect_loop, [2,3,4])
        self.assertRaises(ValueError, CSS.detect_loop, [0,1,1,45,45,1,1,0,0,1,1,45,45,1,1,0])

    def test_bouncing(self):
        CSS.map_data_persistent = [2, 5]
        self.assertTrue(CSS.bouncing([0,2,3,1,0,1,1,0]))
        self.assertTrue(CSS.bouncing([0,1,1,0]))
        self.assertTrue(CSS.bouncing([0,1,2,3,1,0]))
        self.assertFalse(CSS.bouncing([0,1,0,1]))
        self.assertFalse(CSS.bouncing([0,1,0,2,1,0]))
        
    def test_bouncing_errors(self):
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.bouncing, "list")
        self.assertRaises(TypeError, CSS.bouncing, 12.5)
        self.assertRaises(TypeError, CSS.bouncing, [2.4,2.3])
        self.assertRaises(ValueError, CSS.bouncing, [2,3,4])
        self.assertRaises(ValueError, CSS.bouncing, [0,1,1,45,45,1,1,0,0,1,1,45,45,1,1,0])

    def test_skipping(self):
        CSS.data = [["red","red","red","blue3",0],["blue3","blue3","blue3","blue3",0],[0,0,0,0,0],["red","red",0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertFalse(CSS.skipping([0,2,1,0])) #the flask it ends in has multiple ball colours (nr 0)
        self.assertFalse(CSS.skipping([1,0]))
        self.assertFalse(CSS.skipping([0,2,2,3])) #the starting flask has no balls (nr 2)
        self.assertFalse(CSS.skipping([2,3]))
        self.assertFalse(CSS.skipping([0,2,1,3])) #the color of the moving ball does not match the filled flask on the end (from nr 1 to nr 3)
        self.assertFalse(CSS.skipping([1,3]))
        self.assertTrue(CSS.skipping([0,2,0,2])) #moving to an empty one while a stack exists (from 0 to 2)
        self.assertTrue(CSS.skipping([0,2]))
        self.assertTrue(CSS.skipping([0,2,1,2])) #moving to an empty one while a stack exists and it gets moved from that stack (from 1 to 2)
        self.assertTrue(CSS.skipping([1,2]))

    def test_skipping_with_gaps(self):
        CSS.data = [["red","red","red","blue3",0],[0,"blue3","blue3","blue3",0],[0,0,0,0,0],[0,"red",0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertFalse(CSS.skipping([0,2,1,0])) #the flask it ends in has multiple ball colours (nr 0)
        self.assertFalse(CSS.skipping([1,0]))
        self.assertFalse(CSS.skipping([0,2,2,3])) #the starting flask has no balls (nr 2)
        self.assertFalse(CSS.skipping([2,3]))
        self.assertFalse(CSS.skipping([0,2,1,3])) #the color of the moving ball does not match the filled flask on the end (from nr 1 to nr 3)
        self.assertFalse(CSS.skipping([1,3]))
        self.assertFalse(CSS.skipping([0,2,0,2])) #moving to an empty one while a stack with gap exists (from 0 to 2)
        self.assertFalse(CSS.skipping([0,2]))
        self.assertFalse(CSS.skipping([0,2,1,2])) #moving to an empty one while a stack with gap exists and it gets moved from that stack (from 1 to 2)
        self.assertFalse(CSS.skipping([1,2]))

        
    def test_skipping_with_multiple_empty_flasks(self):
        CSS.data = [["red","red","red","blue3",0],["blue3","blue3","blue3","blue3",0],[0,0,0,0,0],[0,0,0,0,0],[0,"red",0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [4, 5]
        self.assertFalse(CSS.skipping([0,2,1,0])) #the flask it ends in has multiple ball colours (nr 0)
        self.assertFalse(CSS.skipping([1,0]))
        self.assertFalse(CSS.skipping([0,2,2,3])) #the starting flask has no balls (nr 2)
        self.assertFalse(CSS.skipping([2,3]))
        self.assertFalse(CSS.skipping([0,2,1,4])) #the color of the moving ball does not match the filled flask on the end (from nr 1 to nr 4)
        self.assertFalse(CSS.skipping([1,4]))
        self.assertTrue(CSS.skipping([0,2,0,2])) #moving to an empty one while a stack exists (from 0 to 2)
        self.assertTrue(CSS.skipping([0,2]))
        self.assertTrue(CSS.skipping([0,2,1,2])) #moving to an empty one while a stack exists and it gets moved from that stack (from 1 to 2)
        self.assertTrue(CSS.skipping([1,2]))
        self.assertTrue(CSS.skipping([0,2,1,3])) #moving to a second empty one (nr 3)
        self.assertTrue(CSS.skipping([1,3]))

    def test_skipping_errors(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.skipping, "list")
        self.assertRaises(TypeError, CSS.skipping, 12.5)
        self.assertRaises(TypeError, CSS.skipping, [2.4,2.3])
        self.assertRaises(ValueError, CSS.skipping, [2,3,4])
        self.assertRaises(ValueError, CSS.skipping, [0,1,1,45,45,1,1,0,0,1,1,45,45,1,1,0])

    def test_twice_twice(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [3, 5]
        self.assertFalse(CSS.twice_twice([0,2,1,0]))
        self.assertFalse(CSS.twice_twice([0,2]))
        self.assertTrue(CSS.twice_twice([0,1,1,2]))
        self.assertTrue(CSS.twice_twice([0,1,3,4,1,2])) #it should detect a twice twice even with other steps between
        self.assertFalse(CSS.twice_twice([0,1,3,0,1,2])) #unless one of those steps influences one of the flasks in those two steps.

    def test_twice_twice_errors(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.twice_twice, "list")
        self.assertRaises(TypeError, CSS.twice_twice, 12.5)
        self.assertRaises(TypeError, CSS.twice_twice, [2.4,2.3])
        self.assertRaises(ValueError, CSS.twice_twice, [2,3,4])
        self.assertRaises(ValueError, CSS.twice_twice, [0,1,1,45,45,1,1,0,0,1,1,45,45,1,1,0])

    def test_full_flask(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertTrue(CSS.full_flask([0,2]))
        self.assertTrue(CSS.full_flask([1,2]))
        self.assertTrue(CSS.full_flask([2,3]))
        CSS.data = [["red","red","red","red",0],["blue3","blue3","red","blue3","blue3"],["blue3",0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertTrue(CSS.full_flask([0,2]))
        self.assertFalse(CSS.full_flask([1,2]))
        self.assertFalse(CSS.full_flask([2,3]))

    def test_full_flask_errors(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertRaises(TypeError, CSS.full_flask, "list")
        self.assertRaises(TypeError, CSS.full_flask, 12.5)
        self.assertRaises(TypeError, CSS.full_flask, [2.4,2.3])
        self.assertRaises(ValueError, CSS.full_flask, [2,3,4])
        self.assertRaises(ValueError, CSS.full_flask, [0,1,1,45,45,1,1,0,0,1,1,45,45,1,1,0])

    def is_solved(self, data):
        if type(data) != list:
            raise TypeError("Data is no list")
        for flask in data:
            if type(flask) != list:
                raise TypeError("flask is no list")
            for ball in flask:
                if type(ball) != str and type(ball) != int:
                    raise TypeError("ball is no string or interger")
                if ball != flask[0]:
                    return False
        return True

    def test_is_solved(self):
        self.assertTrue(self.is_solved([["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]))
        self.assertTrue(self.is_solved([[0,0,0,0,0],["red","red","red","red","red"],[0,0,0,0,0],["blue3","blue3","blue3","blue3","blue3"]]))
        self.assertFalse(self.is_solved([["red","red","red","red","red"],["blue3","blue3","blue3",0,"blue3"],[0,0,0,0,0],[0,0,0,0,0]]))
        self.assertFalse(self.is_solved([[0,0,"red",0,0],["red","red","red","red","red"],[0,0,0,0,0],["blue3","blue3","blue3","blue3","blue3"]]))
        self.assertFalse(self.is_solved([["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],["blue3",0,0,0,0],[0,0,0,0,0]]))

    def test_is_solved_errors(self):
        self.assertRaises(TypeError, self.is_solved, [2.4,2.3])
        self.assertRaises(TypeError, self.is_solved, "test")
        self.assertRaises(TypeError, self.is_solved, [[0,0,0],2.3])
        self.assertRaises(TypeError, self.is_solved, [[0,0,0],[2.5,0,0]])
        self.assertFalse(self.is_solved([[0,0,3],[2.5,0,0]]))

    def test_repeating_moves_solveble(self):
        CSS.data = [["red","red","red",0,0],["blue3","blue3","blue3","red","blue3"],["red","blue3",0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertEqual(len(CSS.repeating_moves())%2, 0)
        self.assertTrue(self.is_solved(CSS.data)) #tests the end state on a solved state
        CSS.data = [["red","red","red",0,0],["blue3","blue3","blue3",0,0],["red","blue3",0,0,0],["red","blue3",0,0,0]]
        self.assertEqual(len(CSS.repeating_moves())%2, 0)
        self.assertTrue(self.is_solved(CSS.data))
        CSS.data = [["red","blue3","red","red","red"],["blue3","blue3","blue3","red","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        self.assertEqual(len(CSS.repeating_moves())%2, 0)
        self.assertTrue(self.is_solved(CSS.data))
        
    def test_repeating_moves_solved(self):
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue3","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertEqual(CSS.repeating_moves(), [])
        self.assertTrue(self.is_solved(CSS.data)) #tests the end state on a solved state
        CSS.data = [["red","red","red","red","red"],["yellow","yellow","yellow","yellow","yellow"],["fkel","fkel","fkel","fkel","fkel"],[5,5,5,5,5]]
        CSS.map_data_persistent = [2, 5]
        self.assertEqual(CSS.repeating_moves(), [])
        self.assertTrue(self.is_solved(CSS.data)) #tests the end state on a solved state

    def test_repeating_moves_unsolveble(self):
        CSS.data = [["green2","green2","red"],["blue3","blue3","red"],["yellow","yellow","red"],["green2",0,0],["blue3",0,0],["yellow",0,0]]
        CSS.map_data_persistent = [4, 3]
        self.assertFalse(CSS.repeating_moves())
        self.assertFalse(self.is_solved(CSS.data)) #tests the end state on a solved state
        CSS.data = [["red","red","red","red","red"],["blue3","blue3","blue","blue3","blue3"],[0,0,0,0,0],[0,0,0,0,0]]
        CSS.map_data_persistent = [2, 5]
        self.assertFalse(CSS.repeating_moves())
        self.assertFalse(self.is_solved(CSS.data)) #tests the end state on a solved state


        
if __name__ == '__main__':
    unittest.main()
