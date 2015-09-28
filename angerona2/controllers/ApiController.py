import json
# import xml

class ApiController(object):
    def __init__(self, fmt='dict', **kwargs):
        self.fmt = fmt

        for key in ('status', 'data', 'msg'):
            try:
                setattr(self, key, kwargs[key])
            except KeyError:
                setattr(self, key, None)

        self.ERR = {
             0: ('OK', 'OK'),
            -1: ('OOPS', 'General error.'),
            -2: ('MISSING', 'Missing fields.'),
            -3: ('INVALID', "Fields didn't validate."),
            -4: ('THROTTLED', 'Request has been throttled.'),
        }

        self._seterror()

    def __repr__(self):
        if self.fmt == 'json':
            return json.dumps({'status': self.status, 'msg': self.msg,
                               'data': self.data})
        elif self.fmt == 'xml':
            raise ProgrammerError('xml __repr__ not implemented yet')
        else:
            return {'status': self.status, 'msg': self.msg, 'data': self.data}

    def get_error(self, name):
        for i, v in enumerate(self.ERR):
            if v[0] == name:
                return i

        raise ProgrammerError('unknown error type: {}'.format(name))

    def _seterror(self):
        # if we set status to one of the usual errors, convert it to a string
        #   and set self.msg to that string if we didn't set a msg
        if self.status and not self.msg:
            try:
                self.msg = self.ERR[self.status]
            except KeyError:
                # but don't freak out about not knowing it
                self.msg = ''

