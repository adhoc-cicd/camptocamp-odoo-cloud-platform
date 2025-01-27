# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
import json

import werkzeug

from openerp.addons.web import http as oeweb
from openerp.addons.web.controllers.main import db_monodb_redirect


class HealthCheckFilter(logging.Filter):

    def __init__(self, path, name=''):
        super(HealthCheckFilter, self).__init__(name)
        self.path = path

    def filter(self, record):
        return self.path not in record.getMessage()


logging.getLogger('werkzeug').addFilter(
    HealthCheckFilter('GET /monitoring/status HTTP')
)


class Monitoring(oeweb.Controller):
    _cp_path = '/monitoring'

    @oeweb.httprequest
    def status(self, req, **kwargs):
        db, redirect = db_monodb_redirect(req)
        if redirect:
            werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))
        # TODO: add 'sub-systems' status and infos:
        # queue job, cron, database, ...
        headers = {'Content-Type': 'application/json'}
        info = {'status': 1}
        session = req.session
        # We set a custom expiration of 1 second for this request, as we do a
        # lot of health checks, we don't want those anonymous sessions to be
        # kept. Beware, it works only when session_redis is used.
        # Alternatively, we could set 'session.should_save = False', which is
        # tested in odoo source code, but we wouldn't check the health of
        # Redis.
        if not session._uid:
            session.expiration = 1
        return werkzeug.wrappers.Response(json.dumps(info), headers=headers)
