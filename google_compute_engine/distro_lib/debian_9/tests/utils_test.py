#!/usr/bin/python
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unittest for utils.py module."""

from google_compute_engine.distro_lib.debian_9 import utils
from google_compute_engine.test_compat import mock
from google_compute_engine.test_compat import unittest


class UtilsTest(unittest.TestCase):

  def setUp(self):
    self.mock_logger = mock.Mock()
    self.mock_setup = mock.create_autospec(utils.Utils)

  @mock.patch('google_compute_engine.distro_lib.helpers.CallDhclientIpv6')
  @mock.patch('google_compute_engine.distro_lib.helpers.SetRouteInformationSysctlIPv6')
  def testEnableIpv6(self, mock_call, mock_sysctl):
    mocks = mock.Mock()
    mocks.attach_mock(mock_call, 'call')
    mocks.attach_mock(mock_sysctl, 'sysctl')

    utils.Utils.EnableIpv6(self.mock_setup, ['A', 'B'], self.mock_logger)
    expected_calls = [mock.call.call(['A', 'B'], mock.ANY),
                      mock.call.sysctl(['A', 'B'], mock.ANY)]
    self.assertEqual(mocks.mock_calls, expected_calls)

  @mock.patch('google_compute_engine.distro_lib.helpers.CallDhclient')
  def testEnableNetworkInterfaces(self, mock_call):
    mocks = mock.Mock()
    mocks.attach_mock(mock_call, 'call')

    utils.Utils.EnableNetworkInterfaces(
        self.mock_setup, ['A', 'B'], self.mock_logger)
    expected_calls = [mock.call.call(['A', 'B'], mock.ANY)]
    self.assertEqual(mocks.mock_calls, expected_calls)

  @mock.patch('google_compute_engine.distro_lib.helpers.CallHwclock')
  def testHandleClockSync(self, mock_call):
    mocks = mock.Mock()
    mocks.attach_mock(mock_call, 'call')

    utils.Utils.HandleClockSync(self.mock_setup, self.mock_logger)
    expected_calls = [mock.call.call(mock.ANY)]
    self.assertEqual(mocks.mock_calls, expected_calls)

  @mock.patch('google_compute_engine.distro_lib.ip_forwarding_utils.IpForwardingUtilsIproute')
  def testIpForwardingUtils(self, mock_call):
    mocks = mock.Mock()
    mocks.attach_mock(mock_call, 'call')

    utils.Utils.IpForwardingUtils(self.mock_setup, self.mock_logger, '66')
    expected_calls = [mock.call.call(mock.ANY, '66')]
    self.assertEqual(mocks.mock_calls, expected_calls)
