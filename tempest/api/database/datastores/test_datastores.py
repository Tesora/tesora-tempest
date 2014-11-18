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


def _get_ref_datastore_id(datastore_client, db_datastore_ref):
    """
    Helper function that iterates through all available datastores and
    checks if referenced datastore is available or not.
    """
    datastore_id = None
    resp, datastores = datastore_client.list_datastores()
    if resp.status != 200:
        raise AssertionError("Response status 200 expected, got '%d'" %
                             resp.status)
    if len(datastores) < 1:
        raise AssertionError("No datastores found")
    LOG.debug('Available datastores are: %s' % str(datastores))
    for datastore in datastores:
        if db_datastore_ref == datastore['name']:
            datastore_id = datastore['id']
            break
    if not datastore_id:
        raise AssertionError("Could not found referenced datastore '%s' " %
                             db_datastore_ref)
    return datastore_id

def _get_ref_datastore_version_id(datastore_client, datastore_id):
    """
    Helper function to get datastore version id for referenced datastore.
    """
    datastore_versoin_id = None
    if datastore_id:
        resp, body = datastore_client.list_datastore_versions(datastore_id)
        if resp.status != 200:
            raise AssertionError("Response status 200 expected, got '%d'" %
                resp.status)
        LOG.debug('Datastore versions are: %s' % str(body))
        for ds_dict in body:
            if datastore_id == ds_dict['datastore']:
                datastore_version_id = ds_dict['id']
                break
    if not datastore_version_id:
        raise AssertionError(
            "Could not find version id for datastore id '%s'" % datastore_id)
    return datastore_version_id

class DatabaseDatastoresTest(base.BaseDatabaseTest):
    _interface = 'json'

    @classmethod
    def setUpClass(cls):
        super(DatabaseDatastoresTest, cls).setUpClass()
        cls.client = cls.database_datastores_client
        cls.datastore_id = None
        cls.datastore_ver_id = None

    def _set_ref_datastore_id(self):
        """Cache the reference datastore id."""
        if not self.datastore_id:
            self.datastore_id = _get_ref_datastore_id(
                self.database_datastores_client, self.db_datastore_ref)

    def _set_ref_datastore_version_id(self):
        """Cache the reference datastore version id."""
        if not self.datastore_id:
            self._set_ref_datastore_id()
        if not self.datastore_ver_id:
            self.datastore_ver_id = _get_ref_datastore_version_id(
                self.database_datastores_client, self.datastore_id)

    @test.attr(type='smoke')
    def test_list_datastores(self):
        """This function verifies if referenced datastore is available."""
        self._set_ref_datastore_id()

    @test.attr(type='smoke')
    def test_get_datastore_details(self):
        """
        This function verifies datastore details for referenced datastore.
        """
        self._set_ref_datastore_id()
        resp, body = self.client.get_datastore_details(self.datastore_id)
        self.assertEqual(200, resp.status)
        LOG.debug('Datastore details are: %s' % str(body))
        self.assertEqual(self.db_datastore_ref, body['name'])

    @test.attr(type='smoke')
    def test_list_datastore_versions(self):
        """
        This function verifies datastore versions for referenced datastore.
        """
        self._set_ref_datastore_version_id()

    @test.attr(type='smoke')
    def test_get_datastore_version_details(self):
        """
        This function gets datastore version details for referenced datastore.
        """
        self._set_ref_datastore_version_id()
        resp, body = self.client.get_datastore_version_details(
            self.datastore_id, self.datastore_ver_id)
        self.assertEqual(200, resp.status)
        LOG.debug('Datastore version details are: %s' % str(body))
        self.assertEqual(self.datastore_id, body['datastore'])
