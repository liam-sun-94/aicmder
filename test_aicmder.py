import unittest
import aicmder as cmder


class TestCommands(unittest.TestCase):

    def test_help(self):
        print(cmder)
        help = cmder.help.HelpCommand()
        help.execute(['onnx'])
        
    def test_onnx(self):
        print(cmder)
        onnx = cmder.onnx.ONNXCommand()
        # onnx.execute(['-s', './save'])
        onnx.execute([])

if __name__ == "__main__":
    unittest.main()
