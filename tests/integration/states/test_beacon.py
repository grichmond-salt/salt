# -*- coding: utf-8 -*-
'''
Integration tests for the beacon states
'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt Testing Libs
import salt.utils.versions
from tests.support.case import ModuleCase
from tests.support.mixins import SaltReturnAssertsMixin

import tornado

import logging
log = logging.getLogger(__name__)


TORNADO_50 = (
    salt.utils.versions.LooseVersion(tornado.version) >=
    salt.utils.versions.LooseVersion('5.0')
)


@skipIf(TORNADO_50, "We need to make this work with tornado 5.0")
class BeaconStateTestCase(ModuleCase, SaltReturnAssertsMixin):
    '''
    Test beacon states
    '''
    def setUp(self):
        '''
        '''
        self.run_function('beacons.reset')

    def tearDown(self):
        self.run_function('beacons.reset')

    def test_present_absent(self):
        kwargs = {'/': '38%', 'interval': 5}
        ret = self.run_state(
            'beacon.present',
            name='diskusage',
            **kwargs
        )
        self.assertSaltTrueReturn(ret)

        ret = self.run_function('beacons.list', return_yaml=False)
        self.assertTrue('diskusage' in ret)
        self.assertTrue({'interval': 5} in ret['diskusage'])
        self.assertTrue({'/': '38%'} in ret['diskusage'])

        ret = self.run_state(
            'beacon.absent',
            name='diskusage',
        )
        self.assertSaltTrueReturn(ret)

        ret = self.run_function('beacons.list', return_yaml=False)
        self.assertEqual(ret, {'beacons': {}})
