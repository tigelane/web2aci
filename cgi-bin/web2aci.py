#!/usr/bin/env python


# Change Log
''' 
    Version 1.0 - Modified from aci-mini tools
'''


import acitoolkit.acitoolkit as ACI
import json
import sys

try:
    import credentials
except:
    pass
        

session = ''
connection_status = 'Disconnected'
url = ''
login = ''
password = ''

def error_message(error):
    '''  Calls and error message.  This takes 1 list argument with 3 components.  #1 is the error number, #2 is the error text, 
         #3 is if the application should continue or not.  Use -1 to kill the application.  Any other number
         continues the application.  You must code in a loop and go back to where you want unless you are exiting.
    '''
    
    print '\n================================='
    print   '  ERROR Number: ' + str(error[0])
    print   '  ERROR Text: ' + str(error[1])
    print '=================================\n'
    
    if error[2] == -1:
        print 'Applicaiton ended due to error.\n'
        sys.exit()

def collect_login():

    global url, login, password
    
    print '\n\n'
    print '===================='
    print '==  Login to ACI  =='
    print '====================\n'

    try:
        url = credentials.URL
        login = credentials.LOGIN
        password = credentials.PASSWORD
        create_login()

    except:
        print "<h2>Error</h2>"
        print "Sorry, I was not able to login to the APIC."
    

def create_login():
    global session, connection_status
    
    print 'In create login'
    
    session = ACI.Session(url, login, password)
    response = session.login()
 
    if not response.ok:
        error_message ([1,'There was an error with the connection to the APIC.', -1])
        return False

    decoded_response = json.loads(response.text)

    if (response.status_code != 200):
        if (response.status_code == 401):
            connection_status = 'Username/Password incorrect'
            return False
        else:
            error_message ([decoded_response['imdata'][0]['error']['attributes']['code'], decoded_response['imdata'][0]['error']['attributes']['text'], -1])
            return False
    
    elif (response.status_code == 200):
        refresh = decoded_response['imdata'][0]['aaaLogin']['attributes']['refreshTimeoutSeconds']
        cookie = response.cookies['APIC-cookie']

        connection_status = 'Connected'
        return True
    else:
        return False
        
    
    return True

def collect_add_server_EPG():
    if not collect_login():
        return False

    tenants_list = []
    apps_list = []
    epgs_list = []
    
    print '\n\n'
    print '====================================='
    print '==  Add physcial server to an EPG  =='
    print '=====================================\n'

    
    tenants = ACI.Tenant.get(session)
    for tenant in tenants:
        tenants_list.append((tenant.name))
    
    for a in range(len(tenants_list)):
        print str(a) + ': ' + tenants_list[a]

    input = raw_input('\nEnter the Tenant #: ')
    tenant_in = 99
    try:
        tenant_in = int(input)
    except:
        pass
    
    print '\n'
    apps = ACI.AppProfile.get(session, tenants[tenant_in])
    for app in apps:
        apps_list.append((app.name))
    
    for a in range(len(apps_list)):
        print str(a) + ': ' + apps_list[a]

    input = raw_input('\nEnter the Application Profile #: ')
    app_in = 99
    try:
        app_in = int(input)
    except:
        pass

    print '\n'
    epgs = ACI.EPG.get(session, apps[app_in], tenants[tenant_in])
    for epg in epgs:
        epgs_list.append((epg.name))
    
    for a in range(len(epgs_list)):
        print str(a) + ': ' + epgs_list[a]

    input = raw_input('\nEnter the End Point Group #: ')
    epg_in = 99
    try:
        epg_in = int(input)
    except:
        pass

    interface = {'type': 'eth',
                 'pod': '1', 
                 'node': '101', 
                 'module': '1', 
                 'port': '8'}
    vlan = {'name': 'vlan5',
            'encap_type': 'vlan',
            'encap_id': '5'}

    input = raw_input('\nPress Enter to continue.')
    create_add_server_EPG(tenants[tenant_in],apps[app_in],epgs[epg_in],interface,vlan)
    # def create_add_server_EPG(tenant_name, app_name, epg_name, interface, vlan):

def create_add_server_EPG(tenant, app, epg, interface, vlan):

    # Create the Tenant, App Profile, and EPG
    #     tenant = ACI.Tenant(tenant_name)
    #     app = ACI.AppProfile(app_name, tenant_name)
    #     epg = ACI.EPG(epg_name, app_name)

    if not connected():
        if not collect_login():
            return

    # Create the physical interface object
    intf = ACI.Interface(interface['type'],
                        interface['pod'],
                        interface['node'],
                        interface['module'],
                        interface['port'])

    # Create a VLAN interface and attach to the physical interface
    vlan_intf = ACI.L2Interface(vlan['name'], 
                                vlan['encap_type'], 
                                vlan['encap_id'])
    vlan_intf.attach(intf)

    # Attach the EPG to the VLAN interface
    epg.attach(vlan_intf)

    # Push it all to the APIC
    response = session.push_to_apic(tenant.get_url(),
                            tenant.get_json())

    decoded_response = json.loads(response.text)

    if not response.ok:
           print '%% Error: Could not push configuration to APIC'
           error_message ([decoded_response['imdata'][0]['error']['attributes']['code'], decoded_response['imdata'][0]['error']['attributes']['text'], -1])

def show_epgs():

    ''' Takes no arguments and returns nothing.  Simple here to show you all of the
            Tenants, Application Profiles, and End Point Groups you have.'
    '''

    data = []
    tenants = ACI.Tenant.get(session)
    for tenant in tenants:
        apps = ACI.AppProfile.get(session, tenant)
        for app in apps:
            epgs = ACI.EPG.get(session, app, tenant)
            for epg in epgs:
                data.append((tenant.name, app.name, epg.name))

    # Display the data downloaded
    template = "{0:19} {1:20} {2:15}"
    print template.format("Tenant", "App Profile", "EPG")
    print template.format("------", "-----------", "---")
    for rec in data:
        print template.format(*rec)



def show_endpoints():
    if not connected():
        if not collect_login():
            return


    # Download all of the end points (devices connected to the fabric)
    # and store the data as tuples in a list
    data = []
    endpoints = ACI.Endpoint.get(session)
    for ep in endpoints:
        epg = ep.get_parent()
        app_profile = epg.get_parent()
        tenant = app_profile.get_parent()
        data.append((ep.mac, ep.ip, ep.if_name, ep.encap, tenant.name, app_profile.name, epg.name))
    
    # Display the data downloaded
    template = "{0:19} {1:17} {2:15} {3:10} {4:10} {5:18} {6:18}"
    print template.format("MACADDRESS",        "IPADDRESS",        "INTERFACE",     "ENCAP",      "TENANT", "APP PROFILE", "EPG")
    print template.format("-----------------", "---------------", "--------------", "----------", "------", "-----------", "---")
    for rec in data:
        print template.format(*rec)
        


    input = raw_input('\nPress Enter to continue ')
    
def get_interfaces():
    # Download all of the interfaces
    # and store the data as tuples in a list
    
    if not connected():
        if not collect_login():
            return

    data = []
    interfaces = ACI.Interface.get(session)
    for interface in interfaces:
      data.append((interface.if_name,
                   interface.porttype,
                   interface.adminstatus,
                   interface.speed,
                   interface.mtu))

    return data

def show_interfaces():
    if not connected():
        if not collect_login():
            return
        
    data = get_interfaces()
    
    # Display the data downloaded
    template = "{0:17} {1:6} {2:6} {3:7} {4:6}"
    print template.format("INTERFACE", "TYPE", "ADMIN", "SPEED", "MTU")
    print template.format("---------", "----", "-----", "-----", "___")
    for rec in data:
        print template.format(*rec)
    

    input = raw_input('\nPress Enter to continue ')

def two_ports():
    if not connected():
        if not collect_login():
            return
        
        
    print '\n\n'
    print '========================='
    print '==  Connect Two Ports  =='
    print '=========================\n'


        
    # Basic Connectivity Example
    # Equivalent to connecting to ports to the same VLAN
    
    new_tenant = raw_input('Please enter a Tenant name: ')
    new_app = raw_input('Please enter an Application name: ')
    new_epg = new_app + '_EPG'

    # Create a tenant
    tenant = ACI.Tenant(new_tenant)

    # Create a Context and a BridgeDomain
    context = ACI.Context('VRF-1', tenant)
    context.set_allow_all()
    bd = ACI.BridgeDomain('BD-1', tenant)
    bd.add_context(context)

    # Create an App Profile and an EPG
    app = ACI.AppProfile(new_app, tenant)
    epg = ACI.EPG(new_epg, app)
    
    interfaces = ACI.Interface.get(session)

    for i in xrange(len(interfaces) - 1, -1, -1):
        if interfaces[i].porttype != 'leaf':
            del interfaces[i]
    
    interface1_in = interface2_in = -1
    
    while interface1_in == -1 or interface2_in == -1:
        for a in range(len(interfaces)):
            name = interfaces[a].if_name
            print str(a) + ': ' + name
        
        input1 = raw_input('\nEnter the first interface: ')
        input2 = raw_input('\nEnter the second interface: ')
        
        try:
            interface1_in = int(input1)
            interface2_in = int(input2)
            if (0 > interface1_in >len(interfaces)) or (0 > interface1_in >len(interfaces)):
                interface1_in = interface2_in == -1
        except:
            print '\nError: Please enter a number on the left side of the screen.'
                 
    # Attach the EPG to 2 interfaces using VLAN 5 as the encap
    if1 = interfaces[interface1_in]
    if2 = interfaces[interface2_in]
#     if1 = ACI.Interface('eth','1','101','1','62')
#     if2 = ACI.Interface('eth','1','101','1','63')
    vlan5_on_if1 = ACI.L2Interface('vlan5_on_if1', 'vlan', '5')
    vlan5_on_if2 = ACI.L2Interface('vlan5_on_if2', 'vlan', '5')
    vlan5_on_if1.attach(if1)
    vlan5_on_if2.attach(if2)
    epg.attach(vlan5_on_if1)
    epg.attach(vlan5_on_if2)

    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())
    
    if resp.ok:
        print '\nSuccess'

    input = raw_input('\nPress Enter to continue ')

   

def main(): 
    show_epgs()
    

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print '\n\n'
    print '<HTML><HEAD><TITLE>Python Test</TITLE></HEAD>'
    print '<BODY><H2>Hello there from a Python Script!</H2>'
    print 'Version info:', sys.version_info
    print '<p><p>'
    create_login()
    main()
    print '</BODY></HTML>'
    