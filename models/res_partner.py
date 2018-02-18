# -*- coding: utf-8 -*-
# Copyright 2018 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, models, _
from openerp.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _zip_codes_consistent(self, vals):
        """Make consistent the fields zip and zip_sat_id"""

        ResCountryZipSatCode = self.env['res.country.zip.sat.code']
        if 'zip' in vals and 'zip_sat_id' not in vals:
            if vals['zip']:
                zip_sat = ResCountryZipSatCode.search([
                    ('code', '=', vals['zip'])])

                if zip_sat:
                    vals['zip_sat_id'] = zip_sat[0].id
                else:
                    raise UserError(
                        _('This zip does not exist in SAT catalog'))

        elif 'zip_sat_id' in vals and 'zip' not in vals:
            if vals['zip_sat_id']:
                zip_sat = ResCountryZipSatCode.browse(vals['zip_sat_id'])
                if zip_sat:
                    vals['zip'] = zip_sat.code
                else:
                    raise UserError(
                        _('This zip does not exist in SAT catalog'))

        elif 'zip_sat_id' in vals and 'zip' in vals:
            if vals['zip_sat_id'] and vals['zip']:

                zip_sat = ResCountryZipSatCode.browse(vals['zip_sat_id'])
                if zip_sat:
                    if zip_sat.code != vals['zip']:

                        raise UserError(
                            _('Zip codes are not consistent. Must be the same'))
                else:
                    raise UserError(
                        _('This zip does not exist in SAT catalog'))

        return vals

    @api.model
    def create(self, vals):
        _logger.debug('DEBUG CREATE VALS %s', vals)
        vals = self._zip_codes_consistent(vals)
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        _logger.debug('DEBUG WRITE VALS %s', vals)
        vals = self._zip_codes_consistent(vals)
        return super(ResPartner, self).write(vals)
