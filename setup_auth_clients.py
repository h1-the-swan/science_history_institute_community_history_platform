# these commands are meant to be run in the hypothesis shell
# @postgres psql -U postgres -c "INSERT INTO public.authclient ($(date +'%F %T'), $(date +'%F %T'), ${HYPOTHESIS_CLIENT_ID}, 'lsf_client', ${HYPOTHESIS_CLIENT_SECRET}, ${HYPOTHESIS_AUTHORITY}, 'client_credentials', '', '${HYPOTHESIS_SERVICE}/app.html', 't')"
# @postgres psql -U postgres -c "INSERT INTO public.authclient ($(date +'%F %T'), $(date +'%F %T'), ${HYPOTHESIS_JWT_CLIENT_ID}, 'lsf_jwt_client', ${HYPOTHESIS_JWT_CLIENT_SECRET}, ${HYPOTHESIS_AUTHORITY}, 'jwt_bearer', '', '', 't')"
from __future__ import unicode_literals
import os, uuid
print("clientid fromenv: {}".format(os.environ.get('HYPOTHESIS_CLIENT_ID')))
# create authclient
authclient = models.AuthClient(id=os.environ.get('HYPOTHESIS_CLIENT_ID'),
                                name='lsf_client',
                                secret=os.environ.get('HYPOTHESIS_CLIENT_SECRET'),
                                authority=os.environ.get('HYPOTHESIS_AUTHORITY'),
                                grant_type='client_credentials',
                                redirect_uri="{}/app.html".format(os.environ.get('HYPOTHESIS_SERVICE')),
                                trusted=True)
request.db.add(authclient)
request.db.flush()

# create jwt client
authclient_jwt = models.AuthClient(id=os.environ.get('HYPOTHESIS_JWT_CLIENT_ID'),
                                name='lsf_jwt_client',
                                secret=os.environ.get('HYPOTHESIS_JWT_CLIENT_SECRET'),
                                authority=os.environ.get('HYPOTHESIS_AUTHORITY'),
                                grant_type='jwt_bearer',
                                trusted=True)
request.db.add(authclient_jwt)
request.db.flush()
request.tm.commit()

# Create organization
org = models.Organization(authority="sciencehistory.org", name="ScienceHistory", logo=None)
request.db.add(org)
request.db.flush()
request.tm.commit()

# Create annotation group
service = request.find_service(name='group')
org = session.query(models.Organization).filter_by(authority="sciencehistory.org").first()
group = service.create_open_group(name="ScienceHistory", userid="acct:admin@sciencehistory.org",
          origins=[os.environ.get('APP_URL')], description=None,
          organization=org)
request.db.add(group)
request.db.flush()
request.tm.commit()
