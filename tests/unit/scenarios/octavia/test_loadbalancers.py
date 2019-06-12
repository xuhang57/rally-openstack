# Copyright 2019: Red Hat Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import mock

from rally_openstack.scenarios.octavia import loadbalancers
from tests.unit import test


class OctaviaLoadbalancersTestCase(test.ScenarioTestCase):

    def test_create_and_list_loadbalancers(self):
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        scenario = loadbalancers.CreateAndListLoadbalancers(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._load_balancer_list = mock.MagicMock()
        scenario.run(
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._load_balancer_list.call_count)

    def test_create_and_show_load_balancers(self):
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        scenario = loadbalancers.CreateAndShowLoadBalancers(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._load_balancer_show = mock.MagicMock()
        scenario.run(
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._load_balancer_show.call_count)

    def test_create_and_stats_show_load_balancers(self):
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        scenario = loadbalancers.CreateAndShowStatsLoadBalancers(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._load_balancer_stats_show = mock.MagicMock()
        scenario.run(
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._load_balancer_stats_show.call_count)

    def test_create_and_update_load_balancers(self):
        load_balancer_update_args = {"name": "_updated"}
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        scenario = loadbalancers.CreateAndUpdateLoadBalancers(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._load_balancer_set = mock.MagicMock()
        scenario.run(
            load_balancer_update_args=load_balancer_update_args,
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._load_balancer_set.call_count)

    def test_create_and_delete_load_balancers(self):
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        scenario = loadbalancers.CreateAndDeleteLoadbalancers(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._load_balancer_delete = mock.MagicMock()
        scenario.run(
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._load_balancer_delete.call_count)
