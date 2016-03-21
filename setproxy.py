#! /bin/sh
""":"
exec python $0 ${1+"$@"}
"""
import fileinput
import os
import platform
import re
import sys
import argparse

all_files = {
    # Proxy files for Ubuntu.
    'ubuntu': {
        '/etc/environment': [
            'http_proxy=":proxy.http:"',
            'https_proxy=":proxy.https:"',
            'ftp_proxy=":proxy.ftp:"',
            'socks_proxy=":proxy.socks:"'
        ],
        '/etc/wgetrc': [
            'http_proxy=":proxy.http:"',
            'https_proxy=":proxy.https:"',
            'ftp_proxy=":proxy.ftp:"',
            'socks_proxy=":proxy.socks:"'
        ],
        '/etc/apt/apt.conf': [
            'Acquire::http::proxy ":proxy.http:";',
            'Acquire::https::proxy ":proxy.https:";',
            'Acquire::ftp::proxy ":proxy.ftp:";',
            'Acquire::socks::proxy ":proxy.socks:";'
        ],
        '/etc/bash.bashrc': [
            'export http_proxy=":proxy.http:"',
            'export https_proxy=":proxy.https:"',
            'export ftp_proxy=":proxy.ftp:"',
            'export socks_proxy=":proxy.socks:"'
        ],
        '~/.bashrc': [
            'export http_proxy=":proxy.http:"',
            'export https_proxy=":proxy.https:"',
            'export ftp_proxy=":proxy.ftp:"',
            'export socks_proxy=":proxy.socks:"'
        ]
    },

    'linuxmint': {
        '/etc/environment': [
            'http_proxy=":proxy.http:"',
            'https_proxy=":proxy.https:"',
            'ftp_proxy=":proxy.ftp:"',
            'socks_proxy=":proxy.socks:"'
        ],
        '/etc/wgetrc': [
            'http_proxy=":proxy.http:"',
            'https_proxy=":proxy.https:"',
            'ftp_proxy=":proxy.ftp:"',
            'socks_proxy=":proxy.socks:"'
        ],
        '/etc/apt/apt.conf': [
            'Acquire::http::proxy ":proxy.http:";',
            'Acquire::https::proxy ":proxy.https:";',
            'Acquire::ftp::proxy ":proxy.ftp:";',
            'Acquire::socks::proxy ":proxy.socks:";'
        ],
        '/etc/bash.bashrc': [
            'export http_proxy=":proxy.http:"',
            'export https_proxy=":proxy.https:"',
            'export ftp_proxy=":proxy.ftp:"',
            'export socks_proxy=":proxy.socks:"'
        ],
        '~/.bashrc': [
            'export http_proxy=":proxy.http:"',
            'export https_proxy=":proxy.https:"',
            'export ftp_proxy=":proxy.ftp:"',
            'export socks_proxy=":proxy.socks:"'
        ]
    }
}

SUPPRESS = '==SUPPRESS=='


def die(error, message=None):
    if message:
        print message
    print error
    exit(1)


class ProxyType(object):
    def __init__(self, https=True, http=True, ftp=True, socks=True):
        self.http = http
        self.https = https
        self.ftp = ftp
        self.socks = socks


class Proxy(object):
    enabled = ProxyType()

    def __init__(self, s, pn, u=None, p=None):
        if u and p:
            proxy_string = "%s:%s@%s:%d" % (u, p, s, pn)
        else:
            proxy_string = "%s:%d" % (s, pn)

        self.http = "http://" + proxy_string
        self.https = "https://" + proxy_string
        self.ftp = "ftp://" + proxy_string
        self.socks = "socks://" + proxy_string

    def set_enabled_proxies(self, enabled):
        """
        :type enabled: ProxyType
        :param enabled: Enabled proxy types
        """
        self.enabled = enabled

    def process(self, filename, patterns, clear=False):
        """
        :type filename: str
        :param filename: Proxy configuration file

        :type patterns: list
        :param patterns: Proxy configuration patterns
        """
        proxy_pattern_string = r'(?:[^:]+:[^@]+@)?' \
                               r'((?:(?:[0-9]{1,3}\.){3}[0-9]{1,3})|' \
                               r'(?:([\da-z\.-]+)\.([a-z\.]{2,6}))):[\d]{1,5}'
        http_proxy_pattern = ':proxy.http:'
        https_proxy_pattern = ':proxy.https:'
        ftp_proxy_pattern = ':proxy.ftp:'
        socks_proxy_pattern = ':proxy.socks:'

        if not os.path.isfile(filename):
            print "Creating file: %s..." % filename
            # noinspection PyBroadException
            try:
                f = open(filename, 'w+')  # Trying to create a new file or open one
                f.close()
            except:
                die('Something went wrong! Can\'t create file: %s?' % filename)

        self.clear_proxies(filename, clear)

        f = open(filename, 'a')
        print "Setting proxy in file: %s..." % filename
        f.write("\n")
        for pattern in patterns:
            if self.enabled.http and pattern.find(http_proxy_pattern) >= 0:
                f.write(pattern.replace(http_proxy_pattern, self.http) + '\n')
            else:
                if self.enabled.https and pattern.find(https_proxy_pattern) >= 0:
                    f.write(pattern.replace(https_proxy_pattern, self.https) + '\n')
                else:
                    if self.enabled.ftp and pattern.find(ftp_proxy_pattern) >= 0:
                        f.write(pattern.replace(ftp_proxy_pattern, self.ftp) + '\n')
                    else:
                        if self.enabled.socks and pattern.find(socks_proxy_pattern) >= 0:
                            f.write(pattern.replace(socks_proxy_pattern, self.socks) + '\n')
        f.close()

    @staticmethod
    def clear_proxies(filename, clear, write=False):
        """
        :type filename: str
        :param filename: Proxy configuration file

        :type proxy_pattern_string: str
        :param proxy_pattern_string: Proxy regular expression
        """
        i = 1
        print "\nClearing old proxy from file: %s..." % filename
        for line in fileinput.input(filename, inplace=True):
            # if re.match(proxy_pattern_string, line, re.I):
            proxy_type = line.find('http') >= 0 or line.find('https') >= 0 or line.find('ftp') >= 0 or line.find(
                'socks') >= 0
            if line.find('proxy') >= 0 and proxy_type:
                if line.strip()[0] is '#':
                    if not clear:
                        sys.stdout.write(line)
                else:
                    if not clear:
                        if write:
                            sys.stdout.write(line)
                        else:
                            sys.stdout.write('# %s' % line)
                sys.stderr.write("line #%d: %s" % (i, line))
            else:
                sys.stdout.write(line)
            i += 1


def get_files():
    if os.getuid() != 0:
        die("Error: run it with sudo")
    dist = platform.linux_distribution()
    files = None
    if len(dist[0]):
        dist_name = dist[0].lower()
        print "Checking configuration for %s..." % dist_name
        if dist_name not in all_files:
            die('Error: No proxy configurations for %s.' % dist_name)
        files = all_files[dist_name]
    else:
        die('Cannot detect operation system.')
    return files


class _TestAction(argparse.Action):
    def __init__(self, option_strings, dest=SUPPRESS, default=SUPPRESS, help=None):
        super(_TestAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        files = get_files()
        for filename in files:
            Proxy.clear_proxies(os.path.expanduser(filename), False, True)
        parser.exit()


class _DeleteAction(argparse.Action):
    def __init__(self, option_strings, dest=SUPPRESS, default=SUPPRESS, help=None):
        super(_DeleteAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        files = get_files()
        for filename in files:
            Proxy.clear_proxies(os.path.expanduser(filename), True, False)
        parser.exit()


def run():
    parser = argparse.ArgumentParser(prog='setproxy', description="Easy proxy configuration")
    parser.register('action', 'test', _TestAction)
    parser.register('action', 'delete', _DeleteAction)
    parser.add_argument('server', type=str, help='Proxy server address. ex: 202.141.80.19 or tamdil.iitg.ernet.in')
    parser.add_argument('port', type=int, default=3128, help='Proxy port. commonly used ports are 3128, 8080 and 1080.',
                        nargs='?')
    parser.add_argument('-u', '--user', type=str, default=None, help='Username for proxy authentication.')
    parser.add_argument('-p', '--password', type=str, default=None, help='Password for proxy authentication.')
    parser.add_argument('--http', dest='http', action='store_true', help='Enable http proxy setting (Default: Enabled)')
    parser.add_argument('--https', dest='https', action='store_true',
                        help='Enable https proxy setting (Default: Enabled)')
    parser.add_argument('--ftp', dest='ftp', action='store_true', help='Enable ftp proxy setting')
    parser.add_argument('--socks', dest='socks', action='store_true', help='Enable socks proxy setting')
    parser.add_argument('--no-http', dest='http', action='store_false', help='Disable http proxy setting')
    parser.add_argument('--no-https', dest='https', action='store_false', help='Disable https proxy setting')
    parser.add_argument('--no-ftp', dest='ftp', action='store_false',
                        help='Disable ftp proxy setting (Default: Disabled)')
    parser.add_argument('--no-socks', dest='socks', action='store_false',
                        help='Disable socks proxy setting (Default: Disabled)')
    parser.add_argument('--clear', dest='clear', action='store_true',
                        help='Delete old proxy settings, while creating new.')
    parser.add_argument('-t', '--test', action='test', default=SUPPRESS, help='Display old proxy settings')
    parser.add_argument('-d', '--delete', action='delete', default=SUPPRESS, help='Delete old proxy settings')
    parser.set_defaults(http=True)
    parser.set_defaults(https=True)
    parser.set_defaults(ftp=False)
    parser.set_defaults(socks=False)
    parser.set_defaults(clear=False)

    args = parser.parse_args()

    proxy = Proxy(args.server, args.port, args.user, args.password)
    proxy_type = ProxyType(args.https, args.http, args.ftp, args.socks)
    proxy.set_enabled_proxies(proxy_type)
    clear = args.clear

    files = get_files()

    if clear:
        print "Deleting old proxy settings..."

    for filename, patterns in files.iteritems():
        print ''
        proxy.process(os.path.expanduser(filename), patterns, clear=clear)
        pass


run()
