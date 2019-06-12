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

from rally_openstack.scenarios.octavia import pools
from tests.unit import test


class PoolsTestCase(test.ScenarioTestCase):

    def test_create_and_list_pools(self):
        pool_create_args = {}
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        pool = mock.MagicMock()
        scenario = pools.CreateAndListPools(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._pool_create = mock.MagicMock()
        scenario._pool_create.return_value = pool
        scenario._pool_list = mock.MagicMock()
        scenario.run(
            pool_create_args=pool_create_args,
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._pool_create.call_count)
        self.assertEqual(1, scenario._pool_list.call_count)

    def test_create_and_show_pools(self):
        pool_create_args = {}
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        pool = mock.MagicMock()
        scenario = pools.CreateAndShowPools(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._pool_create = mock.MagicMock()
        scenario._pool_create.return_value = pool
        scenario._pool_show = mock.MagicMock()
        scenario.run(
            pool_create_args=pool_create_args,
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._pool_create.call_count)
        self.assertEqual(1, scenario._pool_show.call_count)

    def test_create_and_update_pools(self):
        pool_create_args = {}
        pool_update_args = {}
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        pool = mock.MagicMock()
        scenario = pools.CreateAndUpdatePools(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._pool_create = mock.MagicMock()
        scenario._pool_create.return_value = pool
        scenario._pool_set = mock.MagicMock()
        scenario.run(
            pool_update_args=pool_update_args,
            pool_create_args=pool_create_args,
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._pool_create.call_count)
        self.assertEqual(1, scenario._pool_set.call_count)

    def test_create_and_delete_pools(self):
        pool_create_args = {}
        load_balancer_create_args = {}
        subnet = [{"id": 123}]
        lb = mock.MagicMock()
        pool = mock.MagicMock()
        scenario = pools.CreateAndDeletePools(self.context)
        scenario._list_subnets = mock.MagicMock(return_value=subnet)
        scenario._load_balancer_create = mock.MagicMock()
        scenario._load_balancer_create.return_value = lb
        scenario._pool_create = mock.MagicMock()
        scenario._pool_create.return_value = pool
        scenario._pool_delete = mock.MagicMock()
        scenario.run(
            pool_create_args=pool_create_args,
            load_balancer_create_args=load_balancer_create_args)
        self.assertEqual(1, scenario._list_subnets.call_count)
        self.assertEqual(1, scenario._load_balancer_create.call_count)
        self.assertEqual(1, scenario._pool_create.call_count)
        self.assertEqual(1, scenario._pool_delete.call_count)
