# Copyright 2014 Tesora Inc
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

from tempest import test

from tempest.api.database import base
from tempest.api.database.datastores import test_datastores
from tempest.common.utils.data_utils import rand_name
from tempest.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class DatabaseInstancesTest(base.BaseDatabaseTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(DatabaseInstancesTest, cls).setUpClass()
        cls.client = cls.database_instances_client
        cls.instance_id = None
        cls.datastore_id = None
        cls.datastore_version_id = None

    def _set_ref_datastore_id(self):
        if not self.datastore_id:
            self.datastore_id = test_datastores._get_ref_datastore_id(
                self.database_datastores_client, self.db_datastore_ref)

    def _set_ref_datastore_version_id(self):
        if not self.datastore_id:
            self._set_ref_datastore_id()
        if not self.datastore_version_id:
            self.datastore_version_id = (
                test_datastores._get_ref_datastore_version_id(
                    self.database_datastores_client, self.datastore_id))

    def _verify_list_instances(self, count):
        """This function verifies that the list instances is as we expect."""
        resp, body = self.client.list_instances()
        self.assertEqual(200, resp.status)
        self.assertEqual(len(body), count, "Found %d instances - '%s'" %
                         (len(body),str(body)))
        LOG.debug('Trove instance details are: %s' % str(body))

    @test.attr(type='smoke')
    def test_create_instance(self):
        """This function verifies that we can create an instance."""
        self._set_ref_datastore_id()
        self._set_ref_datastore_version_id()
        LOG.debug("Found datastore id '%s', version '%s'" % (
            self.datastore_id, self.datastore_version_id))
        name = "test_inst_%s" % rand_name()
        datastore = {
            'type': self.datastore_id,
            'version': self.datastore_version_id
        }
        volume = {"size": 5}
        resp, body = self.client.create_instance(name, self.db_flavor_ref,
                                                 datastore=datastore,
                                                 volume=volume)
        self.assertEqual(200, resp.status)
        self.assertEqual(self.db_datastore_ref, body['datastore']['type'])
        self._verify_list_instances(1)
