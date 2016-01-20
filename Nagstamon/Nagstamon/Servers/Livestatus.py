# encoding: utf-8

# Nagstamon - Nagios status monitor for your desktop
# Copyright (C) 2008-2015 Henri Wahl <h.wahl@ifw-dresden.de> et al.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import requests
# disable annoying InsecureRequestWarning warnings
try:
    requests.packages.urllib3.disable_warnings()
except:
    # older requests version might not have the packages submodule
    # for example the one in Ubuntu 14.04
    pass

# import sys
# import socket
# import copy
# import webbrowser
# import datetime
# import traceback
# import platform
# import urllib.parse
# from bs4 import BeautifulSoup
#
# from Nagstamon.Helpers import (HostIsFilteredOutByRE,
#                                ServiceIsFilteredOutByRE,
#                                StatusInformationIsFilteredOutByRE,
#                                CriticalityIsFilteredOutByRE,
#                                not_empty,
#                                debug_queue,
#                                STATES)
# from Nagstamon.Objects import (GenericService, GenericHost, Result)
# from Nagstamon.Config import (conf, AppInfo)

# from collections import OrderedDict

from Nagstamon.Objects import Result
from Nagstamon.Objects import GenericHost
from Nagstamon.Objects import GenericService
from Nagstamon.Servers.Generic import GenericServer
from Nagstamon.Config import conf

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Livestatus')

import re
import json
import socket
import time
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse  # noqa


def format_timestamp(timestamp):
    ts_tuple = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', ts_tuple)


def duration(timestamp):
    """human representation of a duration"""
    factors = (60 * 60 * 24, 60 * 60, 60, 1)
    result = []
    diff = time.time() - timestamp
    for f in factors:
        x = int(diff / f)
        result.append(x)
        diff = diff - x * f
    return '%02dd %02dh %02dm %02ds' % tuple(result)


def service_to_host(data):
    """create the host data blob from the implicit join data of a service"""
    result = {}
    for key in data.keys():
        if key.startswith('host_'):
            result[key[5:]] = data[key]
    return result


class LivestatusServer(GenericServer):
    '''
        Abstract server which serves as template for all other types
        Default values are for Nagios servers
    '''

    TYPE = 'Livestatus'

    def init_config(self):
        log.info(self.monitor_url)
        host = 'localhost'
        port = 6558
        # apdhjioapsdj://host
        m = re.match('.*?://([^:/]+?)(?::(\d+))?(?:/|$)', self.monitor_url)
        if m:
            host, port = m.groups()
            if not port:
                port = 6558
            else:
                port = int(port)
            self.address = (host, port)
        else:
            log.error('unable to parse monitor_url %s', self.monitor_url)
            self.enable = False

    def init_HTTP(self):
        pass

    def communicate(self, data, response=True):
        buffersize = 2**20
        data.append('')
        data.append('')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info('connecting')
        s.connect(self.address)
        s.send('\n'.join(data).encode('utf8'))
        log.debug('response is %s', response)
        if not response:
            log.debug('no response required, closing')
            s.close()
            return ''
        result = bytes()
        line = s.recv(buffersize)
        while len(line) > 0:
            result += line
            line = s.recv(buffersize)
        log.debug('disconnect')
        s.close()
        log.debug('received %d bytes', len(result))
        result = result.decode('utf8')
        return result

    def get(self, table, raw=[], headers={}):
        """send data to livestatus socket, receive result, format as json"""
        data = ['GET %s' % table, ]
        headers['OutputFormat'] = 'json'
        headers['ColumnHeaders'] = 'on'
        for k, v in headers.items():
            data.append('%s: %s' % (k, v))
        for line in raw:
            data.append(line)
        result = self.communicate(data)
        if result:
            return json.loads(result)
        return result

    def command(self, *cmd):
        data = []
        ts = str(int(time.time()) + 5)
        for line in cmd:
            data.append('COMMAND [' + ts + '] ' + line.replace('TIMESTAMP', ts))
        self.communicate(data, response=False)

    def table(self, data):
        """take a livestatus answer and format it as a table"""
        try:
            header = data[0]
        except IndexError:
            raise StopIteration
        for line in data[1:]:
            yield(dict(zip(header, line)))

    def _get_status(self):
        """fetch any host/service not in OK state
        store the information in self.new_hosts
        """
        log.debug('_get_status')
        self.new_hosts = dict()
        filters = []
        filters.append('Filter: state != 0')  # ignore OK state
        if conf.filter_acknowledged_hosts_services:
            filters.append('Filter: acknowledged != 1')
        # hosts
        data = self.get("hosts", raw=filters)
        for h in self.table(data):
            host = self._create_host(h)
            self.new_hosts[host.name] = host
            log.info("host %s is %s", host.name, host.status)
        # services
        data = self.get("services", raw=filters)
        for s in self.table(data):
            if s['host_name'] in self.new_hosts:
                host = self.new_hosts[s['host_name']]
            else:
                # need to create the host
                xdata = service_to_host(s)
                host = self._create_host(xdata)
                self.new_hosts[host.name] = host
            service = self._create_service(s)
            service.host = host.name
            host.services[service.name] = service
        return Result()

    def get_host(self, name):
        if name in self.new_hosts:
            return self.new_hosts[name]
        host = GenericHost()
        host.name = name
        host.status = 'UP'
        self.new_hosts[name] = host
        return host

    def _create_object(self, ObjectClass, data):
        """generate eiter GenericService or GenericHost and populate it
        with given json data"""
        result = ObjectClass()
        # result.name = s['display_name']
        result.server = self.name
        # result.status = result_states[s['state']]
        result.last_check = format_timestamp(data['last_check'])
        result.duration = duration(data['last_state_change'])
        result.attempt = data['current_attempt']
        result.status_information = data['plugin_output']
        result.passiveonly = False
        result.notifications_disabled = data['notifications_enabled'] != 1
        result.flapping = data['is_flapping'] == 1
        result.acknowledged = data['acknowledged'] == 1
        result.scheduled_downtime = data['scheduled_downtime_depth'] == 1
        if data['state'] == data['last_hard_state']:
            result.status_type = 'hard'
        else:
            result.status_type = 'soft'
        return result

    def _create_host(self, data):
        """create GenericHost from json data"""
        result = self._create_object(GenericHost, data)
        result.name = data['name']
        host_states = {0: 'UP', 1: 'DOWN', 2: 'UNKNOWN'}
        result.status = host_states[data['state']]
        return result

    def _create_service(self, data):
        """create GenericService from json data"""
        result = self._create_object(GenericService, data)
        result.name = data['display_name']
        service_states = {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}
        result.status = service_states[data['state']]
        return result

    def set_recheck(self, info_dict):
        """schedule a forced recheck of a service or host"""
        service = info_dict['service']
        host = info_dict['host']
        if service:
            if self.hosts[host].services[service].is_passive_only():
                return
            cmd = ['SCHEDULE_FORCED_SVC_CHECK', host, service, 'TIMESTAMP']
        else:
            cmd = ['SCHEDULE_FORCED_HOST_CHECK', host, 'TIMESTAMP']
        self.command(';'.join(cmd))

    def set_acknowledge(self, info_dict):
        """acknowledge a service or host, or all"""
        # ACKNOWLEDGE_SVC_PROBLEM;host;service;sticky;notify;persist;author;comment
        # ACKNOWLEDGE_HOST_PROBLEM;host;sticky;notify;persist;author;comment
        host = info_dict['host']
        service = info_dict['service']
        if service:
            cmd = ['ACKNOWLEDGE_SVC_PROBLEM', host, service]
        else:
            cmd = ['ACKNOWLEDGE_HOST_PROBLEM', host]
        cmd.extend([
            '2' if info_dict['sticky'] else '1',
            '1' if info_dict['notify'] else '0',
            '1' if info_dict['persistent'] else '0',
            info_dict['author'],
            info_dict['comment'],
        ])
        self.command(';'.join(cmd))

    def set_downtime(self, info_dict):
        log.info('set_downtime not implemented')

    def set_submit_check_result(self, info_dict):
        log.info('set_submit_check_result not implemented')

    def get_start_end(self, host):
        log.info('get_start_end not implemented')
        return 'n/a', 'n/a'

    def open_monitor(self, host, service=''):
        log.info('open_monitor not implemented')
        # TODO figure out how to add more config options like socket and weburl

    def open_monitor_webpage(self):
        log.info('open_monitor_webpage not implemented')

    # TODO
    # config dialog fields
    # config
