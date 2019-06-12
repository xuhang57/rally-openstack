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

"""Scenarios for Octavia Loadbalancer."""


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_list_loadbalancers",
                    platform="openstack")
class CreateAndListLoadbalancers(octavia_utils.OctaviaScenario,
                                 neutron_utils.NeutronScenario):

    def run(self, load_balancer_create_args=None):
        """Create a load balancer and then list all load balancers

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
        self._load_balancer_list()


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_delete_loadbalancers",
                    platform="openstack")
class CreateAndDeleteLoadbalancers(octavia_utils.OctaviaScenario,
                                   neutron_utils.NeutronScenario):

    def run(self, load_balancer_create_args=None):
        """Create a load balancer per each subnet and delete loadbalancer

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
            self._load_balancer_delete(
                loadbalancer["loadbalancer"]["id"])


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_update_loadbalancers",
                    platform="openstack")
class CreateAndUpdateLoadBalancers(octavia_utils.OctaviaScenario,
                                   neutron_utils.NeutronScenario):

    def run(self, load_balancer_update_args, load_balancer_create_args=None):
        """Create a loadbalancer per each subnet and update loadbalancer

        :param load_balancer_update_args: dict, PUT /v2/lbaas/loadbalancer
                                          update request
        :param load_balancer_create_args: dict, POST /v2/lbaas/loadbalancer
                                          request options
        """
        loadbalancers = []
        subnets = self._list_subnets()
        for subnet in subnets:
            load_balancer_create_args["vip_subnet_id"] = subnet["id"]
            lb = self._load_balancer_create(load_balancer_create_args)
            loadbalancers.append(lb)
        for loadbalancer in loadbalancers:
            self._wait_for_loadbalancer_prov_status(loadbalancer)
            self._load_balancer_set(
                loadbalancer["loadbalancer"]["id"],
                load_balancer_update_args)


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_stats_loadbalancers",
                    platform="openstack")
class CreateAndShowStatsLoadBalancers(octavia_utils.OctaviaScenario,
                                      neutron_utils.NeutronScenario):

    def run(self, load_balancer_create_args=None):
        """Create a loadbalancer per each subnet and stats

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
            self._load_balancer_stats_show(
                loadbalancer["loadbalancer"]["id"])


@validation.add("required_services", services=[consts.Service.OCTAVIA,
                                               consts.Service.NEUTRON])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup@openstack": ["octavia", "neutron"]},
                    name="Octavia.create_and_show_loadbalancers",
                    platform="openstack")
class CreateAndShowLoadBalancers(octavia_utils.OctaviaScenario,
                                 neutron_utils.NeutronScenario):

    def run(self, load_balancer_create_args=None):
        """Create a loadbalancer per each subnet and show

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
            self._load_balancer_show(
                loadbalancer["loadbalancer"]["id"])
