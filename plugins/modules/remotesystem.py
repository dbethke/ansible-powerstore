#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies
# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: remotesystem
version_added: '1.4.0'
short_description: Remote system operations on a PowerStore storage system
description:
- Performs all remote system operations on a PowerStore Storage System.
- This module supports get details of a remote systems, create/Add new
  remote system for all supported parameters, modify remote system with
  supported parameters and delete/remove a remote system.
extends_documentation_fragment:
  - dellemc.powerstore.powerstore
author:
- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>
options:
  remote_name:
    description:
    - Name of the remote system.
    - Parameter I(remote_name) cannot be mentioned during addition of a new
      remote system.
    type: str
  remote_id:
    description:
    - ID of the remote system.
    - ID for the remote system is autogenerated, cannot be passed during
      creation of a remote system.
    - Parameter I(remote_id) and I(remote_address) are mutually exclusive.
    type: str
  remote_user:
    description:
    - Username used in basic authentication to remote PowerStore cluster.
    - It can be mentioned only during creation of the remote system.
    type: str
  remote_password:
    description:
    - Password used in basic authentication to remote PowerStore cluster.
    - It can be mentioned only during creation of the remote system.
    type: str
  remote_address:
    description:
    - Management IP of the remote system.
    - Parameter I(remote_id) and I(remote_address) are mutually exclusive.
    type: str
  new_remote_address:
    description:
    - New management IP of the remote system.
    type: str
  remote_port:
    description:
    - Remote system's port number.
    - It can be mentioned only during creation of the remote system.
    type: int
    default: 443
  description:
    description:
    - Additional information about the remote system.
    - To remove the description empty string is to be passed.
    type: str
  network_latency:
    description:
    - Replication traffic can be tuned for higher efficiency depending on
      the expected network latency.
    - Setting to low will have latency of less than five milliseconds.
    - Setting to high will have latency of more than five milliseconds.
    type: str
    choices: [Low, High]
  wait_for_completion:
    description:
    - Flag to indicate if the operation should be run synchronously or
      asynchronously.
    - C(true) signifies synchronous execution.
    - By default, modify and delete operation will run asynchronously.
    type: bool
    choices: [true, false]
    default: false
  state:
    description:
    - The state of the remote system after the task is performed.
    - For Delete operation only, it should be set to C(absent).
    - For all Create, Modify or Get details operations it should be set to
      C(present).
    required : true
    choices: [ present, absent]
    type: str
notes:
- The module support allows create/delete/update only for remote PowerStore
  arrays.
- Get details can be done for all type of remote arrays.
- Parameters I(remote_user), I(remote_port) and I(remote_password) are not required
  during modification, getting and deleting. If passed then these parameters
  will be ignored and the operation will be performed.
- If I(wait_for_completion) is set to C(true) then the connection will be terminated
  after the timeout is exceeded. User can tweak timeout and pass it
  in the playbook task.
- By default, the timeout is set to 120 seconds.
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''

- name: Add a new remote system
  dellemc.powerstore.remotesystem:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    remote_address: "xxx.xxx.xxx.xxx"
    remote_user: "admin"
    remote_password: "{{remote_password}}"
    remote_port: 443
    network_latency: "Low"
    decription: "Adding a new remote system"
    state: "present"

- name: Modify attributes of remote system using remote_id
  dellemc.powerstore.remotesystem:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    remote_id: "7d7e7917-735b-3eef-8cc3-1302001c08e7"
    remote_address: "xxx.xxx.xxx.xxx"
    network_latency: "Low"
    wait_for_completion: true
    timeout: 300
    decription: "Updating the description"
    state: "present"

- name: Get details of remote system using remote_id
  dellemc.powerstore.remotesystem:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    remote_id: "D7d7e7917-735b-3eef-8cc3-1302001c08e7"
    state: "present"

- name: Delete remote system using remote_id
  dellemc.powerstore.remotesystem:
    array_ip: "{{array_ip}}"
    validate_certs: "{{validate_certs}}"
    user: "{{user}}"
    password: "{{password}}"
    remote_id: "D7d7e7917-735b-3eef-8cc3-1302001c08e7"
    state: "absent"
'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
job_details:
    description: Details of the job.
    returned: When wait_for_completion is not set to True.
    type: complex
    contains:
        id:
            description: The id of the job.
            type: str
    sample: {
        "description_l10n": "Modify network parameters.",
        "end_time": "2022-01-06T07:39:05.846+00:00",
        "estimated_completion_time": null,
        "id": "be0d099c-a6cf-44e8-88d7-9be80ccae369",
        "parent_id": null,
        "phase": "Completed",
        "phase_l10n": "Completed",
        "progress_percentage": 100,
        "resource_action": "modify",
        "resource_action_l10n": "modify",
        "resource_id": "nw6",
        "resource_name": null,
        "resource_type": "network",
        "resource_type_l10n": "network",
        "response_body": null,
        "response_status": null,
        "response_status_l10n": null,
        "root_id": "be0d099c-a6cf-44e8-88d7-9be80ccae369",
        "start_time": "2022-01-06T07:39:05.47+00:00",
        "state": "COMPLETED",
        "state_l10n": "Completed",
        "step_order": 23792565,
        "user": "admin"
    }

remote_system_details:
    description: Details of the remote system.
    returned: When remote system exists
    type: complex
    contains:
        id:
            description: The system generated ID of the remote system.
            type: str
        name:
            description: Name of the remote system.
            type: str
        management_address:
            description: The management cluster IP address of the remote system.
            type: str
        description:
            description: User-specified description of the remote system instance.
            type: str
        serial_number:
            description: Serial number of the remote system instance.
            type: str
        version:
            description:
                - Version of the remote system.
                - It was added in PowerStore version 2.0.0.0.
            type: str
        type:
            description: Remote system connection type between the local system.
            type: str
        user_name:
            description: Username used to access the non-PowerStore remote systems.
            type: str
        state:
            description:
                - Possible remote system states.
                - OK, Normal conditions.
                - Update_Needed, Verify and update needed to handle network configuration changes on the systems.
                - Management_Connection_Lost, Management connection to the remote peer is lost.
            type: str
        data_connection_state:
            description:  Data connection states of a remote system.
            type: str
        discovery_chap_mode:
            description: Challenge Handshake Authentication Protocol (CHAP) statu.
            type: str
        session_chap_mode:
            description: Challenge Handshake Authentication Protocol (CHAP) status.
            type: str
        data_network_latency:
            description:
                - Network latency choices for a remote system. Replication traffic can be tuned for higher efficiency
                  depending on the expected network latency.
                - This will only be used when the remote system type is PowerStore.
            type: str
        data_connections:
            description:
                - List of data connections from each appliance in the local cluster to iSCSI target IP address.
            type: complex
            contains:
                node_id:
                    description: Unique identifier of the local, initiating node.
                    type: str
                initiator_address:
                    description: Initiating address from the local node.
                    type: str
                status:
                    description: Possible transit connection statuses.
                    type: str
                target_address:
                    description: Target address from the remote system.
                    type: str
    sample: {
        "data_connection_state": "Initializing",
        "data_connection_state_l10n": "Initializing",
        "data_connections": null,
        "data_network_latency": "Low",
        "data_network_latency_l10n": "Low",
        "description": "Adding remote system",
        "discovery_chap_mode": "Disabled",
        "discovery_chap_mode_l10n": "Disabled",
        "id": "aaa3cc6b-455b-4bde-aa75-a1edf61bbe0b",
        "import_sessions": [],
        "iscsi_addresses": [
            "xx.xx.xx.xx",
            "xx.xx.xx.xx"
        ],
        "management_address": "xx.xx.xx.xx",
        "name": "RT-D0100",
        "replication_sessions": [],
        "serial_number": "PSeba1a5c63d46",
        "session_chap_mode": "Disabled",
        "session_chap_mode_l10n": "Disabled",
        "state": "Ok",
        "state_l10n": "Ok",
        "type": "PowerStore",
        "type_l10n": "PowerStore",
        "user_name": ""
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerstore.plugins.module_utils.storage.dell\
    import utils

LOG = utils.get_logger('remotesystem')

py4ps_sdk = utils.has_pyu4ps_sdk()
HAS_PY4PS = py4ps_sdk['HAS_Py4PS']
IMPORT_ERROR = py4ps_sdk['Error_message']

py4ps_version = utils.py4ps_version_check()
IS_SUPPORTED_PY4PS_VERSION = py4ps_version['supported_version']
VERSION_ERROR = py4ps_version['unsupported_version_message']

# Application type
APPLICATION_TYPE = 'Ansible/3.3.0'


class PowerstoreRemoteSystem(object):
    """Remote system operations"""
    cluster_name = ' '
    cluster_global_id = ' '

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_powerstore_management_host_parameters()
        self.module_params.update(get_powerstore_remote_system_parameters())

        # initialize the Ansible module
        mut_ex_args = [['remote_id', 'remote_address']]
        # in case of create remote address and remote port may also be needed.
        # These operation specific parameters validation will be done separately.
        required_together = [['remote_user', 'remote_password']]
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mut_ex_args,
            required_together=required_together
        )
        LOG.info('HAS_PY4PS = %s , IMPORT_ERROR = %s', HAS_PY4PS,
                 IMPORT_ERROR)
        if HAS_PY4PS is False:
            self.module.fail_json(msg=IMPORT_ERROR)
        LOG.info('IS_SUPPORTED_PY4PS_VERSION = %s , VERSION_ERROR = '
                 '%s', IS_SUPPORTED_PY4PS_VERSION, VERSION_ERROR)
        if IS_SUPPORTED_PY4PS_VERSION is False:
            self.module.fail_json(msg=VERSION_ERROR)

        self.conn = utils.get_powerstore_connection(
            self.module.params, application_type=APPLICATION_TYPE)
        self.provisioning = self.conn.provisioning
        LOG.info('Got Py4ps instance for provisioning on PowerStore %s',
                 self.provisioning)
        self.protection = self.conn.protection
        LOG.info('Got Py4ps instance for protection on PowerStore %s',
                 self.protection)
        self.configuration = self.conn.config_mgmt
        LOG.info('Got Py4ps instance for configuration on PowerStore %s',
                 self.configuration)

    def get_remote_system_details(self, remote_sys_name=None,
                                  remote_sys_address=None, remote_sys_id=None):
        """Get remote system details by name or id"""
        try:
            LOG.info('Getting the details of remote system, Name:%s ,'
                     'address:%s, ID:%s', remote_sys_name,
                     remote_sys_address, remote_sys_id)
            if remote_sys_address:
                resp = \
                    self.protection.\
                    get_remote_system_by_mgmt_address(
                        remote_sys_address)
                if resp:
                    LOG.info('Successfully got the details of remote system '
                             'with address: %s', remote_sys_address)
                    return resp[0]

            else:
                resp = self.protection.get_remote_system_details(
                    remote_sys_id)
                if resp:
                    LOG.info('Successfully got the details of replication '
                             'rule with id: %s', remote_sys_id)
                    return resp

            msg = 'No remote system present with name {0} or ID {1}'.format(
                remote_sys_name, remote_sys_id)
            LOG.info(msg)
            return resp

        except Exception as e:
            msg = 'Get details of remote system name: {0} or ID {1}' \
                  'failed with' \
                  ' error : {2} '.format(remote_sys_name, remote_sys_id,
                                         str(e))
            if isinstance(e, utils.PowerStoreException) and \
                    e.err_code == utils.PowerStoreException.HTTP_ERR and \
                    e.status_code == "404":
                LOG.info(msg)
                return None
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def exchange_certificates(self, remote_user, remote_password,
                              remote_address, remote_port):
        """
        Exchange certificates for creation/addition of new
        remote system.
        """
        try:
            LOG.info("Exchanging certifications for"
                     " creation of remote system")
            exchange_cert_dict = {
                'address': remote_address,
                'port': remote_port,
                'username': remote_user,
                'password': remote_password,
                'service': "Replication_HTTP"
            }
            self.configuration.exchange_certificate(exchange_cert_dict)

        except Exception as e:
            msg = 'Exchange certificate on PowerStore array ' \
                  'failed with error {0}'.format(str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def create_remote_system(self, remote_address=None, description=None,
                             network_latency=None):
        """ Create remote system """
        try:
            LOG.info('Creating a remote system')
            create_remote_sys_dict = {
                'management_address': remote_address,
                'description': description,
                'data_network_latency': network_latency
            }
            resp = self.protection.create_remote_system(
                create_remote_sys_dict)

            remote_sys_details = \
                self.protection.get_remote_system_details(resp.get('id'))
            LOG.info(
                'Successfully created remote system, id: %s'
                ' on PowerStore array', resp.get("id"))
            return True, remote_sys_details

        except Exception as e:
            msg = 'create remote system failed with error ' \
                  '{0}'.format(str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def modify_remote_system(self, remote_sys_id, modify_dict, is_async):
        """ Modify an existing remote system of a given PowerStore storage
        system """

        try:
            LOG.info('Modifying an existing remote system')
            resp = self.protection.modify_remote_system(
                remote_sys_id, modify_dict, is_async)
            LOG.info(
                'Successfully modified remote system id %s',
                remote_sys_id)
            return True, resp

        except Exception as e:
            msg = 'Modify remote system id: {0} failed with error ' \
                  '{1}'.format(remote_sys_id, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def delete_remote_system(self, remote_sys_id, is_async):
        """ Delete a remote system by id of a given PowerStore storage
         system """

        try:
            LOG.info('Deleting remote system id %s', remote_sys_id)
            delete_resp = self.protection.delete_remote_system(
                remote_sys_id, is_async)

            LOG.info('Successfully deleted remote system with id: %s',
                     remote_sys_id)
            return True, delete_resp

        except Exception as e:
            msg = 'Delete remote system with id: {0} failed with error ' \
                  '{1} '.format(remote_sys_id, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def get_clusters(self):
        """Get the clusters"""
        try:
            clusters = self.provisioning.get_cluster_list()
            return clusters

        except Exception as e:
            msg = 'Failed to get the clusters with ' \
                  'error {0}'.format(str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg, **utils.failure_codes(e))

    def perform_module_operation(self):
        """collect input"""
        remote_sys_user = self.module.params['remote_user']
        remote_sys_password = self.module.params['remote_password']
        remote_sys_port = self.module.params['remote_port']
        remote_sys_name = self.module.params['remote_name']
        remote_sys_id = self.module.params['remote_id']
        remote_sys_address = self.module.params['remote_address']
        new_remote_sys_address = self.module.params['new_remote_address']
        description = self.module.params['description']
        network_latency = self.module.params['network_latency']
        wait_for_completion = self.module.params['wait_for_completion']
        state = self.module.params['state']

        # set async according to wait_for_completion
        is_async = True
        if wait_for_completion is not None:
            is_async = not wait_for_completion

        result = dict()
        changed = False
        job_id = None

        # Get the cluster details
        clusters = self.get_clusters()
        if len(clusters) > 0:
            self.cluster_name = clusters[0]['name']
            self.cluster_global_id = clusters[0]['id']
        else:
            msg = "Unable to find any active cluster on this array"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        if remote_sys_name and not remote_sys_address and not remote_sys_id:
            self.module.fail_json(
                msg="With remote_name, remote_address or remote_id"
                    " is required to perform Get/Update/Delete.")

        # Get the details of the remote system
        remote_sys_details = self.get_remote_system_details(
            remote_sys_name, remote_sys_address, remote_sys_id)
        if remote_sys_details:
            if not remote_sys_id:
                remote_sys_id = remote_sys_details['id']
            if remote_sys_name and \
                    remote_sys_name != remote_sys_details['name']:
                self.module.fail_json(
                    msg="Please enter a valid remote_name. It is not matching the"
                        " fetched remote system instance")
            if not remote_sys_name:
                remote_sys_name = remote_sys_details['name']
                if not remote_sys_address:
                    remote_sys_address = \
                        remote_sys_details['management_address']

        # Create a remote system
        if not remote_sys_details and state == "present":
            if remote_sys_id or remote_sys_name:
                msg = "remote_id/remote_name cannot be passed" \
                      " during creation. Please enter valid" \
                      " parameters for creation of remote system."
                self.module.fail_json(msg=msg)

            # exchange the certificates
            self.exchange_certificates(
                remote_sys_user, remote_sys_password,
                remote_sys_address, remote_sys_port)
            # creating a remote system after successful
            # exchange of certificates
            changed, remote_sys_details = self.create_remote_system(
                remote_sys_address, description, network_latency)
            remote_sys_id = remote_sys_details['id']

        # Delete a remote system
        if remote_sys_details and state == "absent":
            changed, job_id = self.delete_remote_system(remote_sys_id,
                                                        is_async)
            remote_sys_details = None

        # Update the details of remote system
        if remote_sys_details and state == "present":
            modify_remote_sys_dict = {
                'management_address': new_remote_sys_address,
                'description': description,
                'data_network_latency': network_latency
            }

            to_modify = modify_remote_system_required(
                remote_sys_details, modify_remote_sys_dict)
            LOG.debug("To modify : %s", to_modify)

            if to_modify:
                changed, resp = \
                    self.modify_remote_system(
                        remote_sys_id, modify_remote_sys_dict, is_async)
                if is_async:
                    job_id = resp
                else:
                    remote_sys_details = self.get_remote_system_details(
                        remote_sys_id=remote_sys_id)

        result['changed'] = changed
        result['job_details'] = job_id
        if not job_id:
            result['remote_system_details'] = remote_sys_details

        self.module.exit_json(**result)


def modify_remote_system_required(remote_sys_details, passed_args):
    """ To check if modification is required or not"""
    for key in remote_sys_details.keys():
        if key in passed_args.keys() and\
                passed_args[key] is not None and\
                remote_sys_details[key] != passed_args[key]:
            LOG.debug("Key %s in remote_sys_details=%s,"
                      "passed_args=%s", key,
                      remote_sys_details[key], passed_args[key])
            return True
    return False


def get_powerstore_remote_system_parameters():
    """This method provide the parameters required for the remote system
     operations for PowerStore"""

    return dict(
        remote_id=dict(), remote_name=dict(),
        remote_user=dict(), remote_password=dict(no_log=True),
        remote_address=dict(), new_remote_address=dict(),
        remote_port=dict(default=443, type='int'), description=dict(),
        network_latency=dict(required=False, type='str',
                             choices=['Low', 'High']),
        wait_for_completion=dict(required=False, type='bool',
                                 choices=[True, False], default=False),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerStore remote system object and perform action on it
        based on user input from playbook """
    obj = PowerstoreRemoteSystem()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
