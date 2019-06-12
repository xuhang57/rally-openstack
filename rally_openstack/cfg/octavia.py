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

from rally.common import cfg

OPTS = {"openstack": [
    cfg.FloatOpt("octavia_create_loadbalancer_timeout",
                 default=float(500.0),
                 help="Octavia create loadbalancer timeout"),
    cfg.FloatOpt("octavia_delete_loadbalancer_timeout",
                 default=float(50.0),
                 help="Octavia delete loadbalancer timeout"),
    cfg.FloatOpt("octavia_create_loadbalancer_poll_interval",
                 default=float(2.0),
                 help="Octavia create loadbalancer poll interval"),
    cfg.FloatOpt("octavia_create_pool_timeout",
                 default=float(500.0),
                 help="Octavia create pool timeout"),
    cfg.FloatOpt("octavia_create_pool_poll_interval",
                 default=float(2.0),
                 help="Octavia create pool poll interval")
]}
