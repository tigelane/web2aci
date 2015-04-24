import acitoolkit.acitoolkit as aci
import sys

session = ''

def check_connection():
    description = ('Simple tools to access information in an ACI network via a web interfaces.')
    creds = aci.Credentials('apic', description)
    args = creds.get()
    if login():
        connected = 'You are connected to an APIC at:   %s     as user:   %s<p>' %(args.url, args.login)
    else:
        connected = 'Your current APIC information does not work for server: %s as user: %s<p>'   
    
    return connected 

def login():
    global session
    description = ('Simple tools to access inofrmation in an ACI network via a web interfaces.')
    creds = aci.Credentials('apic', description)
    args = creds.get()

    # Login to APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        return 0
    else:
        return 1
    
def footer():
    html = '''
    <button onclick="goBack()">Go Back</button>
    <script>function goBack() { window.history.back(); } </script>
    </pre>
    </body>
    </html>
    '''
    return html

def setuplogin():
    connected = check_connection()
    
    html = '''
    <html><head>
    <title>Login to APIC</title>
    </head>
    <body>
    <center>
    %s
    <h2>Please enter the following:</h2>
    <FORM value="form" action="setuplogin_info" method="post">
    <P>
	    <LABEL for="host">IP Address or Hostname</LABEL>
	    <INPUT type="text" name="host"><BR>
	    <LABEL for="user">User ID</LABEL>
	    <INPUT type="text" name="user"><BR>
	    <LABEL for="pass">Password</LABEL>
	    <INPUT type="password" name="password"><BR>
	    <INPUT type="radio" name="proto" value=0>HTTP - 80<BR>
	    <INPUT type="radio" name="proto" value=1>HTTPS - 443<BR>
        <BR>
	    <INPUT type="submit" value="Send"> <INPUT type="reset">
    </FORM>
    ''' %(connected)
    
    return html + footer()

def setuplogin_info(req):
    info = req.form
    
    try:
        ipaddr = info['host']
        user = info['user']
        password = info['password']        
        proto = info['proto']
        
    except:
        html = '''
        <html><head>
        <title>Searching APIC</title>
        </head>
        <body>
        <h2>There was a problem with the information.  Please try again.</h2>
        <hr>
        '''
        return html + footer()
    
    #Create the new credentials.py file
    credsfilename = '/usr/local/lib/python2.7/dist-packages/credentials.py'
    try:
        credsfile = open(credsfilename, "w")
    except:
        html = '''
        <html><head>
        <title>Searching APIC</title>
        </head>
        <body>
        <h2>There was a problem opening %s  Please try again.</h2>
        <hr>
        ''' % (credsfilename)
        return html + footer()
    
    credsfile.write("LOGIN = '%s'\n"% (user))
    credsfile.write("PASSWORD = '%s'\n"% (password))
    credsfile.write("IPADDR = '%s'\n" % (ipaddr))
    if proto:
        credsfile.write("URL = 'https://%s'\n"% (ipaddr))
    else:
        credsfile.write("URL = 'http://%s'\n"% (ipaddr))
    credsfile.close()
    
    if login():
        response = "Your login information has been accepted and a test login was completed."
    else:
        response = "ERROR: A test login failed."
    
    # HTML Text return
    html = '''
    <html><head>
    <title>Login information</title>
    </head>
    <body>
    <h2>%s</h2>
    <hr>
    ''' %(response)
    return html + footer()


def search4host():
    connected = check_connection()
    
    html = '''
    <html><head>
    <title>Search for a host</title>
    </head>
    <body>
    <center>
    %s
    <h2>Search for a host</h2><pre>
    <h3>You can enter anything from the following example as a search:</h3>
    MACADDRESS          IPADDRESS         INTERFACE       ENCAP      TENANT     APP PROFILE        EPG
    -----------------   ---------------   --------------  ---------- ------     -----------        ---
    00:50:56:15:7C:44   172.6.101.12     eth 1/101/1/4   vlan-2120  common     Simple_Two-Tier    WWW
    <pre>
    <FORM value="form" action="search4host_info" method="post">
    <P>
	    <LABEL for="search">Search for: </LABEL>
	    <INPUT type="search" name="search"><BR>
	    <INPUT type="radio" name="case" value=1>Case Sensitive<BR>
        <BR>
	    <INPUT type="submit" value="Send"> <INPUT type="reset">
    </FORM>
    ''' % (connected)
    
    return html + footer()

def search4host_info(req):
    casesens = 0
    login()
    info = req.form
    search = info['search']
	
    try:
        case = info['case']
        casesens = 1
    except:
        pass
        
    # Header for this page
    html = '''
    <html><head>
    <title>Searching APIC</title>
    </head>
    <body>
    <h2>Your search resulted in the following:</h2>
    <hr>
    <pre>
    '''
    

    data = []
    endpoints = aci.Endpoint.get(session)
    for ep in endpoints:
        epg = ep.get_parent()
        app_profile = epg.get_parent()
        tenant = app_profile.get_parent()
        data.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                     tenant.name, app_profile.name, epg.name))

    # Display the data downloaded
    col_widths = [19, 17, 15, 10, 15, 25, 15]
    template = ""
    for idx, width in enumerate(col_widths):
        template += '{%s:%s} ' % (idx, width)
    html += (template.format("MACADDRESS", "IPADDRESS", "INTERFACE",
                          "ENCAP", "TENANT", "APP PROFILE", "EPG")) + '<br>'
    fmt_string = []
    for i in range(0, len(col_widths)):
        fmt_string.append('-' * (col_widths[i] - 2))
    html += (template.format(*fmt_string)) + '<br>'
    for rec in data:
	if casesens:
            if any(search in s for s in rec):
                html += (template.format(*rec)) + '<br>'
        else:
            if any(search.lower() in s.lower() for s in rec):
                html += (template.format(*rec)) + '<br>'

    html += '</pre>'
    html += '<p><p>'
    html += footer()
    return html
