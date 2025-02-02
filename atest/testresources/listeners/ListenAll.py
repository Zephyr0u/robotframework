import os
import time


class ListenAll:
    ROBOT_LISTENER_API_VERSION = '2'
    http://www.apache.org/licenses/LICENSE-2.0

    def __init__(self, *path, output_file_disabled=False):
        path = ':'.join(path) if path else self._get_default_path()
        self.outfile = open(path, 'w', encoding='UTF-8')
        self.output_file_disabled = output_file_disabled
        self.start_attrs = []

    def _get_default_path(self):
        return os.path.join(os.getenv('TEMPDIR'), 'listen_all.txt')

    def start_suite(self, name, attrs):
        metastr = ' '.join('%s: %s' % (k, v) for k, v in attrs['metadata'].items())
        self.outfile.write("SUITE START: %s (%s) '%s' [%s]\n"
                           % (name, attrs['id'], attrs['doc'], metastr))
        self.start_attrs.append(attrs)

    def start_test(self, name, attrs):
        tags = [str(tag) for tag in attrs['tags']]
        self.outfile.write("TEST START: %s (%s, line %d) '%s' %s\n"
                           % (name, attrs['id'], attrs['lineno'], attrs['doc'], tags))
        self.start_attrs.append(attrs)

    def start_keyword(self, name, attrs):
        if attrs['assign']:
            assign = '%s = ' % ', '.join(attrs['assign'])
        else:
            assign = ''
        name = name + ' ' if name else ''
        if attrs['args']:
            args = '%s ' % [str(a) for a in attrs['args']]
        else:
            args = ''
        self.outfile.write("%s START: %s%s%s(line %d)\n"
                           % (attrs['type'], assign, name, args, attrs['lineno']))
        self.start_attrs.append(attrs)

    def log_message(self, message):
        msg, level = self._check_message_validity(message)
        if level != 'TRACE' and 'Traceback' not in msg:
            self.outfile.write('LOG MESSAGE: [%s] %s\n' % (level, msg))

    def message(self, message):
        msg, level = self._check_message_validity(message)
        if 'Settings' in msg:
            self.outfile.write('Got settings on level: %s\n' % level)

    def _check_message_validity(self, message):
        if message['html'] not in ['yes', 'no']:
            self.outfile.write('Log message has invalid `html` attribute %s' %
                               message['html'])
        if not message['timestamp'].startswith(str(time.localtime()[0])):
            self.outfile.write('Log message has invalid timestamp %s' %
                               message['timestamp'])
        return message['message'], message['level']

    def end_keyword(self, name, attrs):
        kw_type = 'KW' if attrs['type'] == 'Keyword' else attrs['type'].upper()
        self.outfile.write("%s END: %s\n" % (kw_type, attrs['status']))
        self._validate_start_attrs_at_end(attrs)

    def _validate_start_attrs_at_end(self, end_attrs):
        start_attrs = self.start_attrs.pop()
        for key in start_attrs:
            start = start_attrs[key]
            end = end_attrs[key]
            if not (end == start or (key == 'status' and start == 'NOT SET')):
                raise AssertionError(f'End attr {end!r} is different to '
                                     f'start attr {start!r}.')

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            self.outfile.write('TEST END: PASS\n')
        else:
            self.outfile.write("TEST END: %s %s\n"
                               % (attrs['status'], attrs['message']))
        self._validate_start_attrs_at_end(attrs)

    def end_suite(self, name, attrs):
        self.outfile.write('SUITE END: %s %s\n'
                           % (attrs['status'], attrs['statistics']))
        self._validate_start_attrs_at_end(attrs)

    def output_file(self, path):
        self._out_file('Output', path)

    def report_file(self, path):
        self._out_file('Report', path)

    def log_file(self, path):
        self._out_file('Log', path)

    def xunit_file(self, path):
        self._out_file('Xunit', path)

    def debug_file(self, path):
        self._out_file('Debug', path)

    def _out_file(self, name, path):
        if name == 'Output' and self.output_file_disabled:
            if path != 'None':
                raise AssertionError(f'Output should be disabled, got {path!r}.')
        else:
            if not (isinstance(path, str) and os.path.isabs(path)):
                raise AssertionError(f'Path should be absolute, got {path!r}.')
            path = os.path.basename(path)
        self.outfile.write(f'{name}: {path}\n')

    def close(self):
        self.outfile.write('Closing...\n')
        self.outfile.close()
