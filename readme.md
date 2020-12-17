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

> aicmder onnx -s output_dir -m './model/edsr.py' -c '/Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt'

> aicmder serve -w 4 -p 8080 -f tests_model/conf.json --device_map 0 --max_connect 700
> aicmder serve -w 4 -p 8080 -f tests_model/conf.json 

## abtest

ab -c 500 -t 30 -T 'application/json'  -p post.txt 127.0.0.1:8080/predict
ab -c 500 -t 30 -T 'application/json'  -p post.txt 192.168.2.156:8080/predict

## curl 

curl 127.0.0.1:8080/predict -X POST -d '{"str": "123"}'
curl 127.0.0.1:8080/predict -X POST -d '{"question": "你是谁"}'


1. if error `socket: Too many open files (24)` happened, try `ulimit -n 9000`

```

def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')


for image_file in image_file_list:
   img = open(image_file, 'rb').read()
   if img is None:
      logger.info("error in loading image:{}".format(image_file))
      continue

   # 发送HTTP请求
   starttime = time.time()
   data = {'images': [cv2_to_base64(img)]}


work_file = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'worker.py')
modules_info = json.dumps(modules_info)
for index in range(len(gpus)):
   subprocess.Popen(['python', work_file, modules_info, gpus[index], backend_addr])

def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode('utf8'))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data

```python