## For conversion of model

1. please create model folder as well as file of __init__.py
2. add global function like the following example.
   ```
   def make_model(args, parent=False):
    return EDSR(args)
   ```

## command

aicmder onnx -s aaaa -m /Users/faith/AI_Commander/model/edsr.py -c /Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt

> aicmder onnx -s output_dir -m '/Users/faith/AI_Commander/model/edsr.py' -c '/Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt'

> aicmder onnx -s output_dir -m './edsr.py' -c '/Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt'