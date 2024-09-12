# pylint: disable=W0622
"""cubicweb-jsonschema application packaging information"""


modname = 'cubicweb_jsonschema'
distname = 'cubicweb-jsonschema'

numversion = (0, 2, 12)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'JSON Schema for CubicWeb'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.38.16, < 5.0.0',
    'cubicweb-web': '>= 0.1.3, < 2.0.0',
    'iso8601': None,
    'jsl': None,
    'pyramid': '>= 1.10.8',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: JavaScript',
]
