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

import urllib

from tempest.common import rest_client
from tempest import config

CONF = config.CONF


class DatabaseDatastoresClientJSON(rest_client.RestClient):

    def __init__(self, auth_provider):
        super(DatabaseDatastoresClientJSON, self).__init__(auth_provider)
        self.service = CONF.database.catalog_type

    def list_datastores(self, params=None):
        """List all datastores."""
        url = 'datastores'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        return resp, self._parse_resp(body)

    def get_datastore_details(self, datastore_id):
        """Get datastore details for referenced datastore."""
        resp, body = self.get("datastores/%s" % datastore_id)
        return resp, self._parse_resp(body)

    def list_datastore_versions(self, datastore_id):
        """Get datastore version for referenced datastore."""
        resp, body = self.get("datastores/%s/versions" % datastore_id)
        return resp, self._parse_resp(body)

    def get_datastore_version_details(self, datastore_id,
                                      datastore_version_id):
        """Get datastore version details for referenced datastore."""
        resp, body = self.get("datastores/%s/versions/%s"
                              % (datastore_id, datastore_version_id))
        return resp, self._parse_resp(body)
