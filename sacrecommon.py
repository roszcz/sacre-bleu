import facebook

def get_secrets(filenames):
	with open(filenames[0], 'r') as myfile:
		token = myfile.read().replace('\n','')

	with open(filenames[1], 'r') as idfile:
	    page_id = idfile.read().replace('\n','')

	return token, page_id

def get_api():
    cfg = make_cfg()
    graph = facebook.GraphAPI(cfg['access_token'])
    #  Get page token to post as the page. You can skip
    #  the following if you want to post as yourself.
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
	if page['id'] == cfg['page_id']:
	    page_access_token = page['access_token']
	    graph = facebook.GraphAPI(page_access_token)
    return graph
    # You can also skip the above if you get a page token:
    # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
    # and make that long-lived token as in Step 3

def make_cfg():
    token, pageid = get_secrets(['token.secret', 'pageid.secret'])
    cfg = {
	    'page_id' : '119890141687062',
	    'access_token' : token
	    }
    
    return cfg
