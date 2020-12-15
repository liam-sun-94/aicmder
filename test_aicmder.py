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
        onnx.execute(['-s', 'aaaa', '-m', '/Users/faith/AI_Commander/model/edsr.py', '-c', '/Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt'])

if __name__ == "__main__":
    unittest.main()
