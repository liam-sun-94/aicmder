from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
import os
from shutil import copyfile
from pprint import pprint
import json
# from multiprocessing import set_start_method
# try:
#      set_start_method('spawn')
# except RuntimeError:
#     pass
import subprocess
def is_json(config):
    if config is None:
        return False
    try:
        json_object = json.loads(config)
    except ValueError as e:
        return False
    return True


@register(name='{}.serve'.format(cmd), description='start all module')
class ServeCommand:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description=self.__class__.__doc__, prog='{} serve'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--workers', '-w', type=int, default=1, help='number of server instances')
        self.parser.add_argument('--config', '-c', required=False)
        self.parser.add_argument('--file', '-f', required=False)
        self.parser.add_argument('--http_port', '-p', type=int, default=None,
                        help='server port for receiving HTTP requests')
        self.parser.add_argument('--device_map', '-d', type=int, nargs='+', default=[],
                                 help='specify the list of GPU device ids that will be used (id starts from 0). \
                        If num_worker > len(device_map), then device will be reused; \
                        if num_worker < len(device_map), then device_map[:num_worker] will be used')
        self.parser.add_argument('--cpu', action='store_true', default=False,
                                 help='running on CPU (default on GPU)')
        self.parser.add_argument('--max_connect', type=int, default=500, help='maximum number of concurrent HTTP connections')
        base_dir = os.path.dirname(__file__)
        self.work_file = os.path.join(base_dir, '../service','worker.py')
        assert os.path.exists(self.work_file)
        
    def _get_device_map(self):
        # self.logger.info('get devices')
        run_on_gpu = False
        device_map = [-1] * self.num_worker
        if not self.args.cpu:
            try:
                import GPUtil
                num_all_gpu = len(GPUtil.getGPUs())
                avail_gpu = GPUtil.getAvailable(order='memory', limit=min(num_all_gpu, self.num_worker),
                                                maxMemory=0.9, maxLoad=0.9)
                num_avail_gpu = len(avail_gpu)

                if num_avail_gpu >= self.num_worker:
                    run_on_gpu = True
                elif 0 < num_avail_gpu < self.num_worker:
                    # self.logger.warning('only %d out of %d GPU(s) is available/free, but "-num_worker=%d"' %
                    #                     (num_avail_gpu, num_all_gpu, self.num_worker))
                    # if not self.args.device_map:
                    #     self.logger.warning('multiple workers will be allocated to one GPU, '
                    #                         'may not scale well and may raise out-of-memory')
                    # else:
                    #     self.logger.warning('workers will be allocated based on "-device_map=%s", '
                    #                         'may not scale well and may raise out-of-memory' % self.args.device_map)
                    run_on_gpu = True
                else:
                    print('no GPU available, fall back to CPU')
                    # self.logger.warning('no GPU available, fall back to CPU')

                if run_on_gpu:
                    device_map = ((self.args.device_map or avail_gpu) * self.num_worker)[: self.num_worker]
            except FileNotFoundError:
                print('nvidia-smi is missing, often means no gpu on this machine. '
                                    'fall back to cpu!')
        print('device map: \n\t\t%s' % '\n\t\t'.join(
            'worker %2d -> %s' % (w_id, ('gpu %2d' % g_id) if g_id >= 0 else 'cpu') for w_id, g_id in
            enumerate(device_map)))
        return device_map

    def execute(self, argv: List) -> bool:
        print(argv)
        self.args = self.parser.parse_args(argv)
        self.num_worker = self.args.workers
        device_map = self._get_device_map()
        print(device_map)
        
        assert is_json(self.args.config) == True or os.path.exists(self.args.file) == True
        if self.args.file is not None and os.path.exists(self.args.file):
            with open(self.args.file, 'r') as f:
                content = f.read()
                config = json.loads(content)
        else:
            config = json.loads(self.args.config)
    
        # start server first
        queue = cmder.ServerQueue()
        queue.start()
        queue.is_ready.wait()
        
        workers = []
        for idx, device_id in enumerate(device_map):
            subprocess.Popen(['python', self.work_file, json.dumps(config), str(device_id)])
            
            # worker = cmder.Worker(config, device_id=device_id)
            # workers.append(worker)
            # worker.start()
        if self.args.http_port:
            # self.logger.info('start http proxy')
            proc_proxy = cmder.HTTPProxy(self.args)
            workers.append(proc_proxy)
            proc_proxy.start()    
        
        for worker in workers:
            worker.is_ready.wait()

        queue.join()
        
