#!/usr/bin/env python

'''
Get all monitors in your Datadog account and render it as a pillar suitable for
this formula.

Pass the application key and your API key as arguments or use the environment
variables APP_KEY and API_KEY.
'''

# Python libs
import argparse
import os
import re
import pdb

# 3rd party libs
import yaml
from yaml import SafeDumper
import datadog

def main():
    try:
        args = _parse_args()
        _initialize_connection(args.app_key, args.api_key)
        monitors = _get_all_monitors()
        _output_monitors(monitors, args)
    except InvocationError as e:
        print e
        return

def _get_env():
    '''
    Return API_KEY and APP_KEY from the environment
    '''
    keys = {}
    keys['app_key'] = os.environ.get('APP_KEY', '')
    keys['api_key'] = os.environ.get('API_KEY', '')

    return keys

def _parse_args():
    parser = argparse.ArgumentParser(
        description='Convert Datadog monitors into a pillar file'
    )
    parser.add_argument(
        '--app_key',
        default=os.environ.get('APP_KEY', None),
        type=str,
        help='Datadog application key'
    )
    parser.add_argument(
        '--api_key',
        default=os.environ.get('API_KEY', None),
        type=str,
        help='Datadog API key'
    )
    parser.add_argument(
        '--output',
        default='monitors.yml',
        type=str,
        help='Output file'
    )

    return parser.parse_args()

def _initialize_connection(app_key, api_key):
    if not app_key or not api_key:
        message = (
            'Missing keys: \n'
            'Your application key and API key must be specified either on the '
            'command line or in environment variables as APP_KEY and API_KEY '
            'respectively.'
        )
        raise InvocationError(message)
    keys = {
        'app_key': app_key,
        'api_key': api_key
    }
    datadog.initialize(**keys)

def _get_all_monitors():
    res = datadog.api.Monitor.get_all()
    if 'errors' in res:
        raise Exception('Failed to get monitors')

    return res

def _output_monitors(monitors, args):
    pillar = {}
    pillar['datadog_monitors'] = {}
    pillar['datadog_monitors']['api_key'] = args.api_key
    pillar['datadog_monitors']['app_key'] = args.app_key
    pillar['datadog_monitors']['manage_completely'] = False

    _escape_jinja_tags(monitors)

    # Overwrite the SafeDumper's default representation for type(None)
    SafeDumper.add_representer(type(None), _represent_none)

    monitors_dict = {}
    attribute_list = ['type', 'query', 'message', 'tags', 'options']
    for monitor in monitors:
        name = monitor['name']
        monitors_dict[name] = {}
        for attribute in attribute_list:
            monitors_dict[name][attribute] = monitor[attribute]

    pillar['datadog_monitors']['monitors'] = monitors_dict

    pdb.set_trace()
    with open(args.output, 'w') as f:
        yaml.safe_dump(pillar, f)

def _escape_jinja_tags(monitors):
    '''
    Datadog allows evaluation of variables within the message, and they do so
    using Jinja's default tags (ie. {{ and }}). Therefore, we need to "escape"
    the tags, so that messages are correctly rendered in Salt.
    '''
    for monitor in monitors:
        monitor['message'] = re.sub(
            r"{{(.*?)}}",
            r"{{'{{'}}\1{{'}}'}}",
            monitor['message']
        )

def _represent_none(self, _):
    '''
    Some fields (eg. no_data_timeframe) are rendered by pyyaml as `null` which
    is not accepted by datadog as a valid field. Here we define the
    representation of type(None) as 'None'.

    References:
    https://stackoverflow.com/questions/37200150/can-i-dump-blank-instead-of-null-in-yaml-pyyaml
    https://pyyaml.org/wiki/PyYAMLDocumentation
    '''

    return self.represent_scalar('tag:yaml.org,2002:null', '')

class InvocationError(Exception):
    '''
    Indicates a user invocation error.
    '''
    pass

if __name__ == '__main__':
    main()
