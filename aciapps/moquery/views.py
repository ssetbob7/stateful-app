from aciapps import app
from aciapps.aci_credentials import *
from aciapps.moquery.forms import QueryACI, CreateTenantTree
from flask import render_template, Blueprint, request, redirect, url_for
import cobra.mit.session
import cobra.mit.access
import cobra.mit.request

moquery_blueprints = Blueprint('moquery', __name__, template_folder='templates')
create_blueprints = Blueprint('create', __name__, template_folder='templates')

@moquery_blueprints.route('/moquery', methods=['POST','GET'])
def mo_query():
    form = QueryACI()
    searchitem = request.args.get('mosearch')
    if form.validate_on_submit() or searchitem:
        if form.validate_on_submit():
            searchitem = form.search.data
        try:
            auth = cobra.mit.session.LoginSession(URL, LOGIN, PASSWORD)
            session = cobra.mit.access.MoDirectory(auth)
            session.login()
            tenant_query = cobra.mit.request.ClassQuery(searchitem)
            #tenant_query.subtree = 'full'
          ##  tenant_query.subtreeInclude = 'faults'
            tenant_query.subtreeInclude = 'health'
            print(tenant_query.options)
            tenant = session.query(tenant_query)
            print(dir(tenant_query))
            #tenant = tenant.sort()
            return render_template('mo_query.html', tenant=tenant, searchitem=searchitem, form=form)
        except Exception as error:
      #      print(str(error))
            return render_template('mo_query.html', error=error, form=form)
    else:
        return render_template('mo_query.html', form=form)



@create_blueprints.route('/create', methods=['POST','GET'])
def create():
    form = CreateTenantTree()
    if form.validate_on_submit():
        tenantlist = False
        applist = False
        epglist = False
        bdlist = False
        error = False
        tenantitem = form.tenant.data
        appitem = form.app.data
        if ',' in appitem:
            applist = appitem.split(',')
        #    appitem = applist
        epgitem = form.epg.data
        if ',' in epgitem:
            epglist = epgitem.split(',')
        #    epgitem = epglist
        bditem = form.bd.data
        if ',' in bditem:
            bdlist = bditem.split(',')
        #    bditem = bdlist           
        return render_template('create.html', applist=applist, epglist=epglist, \
                                bdlist=bdlist, tenantlist=tenantlist, appitem=appitem,
                                epgitem=epgitem, bditem=bditem, error=error, form=form)
    else:
        return render_template('create.html', form=form)