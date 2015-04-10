#!/usr/bin/env python

#
"""
Simple application that logs on to the APIC and creates a tenant.
"""
import sys
import acitoolkit.acitoolkit as ACI

# Define static values to pass (edit these if you wish to set differently)
DEFAULT_TENANT_NAME = 'aaa111'

# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Simple application that logs on to the APIC and displays all of the Tenants.'
creds = ACI.Credentials('apic', description)
creds.add_argument('-t', '--tenant', help='The name of tenant',
                default=DEFAULT_TENANT_NAME)
args = creds.get()

# Login to APIC
session = ACI.Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

# Download all of the tenants
print 'Content-type: text/html\n'
print '<pre>'

# Create the Tenant
tenant = aci.Tenant(args.tenant)
    
resp = session.push_to_apic(tenant.get_url(),
                            tenant.get_json())
if not resp.ok:
    print('%% Error: Could not push configuration to APIC')
    print(resp.text)

else:
    print("Tenant created:", args.tenant)
    print("<br>")

    
print '<p><p><button onclick="goBack()">Go Back</button><script>function goBack() { window.history.back(); } </script>'
print '</pre>'





