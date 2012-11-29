import unittest
import conch.engine as engine

class MockAst(object):
    def __init__(self, args):
        self.args = args

    def get_argv(self):
        return self.args

class TestExecute(unittest.TestCase):
    def test_exec_true(self):
        p = engine.execute(MockAst(["/bin/true"]))
        p.wait()

    def test_exec_cat(self):
        p = engine.execute(MockAst(["/bin/cat"]))
        p.stdin.write("a")
        self.assertEquals("a", p.stdout.read(1))
        p.stdin.write("bc")
        self.assertEquals("b", p.stdout.read(1))
        self.assertEquals("c", p.stdout.read(1))
        p.stdin.close()
        p.wait()


