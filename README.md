consul-contents
===============

Consul-contents is for loading key-value from consul server in given hierarchy unlike consulate.
This has been developed on top of [consulate](https://github.com/gmr/consulate).

Installation
-------------

Consul-contents is available via pypi and can be installed with pip:

    pip install consul_contents

Description
-----------

Consul-contents get default as a root directory and give data inside default in dict format.
If you want to change any value inside default directory server to server. You just need to
set ENV in your server os that is CONSUL_ENV_NAME='xxxxx'.

Consul-content first read data from default directory and then CONSUL_ENV_NAME directory
from consul. If new data in CONSUL_ENV_NAME then it will add in resultant dict (default dir data)
otherwise overwrite on existing default data.

Example with consul snapshots:

![alt-text](https://raw.githubusercontent.com/vidur-88/consul_contents/master/consul1.png)

In above images you can see 2 root directory one is **default** and other is **dev_server**
If your os env has CONSUL_ENV_NAME='dev_server' then consul-contents overwrite **dev_server**
directory's data on **default** directory's data on same hierarchal level.

![alt-text](https://raw.githubusercontent.com/vidur-88/consul_contents/master/consul2.png)

In this image you can see hierarchy is default->databases->default->db_name->'localhost'
consul-contents return dict: result['databases']['default']['db_name'] = 'localhost'

if dev-server->databases->default->db_name->'server-ip' is exist then
consul-contents return dict: result['databases']['default']['db_name'] = 'server-ip'

if dev-server->anykey->'value' and anykey is not exist in default directory then
consul-contents add anykey in resultant dict: result['anykey'] = 'value'


Example
-------

```
from consul_contents import consul

consul_server_info = {'host': 'localhost', 'port': 8500, 'token': 'xxx'}
consul_kv = consul.ConsulContents(consul_server_info).get_consul_data()

 '''
 signature of ConsulContents is (host=consul_server['host'],
                                       port=consul_server['port'],
                                       token=consul_server.get('token'),
                                       datacenter=consul_server.get('datacenter'),
                                       scheme=consul_server.get('scheme', 'http'),
                                       adapter=consul_server.get('adapter'))
'''

```

So, you will get data (consul_kv) from consul in dict format.

Motivation
----------

Consulate give data from consul in following format:
```
{u'default/databases/default/host': u'server-ip', u'default/redis/host': u'localhost', u'default/databases/default/db_name': u'db_name', u'default/redis/port': u'6379'}
```
So, in above format it is difficult to find hierarchy level which you have given in consul.

Consul-contents output like:
```
{'redis': {'host': 'localhost', 'port': '6379'}, 'databases': {'default': {'host': 'server-ip', 'db_name': 'db_name'}}}
```
So, using consul-contents you can easily figure out hierarchy level.
