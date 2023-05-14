from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from audit.my_thrift.gen_py.Test.ttypes import ConfigRequest, ConfigResponse
from audit.my_thrift.gen_py.Test.ConfigService import Client


def rpc_client_start(hostname, username, password, input_file):
	# 创建 thrift 客户端连接
	transport = TSocket.TSocket('localhost', 9000)
	transport = TTransport.TBufferedTransport(transport)
	protocol = TBinaryProtocol.TBinaryProtocol(transport)
	client = Client(protocol)

	transport.open()

	# 调用 thrift 方法获取路由器配置信息
	response = client.get_config(ConfigRequest(
    	hostname=hostname,
    	username=username,
    	password=password,
    	input_file=input_file
	))

	transport.close()

	return response


