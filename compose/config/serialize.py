from __future__ import absolute_import
from __future__ import unicode_literals

import six
import yaml

from compose.config import types
from compose.config.config import V1
from compose.config.config import V2_1
from compose.config.config import V3_1


def serialize_config_type(dumper, data):
    representer = dumper.represent_str if six.PY3 else dumper.represent_unicode
    return representer(data.repr())


def serialize_dict_type(dumper, data):
    return dumper.represent_dict(data.repr())


yaml.SafeDumper.add_representer(types.VolumeFromSpec, serialize_config_type)
yaml.SafeDumper.add_representer(types.VolumeSpec, serialize_config_type)
yaml.SafeDumper.add_representer(types.ServiceSecret, serialize_dict_type)
yaml.SafeDumper.add_representer(types.ServicePort, serialize_dict_type)


def serialize_config(config):
    output = {
		service.pop('name'): service for service in config.services
    }
    return yaml.safe_dump(
        output,
        default_flow_style=False,
        indent=2,
        width=80)


def serialize_ns_time_value(value):
    result = (value, 'ns')
    table = [
        (1000., 'us'),
        (1000., 'ms'),
        (1000., 's'),
        (60., 'm'),
        (60., 'h')
    ]
    for stage in table:
        tmp = value / stage[0]
        if tmp == int(value / stage[0]):
            value = tmp
            result = (int(value), stage[1])
        else:
            break
    return '{0}{1}'.format(*result)


def denormalize_service_dict(service_dict, version):
    service_dict = service_dict.copy()

    if 'restart' in service_dict:
        service_dict['restart'] = types.serialize_restart_spec(service_dict['restart'])

    if version == V1 and 'network_mode' not in service_dict:
        service_dict['network_mode'] = 'bridge'

    if 'depends_on' in service_dict and version != V2_1:
        service_dict['depends_on'] = sorted([
            svc for svc in service_dict['depends_on'].keys()
        ])

    if 'healthcheck' in service_dict:
        if 'interval' in service_dict['healthcheck']:
            service_dict['healthcheck']['interval'] = serialize_ns_time_value(
                service_dict['healthcheck']['interval']
            )
        if 'timeout' in service_dict['healthcheck']:
            service_dict['healthcheck']['timeout'] = serialize_ns_time_value(
                service_dict['healthcheck']['timeout']
            )

    if 'ports' in service_dict and version != V3_1:
        service_dict['ports'] = map(
            lambda p: p.legacy_repr() if isinstance(p, types.ServicePort) else p,
            service_dict['ports']
        )

    return service_dict
