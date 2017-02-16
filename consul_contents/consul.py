import consulate
import os

#
# CONSUL_CONFIG = dict()
CONSUL_NAME = os.environ.get('CONSUL_NAME', 'dev')

consul = consulate.Consul(host='localhost', port=8500)
config = consul.kv.find(CONSUL_NAME)


def assign_consul(data, key, split_keys, start, end, CONSUL_CONFIG):
    if start > end or split_keys[start] == '':
        return
    if start == end:
        CONSUL_CONFIG[split_keys[start]] = str(data[key])
    else:
        if split_keys[start] not in CONSUL_CONFIG:
            CONSUL_CONFIG[split_keys[start]] = {}
        assign_consul(data, key, split_keys, start+1, end, CONSUL_CONFIG[split_keys[start]])


CONSUL_CONFIG = dict()
for key in config:
    split_keys = str(key).split('/')
    l = len(split_keys)
    assign_consul(config, key, split_keys, 1, l-1, CONSUL_CONFIG)
    # print CONSUL_CONFIG

print CONSUL_CONFIG


# consulate --datacenter dc1 --token 33921f61-d6b9-6c89-a6bb-6c872c33f83c kv backup > sample.json
# cat sample.json | consulate --datacenter dc1 --token 33921f61-d6b9-6c89-a6bb-6c872c33f83c kv restore
