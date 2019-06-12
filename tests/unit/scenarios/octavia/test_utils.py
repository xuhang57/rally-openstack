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

from rally_openstack.scenarios.octavia import utils
from tests.unit import test

OCTAVIA_UTILS = "rally_openstack.scenarios.octavia.utils"


class LoadbalancerBaseTestCase(test.ScenarioTestCase):

    def setUp(self):
        super(LoadbalancerBaseTestCase, self).setUp()
        self.load_balancer = mock.Mock()
        self.pool = mock.Mock()
        self.scenario = utils.OctaviaScenario(self.context)

        self.random_name = "random_name"
        self.scenario.generate_random_name = mock.Mock(
            return_value=self.random_name)

    def test__load_balancer_create(self):
        self.clients(
            "octavia").load_balancer_create.return_value = self.load_balancer
        load_balancer_data = {"vip_subnet_id": "subnet-id"}
        expected_load_balancer_data = {"loadbalancer": load_balancer_data}
        load_balancer = self.scenario._load_balancer_create(load_balancer_data)
        self.assertEqual(self.load_balancer, load_balancer)
        self.clients("octavia").load_balancer_create.assert_called_once_with(
            json=expected_load_balancer_data)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_create")

    def test__load_balancer_list(self):
        load_balancers_list = []
        load_balancers_dict = {"loadbalancers": load_balancers_list}
        self.clients(
            "octavia").load_balancer_list.return_value = load_balancers_dict

        # without atomic action
        return_load_balancers_list = self.scenario._load_balancer_list()
        self.assertEqual(load_balancers_list,
                         return_load_balancers_list["loadbalancers"])

        # with atomic action
        return_load_balancers_list = self.scenario._load_balancer_list()
        self.assertEqual(load_balancers_list,
                         return_load_balancers_list["loadbalancers"])
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_list", count=2)

    def test__load_balancer_show(self):
        load_balancer = {
            "loadbalancer": {
                "id": "lb-id"
            }
        }

        return_load_balancer = self.scenario._load_balancer_show(
            load_balancer["loadbalancer"]["id"])
        self.assertEqual(
            self.clients("octavia").load_balancer_show.return_value,
            return_load_balancer)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_show")

    def test__load_balancer_stats_show(self):
        load_balancer = {
            "loadbalancer": {
                "id": "another-lb-id"
            }
        }

        return_load_balancer = self.scenario._load_balancer_stats_show(
            load_balancer["loadbalancer"]["id"])
        self.assertEqual(
            self.clients("octavia").load_balancer_stats_show.return_value,
            return_load_balancer)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_stats_show")

    def test__load_balancer_set(self):
        expected_load_balancer = {
            "loadbalancer": {
                "name": self.scenario.generate_random_name.return_value,
                "subnet_id": "subnet-id"
            }
        }

        self.clients(
            "octavia").load_balancer_set.return_value = expected_load_balancer
        load_balancer = {"loadbalancer": {"id": "fake-lb-id"}}
        load_balancer_update_args = {"name": "random_name",
                                     "subnet_id": "subnet-id"}
        result_lb = self.scenario._load_balancer_set(
            load_balancer["loadbalancer"]["id"], load_balancer_update_args)
        self.clients("octavia").load_balancer_set.assert_called_once_with(
            load_balancer["loadbalancer"]["id"], json=expected_load_balancer)
        self.assertEqual(
            expected_load_balancer["loadbalancer"]["name"],
            result_lb["loadbalancer"]["name"])
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_set")

    def test__load_balancer_delete(self):
        load_balancer_create_args = {}
        load_balancer = self.scenario._load_balancer_create(
            load_balancer_create_args)
        self.scenario._load_balancer_delete(load_balancer)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.load_balancer_delete")

    def test__pool_create(self):
        self.clients(
            "octavia").pool_create.return_value = self.pool
        pool_data = {"lb_id": "lb-id",
                     "protocol": "HTTPS",
                     "lb_algorithm": "ROUND_ROBIN"}
        expected_pool_data = {"pool": pool_data}
        pool = self.scenario._pool_create(pool_data["lb_id"], pool_data)
        self.assertEqual(self.pool, pool)
        self.clients("octavia").pool_create.assert_called_once_with(
            json=expected_pool_data)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.pool_create")

    def test__pool_list(self):
        pool_list = []
        pool_dict = {"pools": pool_list}
        self.clients(
            "octavia").pool_list.return_value = pool_dict

        # without atomic action
        return_pool_list = self.scenario._pool_list()
        self.assertEqual(pool_list,
                         return_pool_list["pools"])

        # with atomic action
        return_pool_list = self.scenario._pool_list()
        self.assertEqual(pool_list,
                         return_pool_list["pools"])
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.pool_list", count=2)

    def test__pool_show(self):
        pool = {
            "pool": {
                "id": "lb-id"
            }
        }

        return_pool = self.scenario._pool_show(
            pool["pool"]["id"])
        self.assertEqual(
            self.clients("octavia").pool_show.return_value,
            return_pool)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.pool_show")

    def test__pool_set(self):
        expected_pool = {
            "pool": {
                "name": "pool-name",
                "lb_id": "lb-id",
                "protocol": "HTTPS",
                "lb_algorithm": "ROUND_ROBIN"
            }
        }

        self.clients(
            "octavia").pool_set.return_value = expected_pool
        pool = {"pool": {"id": "fake-pool-id"}}
        pool_update_args = {"protocol": "HTTPS",
                            "lb_id": "lb-id",
                            "lb_algorithm": "ROUND_ROBIN",
                            "name": "pool-name"}
        result_pool = self.scenario._pool_set(
            pool["pool"]["id"], pool_update_args)
        self.clients("octavia").pool_set.assert_called_once_with(
            pool["pool"]["id"], json=expected_pool)
        self.assertEqual(
            expected_pool["pool"]["protocol"],
            result_pool["pool"]["protocol"])
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.pool_set")

    def test__pool_delete(self):
        pool_create_args = {}
        pool = self.scenario._pool_create(
            "fake-id",
            pool_create_args)
        self.scenario._pool_delete(pool)
        self._test_atomic_action_timer(self.scenario.atomic_actions(),
                                       "octavia.pool_delete")

    def test__update_load_balancer_resource(self):
        lb = {"id": "1", "provisioning_status": "READY"}
        new_lb = {"id": "1", "provisioning_status": "ACTIVE"}
        self.clients("octavia").load_balancer_show.return_value = new_lb

        return_lb = self.scenario._update_load_balancer_resource(lb)

        self.clients("octavia").load_balancer_show.assert_called_once_with(
            lb["id"])
        self.assertEqual(new_lb, return_lb)
