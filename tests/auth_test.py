import importlib.util,tempfile,threading,http.client,json,os,unittest
spec=importlib.util.spec_from_file_location('auth','server/auth.py');auth=importlib.util.module_from_spec(spec);spec.loader.exec_module(auth)
class TestAccounts(unittest.TestCase):
 def test_flow(self):
  with tempfile.TemporaryDirectory() as d:
   auth.DB=os.path.join(d,'accounts.db');auth.initialize();s=auth.ThreadingHTTPServer(('127.0.0.1',0),auth.Handler);threading.Thread(target=s.serve_forever,daemon=True).start()
   def request(path,data=None,cookie=None,origin=auth.ORIGIN):
    c=http.client.HTTPConnection('127.0.0.1',s.server_port);headers={'Origin':origin,'Content-Type':'application/json'}
    if cookie:headers['Cookie']=cookie
    c.request('POST' if data is not None else 'GET',path,json.dumps(data) if data is not None else None,headers);r=c.getresponse();result=(r.status,json.loads(r.read()),r.getheader('Set-Cookie'));c.close();return result
   try:
    data={'email':'test@example.com','password':'strong-test-password','name':'Demo','accept_terms':True}
    self.assertEqual(request('/api/auth/signup',data,origin='https://other.example')[0],403)
    status,body,cookie=request('/api/auth/signup',data);self.assertEqual(status,200);self.assertEqual(body['user']['name'],'Demo');self.assertIn('HttpOnly',cookie);self.assertIn('Secure',cookie)
    self.assertEqual(request('/api/auth/me',cookie=cookie)[0],200)
    self.assertEqual(request('/api/auth/login',{**data,'password':'wrong-password'})[0],401)
    self.assertEqual(request('/api/auth/login',data)[0],200)
    self.assertEqual(request('/api/auth/signup',data)[0],409)
    self.assertEqual(request('/api/auth/logout',{},cookie)[0],200)
    self.assertEqual(request('/api/auth/me',cookie=cookie)[0],401)
    with auth.connect() as c:self.assertNotEqual(c.execute('select password from users').fetchone()[0],data['password'])
   finally:s.shutdown();s.server_close()
if __name__=='__main__':unittest.main()
