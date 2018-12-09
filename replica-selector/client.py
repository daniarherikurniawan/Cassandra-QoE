import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
proxy.add(7, 3)
proxy.subtract(7, 3)
proxy.multiply(7, 3)
proxy.divide(7, 3)

