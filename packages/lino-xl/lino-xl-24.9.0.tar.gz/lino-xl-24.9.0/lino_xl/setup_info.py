# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# $ pytest tests/test_packages.py

SETUP_INFO = dict(
    name='lino-xl',
    version='24.9.0',
    install_requires=['lino', 'commondata'],  # odfpy dependency now in lino_xl.lib.appypod
    tests_require=[],
    description="The Lino Extensions Library",
    license_files=['COPYING'],
    author='Rumma & Ko Ltd',
    author_email='info@saffre-rumma.net',
    url="https://gitlab.com/lino-framework/xl",
    test_suite='tests')

SETUP_INFO.update(long_description="""

The **Lino Extensions Library** is a collection of plugins used by many Lino
applications.

- This repository is considered an integral part of the Lino framework, which is
  documented as a whole in the `Lino Book
  <https://www.lino-framework.org/about/overview.html>`__.

- Your feedback is welcome.  See https://community.lino-framework.org

- API changes to this repository are logged at
  https://www.lino-framework.org/changes/


""")

SETUP_INFO.update(packages=[
    str(n) for n in """
lino_xl
lino_xl.lib
lino_xl.lib.addresses
lino_xl.lib.addresses.fixtures
lino_xl.lib.agenda
lino_xl.lib.agenda.fixtures
lino_xl.lib.albums
lino_xl.lib.albums.fixtures
lino_xl.lib.ana
lino_xl.lib.ana.fixtures
lino_xl.lib.b2c
lino_xl.lib.b2c.fixtures
lino_xl.lib.appypod
lino_xl.lib.bdvat
lino_xl.lib.bdvat.fixtures
lino_xl.lib.beid
lino_xl.lib.blogs
lino_xl.lib.blogs.fixtures
lino_xl.lib.bnid
lino_xl.lib.boards
lino_xl.lib.bevat
lino_xl.lib.bevat.fixtures
lino_xl.lib.bevats
lino_xl.lib.bevats.fixtures
lino_xl.lib.eevat
lino_xl.lib.eevat.fixtures
lino_xl.lib.cal
lino_xl.lib.cal.fixtures
lino_xl.lib.cal.management
lino_xl.lib.cal.management.commands
lino_xl.lib.cal.workflows
lino_xl.lib.calview
lino_xl.lib.calview.fixtures
lino_xl.lib.clients
lino_xl.lib.coachings
lino_xl.lib.coachings.fixtures
lino_xl.lib.concepts
lino_xl.lib.contacts
lino_xl.lib.contacts.fixtures
lino_xl.lib.contacts.management
lino_xl.lib.contacts.management.commands
lino_xl.lib.countries
lino_xl.lib.countries.fixtures
lino_xl.lib.courses
lino_xl.lib.courses.fixtures
lino_xl.lib.courses.workflows
lino_xl.lib.cv
lino_xl.lib.cv.fixtures
lino_xl.lib.dupable_partners
lino_xl.lib.dupable_partners.fixtures
lino_xl.lib.eid_jslib
lino_xl.lib.eid_jslib.beid
lino_xl.lib.events
lino_xl.lib.events.fixtures
lino_xl.lib.excerpts
lino_xl.lib.excerpts.fixtures
lino_xl.lib.orders
lino_xl.lib.extensible
lino_xl.lib.families
lino_xl.lib.github
lino_xl.lib.groups
lino_xl.lib.groups.fixtures
lino_xl.lib.google
lino_xl.lib.google.calendar
lino_xl.lib.households
lino_xl.lib.households.fixtures
lino_xl.lib.healthcare
lino_xl.lib.healthcare.fixtures
lino_xl.lib.humanlinks
lino_xl.lib.humanlinks.fixtures
lino_xl.lib.lists
lino_xl.lib.lists.fixtures
lino_xl.lib.caldav
lino_xl.lib.mailbox
lino_xl.lib.mailbox.fixtures
lino_xl.lib.meetings
lino_xl.lib.measurements
lino_xl.lib.nicknames
lino_xl.lib.nicknames.fixtures
lino_xl.lib.notes
lino_xl.lib.notes.fixtures
lino_xl.lib.outbox
lino_xl.lib.outbox.fixtures
lino_xl.lib.phones
lino_xl.lib.phones.fixtures
lino_xl.lib.pisa
lino_xl.lib.polls
lino_xl.lib.polls.fixtures
lino_xl.lib.postings
lino_xl.lib.products
lino_xl.lib.products.fixtures
lino_xl.lib.properties
lino_xl.lib.properties.fixtures
lino_xl.lib.reception
lino_xl.lib.rooms
lino_xl.lib.sheets
lino_xl.lib.sheets.fixtures
lino_xl.lib.skills
lino_xl.lib.sources
lino_xl.lib.sources.fixtures
lino_xl.lib.stars
lino_xl.lib.statbel
lino_xl.lib.statbel.countries
lino_xl.lib.statbel.countries.fixtures
lino_xl.lib.storage
lino_xl.lib.subscriptions
lino_xl.lib.topics
lino_xl.lib.userstats
lino_xl.lib.shopping
lino_xl.lib.shopping.fixtures
lino_xl.lib.teams
lino_xl.lib.xl

lino_xl.lib.finan
lino_xl.lib.finan.fixtures
lino_xl.lib.ledgers
lino_xl.lib.accounting
lino_xl.lib.accounting.fixtures
lino_xl.lib.accounting.management
lino_xl.lib.accounting.management.commands
lino_xl.lib.trading
lino_xl.lib.trading.fixtures
lino_xl.lib.sepa
lino_xl.lib.inbox
lino_xl.lib.inbox.fixtures
lino_xl.lib.inbox.management
lino_xl.lib.inbox.management.commands
lino_xl.lib.inspect
lino_xl.lib.invoicing
lino_xl.lib.invoicing.fixtures
lino_xl.lib.sepa.fixtures
lino_xl.lib.tim2lino
lino_xl.lib.tim2lino.fixtures
lino_xl.lib.trends
lino_xl.lib.trends.fixtures
lino_xl.lib.vat
lino_xl.lib.vat.fixtures
lino_xl.lib.vatless

lino_xl.lib.deploy
lino_xl.lib.deploy.fixtures
lino_xl.lib.tickets
lino_xl.lib.tickets.fixtures
lino_xl.lib.working
lino_xl.lib.working.fixtures
lino_xl.lib.uploads
lino_xl.lib.uploads.fixtures
lino_xl.lib.votes
lino_xl.lib.votes.fixtures
""".splitlines() if n
])

SETUP_INFO.update(classifiers="""\
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
Topic :: Software Development :: Libraries :: Application Frameworks""".
                  splitlines())

SETUP_INFO.update(include_package_data=True)
