# -*- coding: utf-8 -*-
# Copyright (C) 2023 - Teclib'ERP (<https://www.teclib-erp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from collections import OrderedDict
from . import base


class OdooConfig(base.OdooModule):
    _name = "Config"

    def __init__(self, configurator, auto_apply=True):
        self.auto_apply = auto_apply
        super(OdooConfig, self).__init__(configurator)

    def apply(self):
        super(OdooConfig, self).apply()
        config_values = self.prepare_config_values()
        if config_values:
            self.execute_config(config_values)

    def execute_script_config(self, datas=False):
        datas = datas if datas else self._datas
        for key in datas:
            if isinstance(datas.get(key), dict) or isinstance(datas.get(key), OrderedDict):
                if datas.get(key).get('config', {}):
                    self.logger.info("\t- Config for %s" % key)
                    values = self.prepare_company_values(datas.get(key).get('config', {}))
                    self.execute_config(values)

    def prepare_config_values(self, datas=False):
        datas = datas if datas else self._datas
        config_values = {}
        for key in datas:
            if isinstance(datas.get(key), dict) or isinstance(datas.get(key), OrderedDict):
                if datas.get(key).get('config', {}):
                    self.logger.info("\t- Config for %s" % key)
                    config_values.update(datas.get(key).get('config', {}))
        if config_values:
            self.prepare_company_values(datas)
        return config_values

    def prepare_company_values(self, values):
        self.pre_config(values)
        if values.get('company_id'):
            self._context['allowed_company_ids'] = [values.get('company_id')]
        if values.get('allowed_company_ids'):
            self._context['allowed_company_ids'] = values.get('allowed_company_ids')
            values.pop('allowed_company_ids')
        return values

    def execute_config(self, config):
        context = self._context
        for key in config:
            if isinstance(config[key], str) and config[key].startswith('get_'):
                config[key] = self.safe_eval(config[key])
        domain = []

        if 'context' in config:
            context.update(config.pop('context'))

        if 'company_id' in config:
            domain.append(('company_id', '=', config['company_id']))
            context['allowed_company_ids'] = [config['company_id']]

        config_ids = self.search('res.config.settings', domain, context=context)
        if config_ids:
            config_id = config_ids[-1]
        else:
            config_id = self.execute_odoo('res.config.settings', 'create', [self.deep_convert_dict(config)],
                                          {'context': context})
        self.execute_odoo('res.config.settings', 'write', [config_id, self.deep_convert_dict(config)],
                          {'context': context})
        self.execute_odoo('res.config.settings', 'execute', [config_id], {'context': context})
