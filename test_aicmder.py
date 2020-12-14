import unittest
import aicmder as cmder


class TestCommands(unittest.TestCase):

    def test_fastai(self):
        print(cmder)
        help = cmder.help.HelpCommand()
        help.execute(['onnx'])


if __name__ == "__main__":
    unittest.main()
