import consulate
import os


CONSUL_ENV_NAME = 'CONSUL_NAME'
DEFAULT_CONSUL_NAME = 'default'


class ConsulContents:
    def __init__(self, consul_server):
        self.consul_name = os.environ.get('CONSUL_ENV_NAME', None)
        self.consul = consulate.Consul(host=consul_server['host'], port=consul_server['port'])
        self.consul_key_value_default = self.consul.kv.find(DEFAULT_CONSUL_NAME)
        self.consul_key_value_env = None
        if self.consul_name:
            self.consul_key_value_env = self.consul.kv.find(self.consul_name)
        self.consul_nested_data = dict()

    def assign_consul(self, data, key, split_keys, start, end, consul_nested_data):
        if start > end or split_keys[start] == '':
            return
        if start == end:
            consul_nested_data[split_keys[start]] = str(data[key])
        else:
            if split_keys[start] not in consul_nested_data:
                consul_nested_data[split_keys[start]] = dict()
            self.assign_consul(data, key, split_keys, start+1, end, consul_nested_data[split_keys[start]])

    def set_consul_nested_data(self, datasets):
        for key in datasets:
            split_keys = str(key).split('/')
            keys_len = len(split_keys)
            self.assign_consul(datasets, key, split_keys, 1, keys_len-1, self.consul_nested_data)

    def get_consul_data(self):
        self.set_consul_nested_data(self.consul_key_value_default)
        if self.consul_key_value_env:
            self.set_consul_nested_data(self.consul_key_value_env)
        return self.consul_nested_data


# consulate --datacenter dc1 --token 33921f61-d6b9-6c89-a6bb-6c872c33f83c kv backup > sample.json
# cat sample.json | consulate --datacenter dc1 --token 33921f61-d6b9-6c89-a6bb-6c872c33f83c kv restore
