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

from rally.task import validation

from rally_openstack import consts
from rally_openstack import scenario
from rally_openstack.scenarios.neutron import utils as neutron_utils
from rally_openstack.scenarios.octavia import utils as octavia_utils

"""Scenarios for Octavia Pools."""


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_list_pools",
                    platform="openstack")
class CreateAndListPools(octavia_utils.OctaviaScenario,
                         neutron_utils.NeutronScenario):

    def run(self, pool_create_args, load_balancer_create_args=None):
        """Create a loadbalancer pool per each subnet and then pools.

        :param load_balancer_create_args: dict
            POST /v2/lbaas/loadbalancer request options
        :param pool_create_args: dict
            POST /v2/lbaas/pool request options
        """
        loadbalancers = []
        subnets = self._list_subnets()
        for subnet in subnets:
            load_balancer_create_args["vip_subnet_id"] = subnet["id"]
            lb = self._load_balancer_create(load_balancer_create_args)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self._wait_for_loadbalancer_prov_status(loadbalancer)
            pool = self._pool_create(
                lb_id=loadbalancer["loadbalancer"]["id"],
                pool_create_args=pool_create_args)
            self._wait_for_pool_prov_status(pool)
        self._pool_list()


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_delete_pools",
                    platform="openstack")
class CreateAndDeletePools(octavia_utils.OctaviaScenario,
                           neutron_utils.NeutronScenario):

    def run(self, pool_create_args, load_balancer_create_args=None):
        """Create a pool per each subnet and then delete pool

        :param load_balancer_create_args: dict
            POST /v2/lbaas/loadbalancer request options
        :param pool_create_args: dict
            POST /v2/lbaas/pool request options
        """
        loadbalancers = []
        subnets = self._list_subnets()
        for subnet in subnets:
            load_balancer_create_args["vip_subnet_id"] = subnet["id"]
            lb = self._load_balancer_create(load_balancer_create_args)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self._wait_for_loadbalancer_prov_status(loadbalancer)
            pool = self._pool_create(
                lb_id=loadbalancer["loadbalancer"]["id"],
                pool_create_args=pool_create_args)
            self._wait_for_pool_prov_status(pool)
            self._pool_delete(pool["pool"]["id"])


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_update_pools",
                    platform="openstack")
class CreateAndUpdatePools(octavia_utils.OctaviaScenario,
                           neutron_utils.NeutronScenario):

    def run(self, pool_create_args, pool_update_args,
            load_balancer_create_args=None):
        """Create a pool per each subnet and update

        :param pool_create_args: dict
            POST /v2/lbaas/pool request options
        :param pool_update_args: dict
            PUT /v2/lbaas/pool/{pool_id} request options
        :param load_balancer_create_args: dict
            POST /v2/lbaas/loadbalancer request options
        """
        loadbalancers = []
        subnets = self._list_subnets()
        for subnet in subnets:
            load_balancer_create_args["vip_subnet_id"] = subnet["id"]
            lb = self._load_balancer_create(load_balancer_create_args)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self._wait_for_loadbalancer_prov_status(loadbalancer)
            pool = self._pool_create(
                lb_id=loadbalancer["loadbalancer"]["id"],
                pool_create_args=pool_create_args)
            self._wait_for_pool_prov_status(pool)
            self._pool_set(
                pool_id=pool["pool"]["id"], pool_update_args=pool_update_args)


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_show_pools",
                    platform="openstack")
class CreateAndShowPools(octavia_utils.OctaviaScenario,
                         neutron_utils.NeutronScenario):

    def run(self, pool_create_args, load_balancer_create_args=None):
        """Create a pool per each subnet and show it

        :param load_balancer_create_args: dict
            POST /v2/lbaas/loadbalancer request options
        :param pool_create_args: dict
            POST /v2/lbaas/pool request options
        """
        loadbalancers = []
        subnets = self._list_subnets()
        for subnet in subnets:
            load_balancer_create_args["vip_subnet_id"] = subnet["id"]
            lb = self._load_balancer_create(load_balancer_create_args)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self._wait_for_loadbalancer_prov_status(loadbalancer)
            pool = self._pool_create(
                lb_id=loadbalancer["loadbalancer"]["id"],
                pool_create_args=pool_create_args)
            self._wait_for_pool_prov_status(pool)
            self._pool_show(pool["pool"]["id"])
