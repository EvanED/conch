import unittest
import conch.ast

ast = conch.ast

#class Test_Position(unittest.TestCase):
#    def test_create(self):
#        p = ast.Position(1,2)

class Test_Word(unittest.TestCase):
    def test_create(self):
        w = ast.Word("a")

    def test_retrieve_a_word(self):
        w = ast.Word("a")
        w.getWord()

    def test_retrieve_original_word(self):
        w1 = ast.Word("a1")
        w2 = ast.Word("a2")
        self.assertEqual("a1", w1.getWord())
        self.assertEqual("a2", w2.getWord())


if __name__ == '__main__':
    unittest.main()
