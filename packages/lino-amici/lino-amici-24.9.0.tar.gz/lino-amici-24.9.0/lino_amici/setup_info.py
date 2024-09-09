# -*- coding: UTF-8 -*-
# Copyright 2017-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# $ python setup.py test -s tests.test_packages

SETUP_INFO = dict(
    name='lino-amici',
    version='24.9.0',
    install_requires=['lino-xl', 'vobject'],

    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("Manage your family contacts"),
    long_description="""\

**Lino Amici** helps you to manage your family contacts.

- Source code: https://gitlab.com/lino-framework/amici

- Documentation: https://lino-framework.gitlab.io/amici/

- Changelog: https://lino-framework.gitlab.io/amici/changes.html

- This is an integral part of the Lino framework, which is documented
  at https://www.lino-framework.org

- For introductions, commercial information and hosting solutions
  see https://www.saffre-rumma.net

- This is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.


""",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/amici",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
Topic :: Communications :: Email :: Address Book
Topic :: Office/Business :: Groupware
""".splitlines())

SETUP_INFO.update(packages=[
    str(n) for n in """
lino_amici
lino_amici.lib
lino_amici.lib.amici
lino_amici.lib.cal
lino_amici.lib.contacts
lino_amici.lib.contacts.fixtures
lino_amici.lib.households
lino_amici.lib.households.fixtures
lino_amici.projects
lino_amici.projects.amici1
lino_amici.projects.amici1.tests
lino_amici.projects.amici1.fixtures
lino_amici.lib.users
lino_amici.lib.users.fixtures
""".splitlines() if n
])

SETUP_INFO.update(include_package_data=True, zip_safe=False)
