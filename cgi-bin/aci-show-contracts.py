#!/usr/bin/env python
# Copyright (c) 2014, 2015 Cisco Systems, Inc.
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
#
"""
Simple application that logs on to the APIC and displays all
of the Contracts.
"""
import sys
import acitoolkit.acitoolkit as aci

def main():
    """
    Main show contracts routine
    :return: None
    """
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = ('Simple application that logs on to the APIC'
                   'and displays all of the Contracts.')
    creds = aci.Credentials('apic', description)
    args = creds.get()

    # Login to APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    # Download all of the contracts
    # and store the data as tuples in a list
    data = []
    tenants = aci.Tenant.get(session)
    for tenant in tenants:
        contracts = aci.Contract.get(session, tenant)
        for contract in contracts:
            data.append((tenant.name, contract.name))

    # IPython.embed()

    # Display the data downloaded
    print 'Content-type: text/html\n'
    print '<pre>'
    template = '{0:19} {1:20}'
    print(template.format("Tenant", "Contract"))
    print(template.format("------", "--------"))
    for rec in data:
        print template.format(*rec)
        print '<br>'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
