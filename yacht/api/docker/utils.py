import re

REGEXP_PORT_ASSIGN = r'^(?:(?:\d{1,5}\:)?\d{1,5})|\:d{1,5}/(?:tcp|udp)$'

# Input Format:
# [
#     '80:8080/tcp',
#     '123:123/udp'
#     '4040/tcp',
# ]
# Result Format:
# [
#     {
#         'cport': '80',
#         'hport': '8080',
#         'proto': 'tcp',
#     },
#     ...
# ]
def conv_ports2dict(data):
    if not all(isinstance(x, str) for x in data):
        raise TypeError('Expected list of str types.')
    if not all(re.match(REGEXP_PORT_ASSIGN, x, flags=re.IGNORECASE) for x in data):
        raise ValueError('Malformed port assignment.')

    delim = ':'
    portlst = []
    for port_data in data:
        cport,hport = None,port_data
        if delim in hport:
            cport,hport = hport.split(delim, 1)
            if not cport: cport = None
        hport,proto = hport.split('/', 1)
        portlst.append({ 'cport': cport, 'hport': hport, 'proto': proto })
    return portlst
