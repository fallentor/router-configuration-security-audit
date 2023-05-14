import sys
import os
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

auto_gen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_py')
sys.path.append(auto_gen_path)

from Test.ConfigService import Processor
from Test.ttypes import ConfigRequest, ConfigResponse
from router_ssh_client import RouterSshClient

class RouterSshHandler:
    def get_config(self, request: ConfigRequest) -> ConfigResponse:
        result = ConfigResponse()

        try:
            ssh = RouterSshClient(request.hostname, request.username, request.password, request.input_file)
            ssh.connect()
            output = ssh.get_running_config()
            result.success = True
            result.message = 'Success'
        except Exception as e:
            result.success = False
            result.message = str(e)

        return result

def serve():
    # 创建 thrift 服务端对象
    handler = RouterSshHandler()
    processor = Processor(handler)
    transport = TSocket.TServerSocket(port=9000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 创建 thrift 服务进程并启动监听
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.serve()

if __name__ == '__main__':
    print("start Listenning 9000 port...")
    serve()
