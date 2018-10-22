from flask import redirect, session, jsonify, request, render_template, url_for, make_response
from aciapps.models import Login_User
from aciapps.forms import NewUser, IPSearch
from aciapps import app, db
#from aciapps.aci_credentials import *
import cobra.mit.session
import cobra.mit.access
import cobra.mit.request
from netaddr import IPAddress, IPNetwork
from aciapps.aci_credentials import *
import json
import requests

aepglist = ['web', 'app', 'db']
db.create_all()

class mynetwork(object):
     netlist = []
     def __init__(self, network):
         self.network = network
     def addnet(self, value):
         self.netlist.append(value)
     def cidr(self):
         slash = self.network.rfind('/')
         cidr = self.network[slash+1:]
         return cidr


user1 = ['settlej', 'cisco']
def valid_login(user, passw):
    if user1[0] == user and user1[1] == passw:
        return True
    return False

@app.route('/applogin.json', methods=['POST', 'GET'])
def applogin():
    if request.method == 'POST':
        logindata = json.loads(request.data)
       # print(logindata)
        LOGIN = logindata['aaaUser']['attributes']['name']
        PASSWORD = logindata['aaaUser']['attributes']['pwd']
        auth = cobra.mit.session.LoginSession('https://sandboxapicdc.cisco.com', LOGIN, PASSWORD)
        apicsession = cobra.mit.access.MoDirectory(auth)
        apicsession.login()
        print(apicsession.session.cookie)
        return jsonify(apicsession.session.cookie)

porteventspath = '/api/node/class/eventRecord.json?query-target-filter=or(eq(eventRecord.cause,"port-up"),eq(eventRecord.cause,"port-down"),eq(eventRecord.cause,"port-pfc-congested"),eq(eventRecord.cause,"port-security-config-not-supported"),eq(eventRecord.cause,"update-remote-port-to-dbgrelem-failed"),eq(eventRecord.cause,"addor-del-uplink-port-group-failed"),eq(eventRecord.cause,"addor-del-vtep-port-group-failed"),eq(eventRecord.cause,"port-state-change"),eq(eventRecord.cause,"port-pfc-congested"))&order-by=eventRecord.created|desc&page=0&page-size=15'
#apicurl = 'https://198.18.133.200'
apicurl = 'https://sandboxapicdc.cisco.com'

@app.route('/portevents.json')
def portevents():
    print(request.headers)
    headers = { "content-type": "application/json",
        'Cookie' : request.headers['Cookie']}
    print(type(headers))
    print( headers)
   # headers = {'DevCookie': cookie}
  #  print(cookies)
    apicrequest = requests.get(apicurl + porteventspath, verify=False, headers=headers)
    print(type(jsonify(apicrequest.content)))
    d = json.loads(apicrequest.content)
    print(type(d))
    return jsonify(d)

@app.route('/')
def index():
  # if 'username' not in session:
  #      return render_template('login.html')
    searchs = ''
    search = request.args.get('search')
    if search in aepglist:
        searchs = search
    return render_template('home.html', searchs=searchs)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
   # getvalues = Login_User.query.all()
   # value = Login_User.query.getlist()
   # print(repr(value))
    if request.method == 'POST':
        print(request.form)
        if valid_login(request.form['username'],
                       request.form['password']):
            session['username'] = request.form['username']
            return render_template('login.html', error=error)
            ##return redirect(url_for('index'))
          #  return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    respon = make_response(render_template('login.html', error=error))
  #  respon.set_cookie('username', 'thisuser')
    return respon

@app.route('/iproute', methods=['POST','GET'])
def iproute():
    form = IPSearch()
    ip = form.ip.data
    #if ip:
    #    print(ip.encode('utf8'), '***************************************************')
    if form.validate_on_submit():
        auth = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
        apicsession = cobra.mit.access.MoDirectory(auth)
        apicsession.login()
        ip = form.ip.data
        #print(ip)
        sublist = []
        foundlist = []
        tenants_query = None
        winner = None
        searchitem = '/uni/tn-Heroes/BD-Heroes'
        tenants_query = cobra.mit.request.DnQuery(searchitem)
        tenants_query.queryTarget = 'children'
        tenants_query.classFilter = 'fvSubnet'
        subnets_query = apicsession.query(tenants_query)
        for sub in subnets_query:
                sublist.append(sub.ip)
        for ips in sublist:
            #print('this is the ip', ips)
            if IPAddress(ip) in IPNetwork(ips):
                foundnetwork = mynetwork(ips)
                foundlist.append(foundnetwork)
                #print(foundlist)
            valuemax = 0 
            for items in foundlist:
               # print(items.cidr())
               # print('value: ', valuemax, items.cidr())
                if int(items.cidr()) > valuemax:
                    winner = items
                    valuemax = int(items.cidr())
        #print(winner.network)
        sublist = None
        foundlist = None
        tenants_query = None
        return render_template('iproute.html', form=form, winner=winner)
    return render_template('iproute.html', form=form)

@app.route('/new', methods=['POST','GET'])
def new_user():
    form = NewUser()
    user = False
    password = False
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        email = form.email.data
        adduser = Login_User(user, password, email)
        #print(password)
        db.session.add(adduser)
        db.session.commit()
        another = Login_User.query.all()
        print(another)

        return render_template('newuser.html', form=form, user=user, password=password)
    #   return redirect(url_for('new_user'))
    return render_template('newuser.html', form=form, user=user, password=password)


if __name__ == '__main__':
    app.run(debug='True')