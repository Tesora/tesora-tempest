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

from tempest.api.database import base
from tempest.openstack.common import log as logging
from tempest import test

LOG = logging.getLogger(__name__)


class DatabaseDatastoresTest(base.BaseDatabaseTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(DatabaseDatastoresTest, cls).setUpClass()
        cls.client = cls.database_datastores_client
        cls.datastore_id = None
        cls.datastore_ver_id = None

    def _get_ref_datastore(self):
        """
        Helper function that iterates through all available datastores and
        checks if referenced datastore is available or not.
        """
        if not self.datastore_id:
            resp, datastores = self.client.list_datastores()
            self.assertEqual(200, resp.status)
            LOG.debug('Available datastore are: %s' % str(datastores))
            self.assertTrue(len(datastores) > 0, "No datastores found")
            for datastore in datastores:
                if self.db_datastore_ref == datastore['name']:
                    self.datastore_id = datastore['id']
                    break
            self.assertTrue(self.datastore_id,
                            "Could not found referenced datastore '%s' " %
                            self.db_datastore_ref)

    def _get_ref_datastore_version_list(self):
        """
        Helper function to get datastore version id for referenced datastore.
        """
        if not self.datastore_ver_id:
            self._get_ref_datastore()
            resp, body = self.client.list_datastore_versions(self.datastore_id)
            self.assertEqual(200, resp.status)
            LOG.debug('Datastore versions are: %s' % str(body))
            for ds_dict in body:
                if self.datastore_id == ds_dict['datastore']:
                    self.datastore_ver_id = ds_dict['id']
                    break
            self.assertTrue(self.datastore_ver_id,
                            "datastore's version id not found'%s' " %
                            self.db_datastore_ref)

    @test.attr(type='smoke')
    def test_list_datastores(self):
        """This function verifies if referenced datastore is available."""
        self._get_ref_datastore()

    @test.attr(type='smoke')
    def test_get_datastore_details(self):
        """
        This function verifies datastore details for referenced datastore.
        """
        self._get_ref_datastore()
        resp, body = self.client.get_datastore_details(self.datastore_id)
        self.assertEqual(200, resp.status)
        LOG.debug('Datastore details are: %s' % str(body))
        self.assertEqual(self.db_datastore_ref, body['name'])

    @test.attr(type='smoke')
    def test_list_datastore_versions(self):
        """
        This function verifies datastore versions for referenced datastore.
        """
        self._get_ref_datastore_version_list()

    @test.attr(type='smoke')
    def test_get_datastore_version_details(self):
        """
        This function gets datastore version details for referenced datastore.
        """
        self._get_ref_datastore_version_list()
        resp, body = self.client.get_datastore_version_details(
            self.datastore_id, self.datastore_ver_id)
        self.assertEqual(200, resp.status)
        LOG.debug('Datastore version details are: %s' % str(body))
        self.assertEqual(self.datastore_id, body['datastore'])
