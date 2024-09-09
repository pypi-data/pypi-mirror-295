# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# python setup.py test -s tests.test_packages

import sys

SETUP_INFO = dict(
    name="lino",
    version="24.9.0",
    description="A framework for writing desktop-like sustainably free "
    "web applications using Django and ExtJS or React",
    license="COPYING",
    author="Rumma & Ko Ltd",
    author_email="info@lino-framework.org",
    url="https://gitlab.com/lino-framework/lino",
    test_suite="tests",
)

install_requires = [
    # 'Sphinx',
    "Django",
    # 'atelier',
    "unipath",
    "python_dateutil",
    "dateparser",
    "etgen",  # 'docutils',
    "Babel",
    "lxml",
    "odfpy",
    "jinja2",
    "pytidylib",
    "PyYAML",
    "clint",  # lino.modlib.checkdata.management.commands
    "django-localflavor",  # lino.modlib.sepa
    "django-click",  # for passwd command
    "openpyxl",  # removed version requirement 'openpyxl==3.0.1',
    "html2text",
]

install_requires.append("Sphinx")  # lino.utils.restify
install_requires.append("docutils")  # lino.modlib.memo.mixins
install_requires.append("beautifulsoup4")  # lino.modlib.memo.mixins
# install_requires.append('reportlab')
install_requires.append("weasyprint")
# install_requires.append('weasyprint<=52')
# avoid function/symbol 'pango_context_set_round_glyph_positions' not found in library 'libpango-1.0.so.0': /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0: undefined symbol: pango_context_set_round_glyph_positions

# install_requires.append('weasyprint')
# install_requires.append('zodb')
# install_requires.append('DateTime')
# install_requires.append('appy@svn+https://svn.forge.pallavi.be/appy-dev/dev1')
# 'django-mailbox@git+https://github.com/cylonoven/django-mailbox#egg=django-mailbox'
# SETUP_INFO.update(dependency_links=[
#     "svn+https://svn.forge.pallavi.be/appy-dev/dev1#egg=appy-dev"
# "git+https://github.com/lino-framework/appypod.git@dbf123584cd9c5ef4a35e8efb9f489eaa54e26f2#egg=appy-dev"
# ])

SETUP_INFO.update(install_requires=install_requires)

SETUP_INFO.update(
    extras_require={
        "testing": ["atelier", "pytest", "pytest-html", "pytest-forked", "pytest-env"]
    }
)


# .. raw:: html
#
#     <a class="reference external"
#     href="http://lino.readthedocs.io/en/latest/?badge=latest"><img
#     alt="Documentation Status"
#     src="https://readthedocs.org/projects/lino/badge/?version=latest"
#     /></a> <a class="reference external"
#     href="https://coveralls.io/github/lino-framework/book?branch=master"><img
#     alt="coverage"
#     src="https://coveralls.io/repos/github/lino-framework/book/badge.svg?branch=master"
#     /></a> <a class="reference external"
#     href="https://travis-ci.org/lino-framework/book?branch=stable"><img
#     alt="build"
#     src="https://travis-ci.org/lino-framework/book.svg?branch=stable"
#     /></a> <a class="reference external"
#     href="https://pypi.python.org/pypi/lino/"><img alt="pypi_v"
#     src="https://img.shields.io/pypi/v/lino.svg" /></a> <a
#     class="reference external"
#     href="https://pypi.python.org/pypi/lino/"><img alt="pypi_license"
#     src="https://img.shields.io/pypi/l/lino.svg" /></a>

SETUP_INFO.update(
    long_description="""

This is the core package of the Lino framework.

This repository is an integral part of the `Lino framework
<https://www.lino-framework.org>`__, a sustainably free open-source project
maintained by the `Synodalsoft team <https://www.synodalsoft.net>`__ sponsored
by `Rumma & Ko OÜ <https://www.saffre-rumma.net>`__. Your contributions are
welcome.

- Code repository: https://gitlab.com/lino-framework/lino
- Test results: https://gitlab.com/lino-framework/lino/-/pipelines
- Feedback: https://community.lino-framework.org
- Maintainer: https://www.synodalsoft.net
- Service provider: https://www.saffre-rumma.net

"""
)

SETUP_INFO.update(
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines()
)

SETUP_INFO.update(
    packages=[
        str(n)
        for n in """
lino
lino.api
lino.core
lino.core.auth
lino.core.management
lino.fake_migrations
lino.mixins
lino.modlib
lino.modlib.about
lino.modlib.awesomeuploader
lino.modlib.blacklist
lino.modlib.bootstrap3
lino.modlib.changes
lino.modlib.comments
lino.modlib.comments.fixtures
lino.modlib.dashboard
lino.modlib.dupable
lino.modlib.export_excel
lino.modlib.extjs
lino.modlib.forms
lino.modlib.gfks
lino.modlib.help
lino.modlib.help.fixtures
lino.modlib.help.management
lino.modlib.help.management.commands
lino.modlib.ipdict
lino.modlib.jinja
lino.modlib.jinja.management
lino.modlib.jinja.management.commands
lino.modlib.importfilters
lino.modlib.languages
lino.modlib.languages.fixtures
lino.modlib.linod
lino.modlib.linod.management
lino.modlib.linod.management.commands
lino.management
lino.management.commands
lino.modlib.odata
lino.modlib.memo
lino.modlib.office
lino.modlib.checkdata
lino.modlib.checkdata.fixtures
lino.modlib.checkdata.management
lino.modlib.checkdata.management.commands
lino.modlib.publisher
lino.modlib.publisher.fixtures
lino.modlib.printing
lino.modlib.restful
lino.modlib.smtpd
lino.modlib.smtpd.management
lino.modlib.smtpd.management.commands
lino.modlib.notify
lino.modlib.notify.fixtures
lino.modlib.search
lino.modlib.search.management
lino.modlib.search.management.commands
lino.modlib.summaries
lino.modlib.summaries.fixtures
lino.modlib.summaries.management
lino.modlib.summaries.management.commands
lino.modlib.system
lino.modlib.tinymce
lino.modlib.tinymce.fixtures
lino.modlib.uploads
lino.modlib.uploads.fixtures
lino.modlib.users
lino.modlib.users.fixtures
lino.modlib.weasyprint
lino.modlib.wkhtmltopdf
lino.projects
lino.projects.std
lino.sphinxcontrib
lino.sphinxcontrib.logo
lino.utils
lino.utils.mldbc
""".splitlines()
        if n
    ]
)

SETUP_INFO.update(include_package_data=True)
