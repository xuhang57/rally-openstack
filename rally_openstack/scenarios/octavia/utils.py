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

from rally import exceptions

from rally.common import cfg
from rally.common import logging
from rally.task import atomic
from rally.task import utils

from rally_openstack import scenario


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class OctaviaScenario(scenario.OpenStackScenario):
    """Base class for Octavia scenarios with basic atomic actions."""

    @atomic.action_timer("octavia.load_balancer_create")
    def _load_balancer_create(self, load_balancer_create_args):
        """Create octavia load balancer

        :param loadbalancer_create_args: dict
        POST /v2/lbaas/loadbalancers request options
        :returns:
            Octavia load balancer dict
        """
        load_balancer_create_args["name"] = self.generate_random_name()
        return self.clients("octavia").load_balancer_create(
            json={"loadbalancer": load_balancer_create_args})

    @atomic.action_timer("octavia.load_balancer_list")
    def _load_balancer_list(self, **kwargs):
        """Return user load balancers list

        :param kwargs:  octavia load balancer list options
        :returns:
            User load balancers list
        """
        return self.clients("octavia").load_balancer_list(**kwargs)

    @atomic.action_timer("octavia.load_balancer_set")
    def _load_balancer_set(self, lb_id, lb_update_args):
        """Update a load balancer's settings

        :param lb_id: string
        :param lb_update_args: dict
            PUT /v2/lbaas/loadbalancers/{lb_id} request options
        :return:
            API Response Code
        """
        return self.clients("octavia").load_balancer_set(
            lb_id, json={"loadbalancer": lb_update_args})

    @atomic.action_timer("octavia.load_balancer_stats_show")
    def _load_balancer_stats_show(self, lb_id, **kwargs):
        """Shows the current statistics for a load balancer.

        :param lb_id: string
            POST /v2/lbaas/loadbalancer/{ib_id} request options
        :return:
            A dict of the specified load balancer's statistics
        """
        return self.clients("octavia").load_balancer_stats_show(
            lb_id, **kwargs)

    @atomic.action_timer("octavia.load_balancer_show")
    def _load_balancer_show(self, lb_id):
        """Show a load balancer

        :param lb_id: string
            POST /v2/lbaas/loadbalancer/{ib_id} request options
        :return:
            A dict of the specified load balancer's settings
        """
        return self.clients("octavia").load_balancer_show(lb_id)

    @atomic.action_timer("octavia.load_balancer_delete")
    def _load_balancer_delete(self, lb_id, cascade=False):
        """Delete a load balancer

        :param lb_id: string
            DELETE /v2/lbaas/loadbalancers/{lb_id}
        :return:
            API Response Code
        """
        return self.clients("octavia").load_balancer_delete(
            lb_id, cascade=cascade)

    @atomic.action_timer("octavia.wait_for_loadbalancers")
    def _wait_for_loadbalancer_prov_status(self, lb, prov_status="ACTIVE"):
        return utils.wait_for_status(
            lb["loadbalancer"],
            ready_statuses=[prov_status],
            status_attr="provisioning_status",
            update_resource=self._update_load_balancer_resource,
            timeout=CONF.openstack.octavia_create_loadbalancer_timeout,
            check_interval=(
                CONF.openstack.octavia_create_loadbalancer_poll_interval)
        )

    def _update_load_balancer_resource(self, lb):
        try:
            new_lb = self.clients("octavia").load_balancer_show(
                lb["id"])
        except Exception as e:
            if getattr(e, "status_code", 400) == 404:
                raise exceptions.GetResourceNotFound(resource=lb)
            raise exceptions.GetResourceFailure(resource=lb, err=e)
        return new_lb

    @atomic.action_timer("octavia.pool_create")
    def _pool_create(self, lb_id, pool_create_args):
        """Create a pool

        :param lb_id: UUID of the loadbalancer
        :param pool_create_args: dict
            POST /v2/lbaas/pool/ request options
        :return:
            A dict of the created pool's settings
        """
        pool_create_args["name"] = self.generate_random_name()
        pool_create_args["loadbalancer_id"] = lb_id
        return self.clients("octavia").pool_create(
            json={"pool": pool_create_args})

    @atomic.action_timer("octavia.pool_list")
    def _pool_list(self, **kwargs):
        """List all pools

        :param kwargs:
            Parameters to filter on
        :return:
            List of pools
        """
        return self.clients("octavia").pool_list(**kwargs)

    @atomic.action_timer("octavia.pool_show")
    def _pool_show(self, pool_id):
        """Show a pool's settings

        :param string pool_id:
            UUID of the pool to show
        :return:
            Dict of the specified pool's settings
        """
        return self.clients("octavia").pool_show(pool_id)

    @atomic.action_timer("octavia.pool_set")
    def _pool_set(self, pool_id, pool_update_args):
        """Update a pool's settings

        :param pool_id:
            UUID of the pool to update
        :param pool_update_args:
            A dict of arguments to update a pool
        :return:
            API Response Code
        """
        return self.clients("octavia").pool_set(
            pool_id, json={"pool": pool_update_args})

    @atomic.action_timer("octavia.pool_delete")
    def _pool_delete(self, pool_id):
        """Delete a pool

        :param string pool_id:
            UUID of of pool to delete
        :return:
            Response Code from the API
        """
        return self.clients("octavia").pool_delete(pool_id)

    @atomic.action_timer("octavia.wait_for_pools")
    def _wait_for_pool_prov_status(self, pool, prov_status="ACTIVE"):
        return utils.wait_for_status(
            pool["pool"],
            ready_statuses=[prov_status],
            status_attr="provisioning_status",
            update_resource=self._update_pool_resource,
            timeout=CONF.openstack.octavia_create_pool_timeout,
            check_interval=(
                CONF.openstack.octavia_create_pool_poll_interval)
        )

    def _update_pool_resource(self, pool):
        try:
            new_pool = self.clients("octavia").pool_show(
                pool["id"])
        except Exception as e:
            if getattr(e, "status_code", 400) == 404:
                raise exceptions.GetResourceNotFound(resource=pool)
            raise exceptions.GetResourceFailure(resource=pool, err=e)
        return new_pool
