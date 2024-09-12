# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# python setup.py test -s tests.test_packages


SETUP_INFO = dict(
    test_suite="tests",
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
