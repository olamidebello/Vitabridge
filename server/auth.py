"""VitaBridge account service. Clinical/dispatch data is not handled here."""
import hashlib,hmac,json,os,re,secrets,sqlite3,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from http.cookies import SimpleCookie
DB=os.environ.get('VITABRIDGE_DB','/var/lib/vitabridge/accounts.sqlite3')
ORIGIN=os.environ.get('VITABRIDGE_ORIGIN','https://vitabridge.olamidemedical.health')
def connect():
 c=sqlite3.connect(DB,timeout=10);c.row_factory=sqlite3.Row;return c
def initialize():
 os.makedirs(os.path.dirname(os.path.abspath(DB)),exist_ok=True)
 with connect() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,email TEXT UNIQUE,name TEXT,salt TEXT,password TEXT,created INTEGER);CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT,expires INTEGER);CREATE TABLE IF NOT EXISTS attempts(ip TEXT,at INTEGER);''')
 os.chmod(DB,0o600)
def digest(password,salt):return hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt),n=16384,r=8,p=1).hex()
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def reply(self,status,data,cookie=None):
  raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(raw)))
  if cookie:self.send_header('Set-Cookie',cookie)
  self.end_headers();self.wfile.write(raw)
 def current(self,c):
  try:
   cookies=SimpleCookie(self.headers.get('Cookie',''));token=cookies['vb_session'].value
  except (KeyError,ValueError):return None
  return c.execute('SELECT u.id,u.email,u.name FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.token=? AND s.expires>?',(hashlib.sha256(token.encode()).hexdigest(),int(time.time()))).fetchone()
 def do_GET(self):
  if self.path=='/api/health':return self.reply(200,{'ok':True,'service':'vitabridge-accounts'})
  if self.path!='/api/auth/me':return self.reply(404,{'error':'Not found'})
  with connect() as c:u=self.current(c)
  self.reply(200 if u else 401,{'user':dict(u)} if u else {'error':'Sign in required'})
 def do_POST(self):
  if self.headers.get('Origin')!=ORIGIN:return self.reply(403,{'error':'Invalid origin'})
  if self.path not in ['/api/auth/signup','/api/auth/login','/api/auth/logout']:return self.reply(404,{'error':'Not found'})
  try:
   size=int(self.headers.get('Content-Length','0'))
   if size<1 or size>8192:raise ValueError()
   data=json.loads(self.rfile.read(size))
   if not isinstance(data,dict):raise ValueError()
  except (ValueError,json.JSONDecodeError):return self.reply(400,{'error':'Invalid request'})
  now=int(time.time())
  with connect() as c:
   if self.path.endswith('/logout'):
    cookie=SimpleCookie(self.headers.get('Cookie',''));token=cookie['vb_session'].value if 'vb_session' in cookie else ''
    c.execute('DELETE FROM sessions WHERE token=?',(hashlib.sha256(token.encode()).hexdigest(),));return self.reply(200,{'ok':True},'vb_session=; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=0')
   ip=self.client_address[0] # loopback proxy intentionally imposes a conservative aggregate limit
   c.execute('DELETE FROM attempts WHERE at<?',(now-900,));c.execute('DELETE FROM sessions WHERE expires<?',(now,))
   if c.execute('SELECT count(*) FROM attempts WHERE ip=?',(ip,)).fetchone()[0]>=30:return self.reply(429,{'error':'Too many attempts. Try again in 15 minutes.'})
   c.execute('INSERT INTO attempts VALUES(?,?)',(ip,now))
   email=str(data.get('email','')).strip().lower();password=str(data.get('password',''));name=str(data.get('name','')).strip()
   if not re.fullmatch(r'[^\s@]{1,100}@[^\s@]{1,150}\.[^\s@]{2,30}',email) or not 12<=len(password)<=256:return self.reply(400,{'error':'Enter a valid email and a password of 12–256 characters.'})
   if self.path.endswith('/signup'):
    if not 1<=len(name)<=100 or data.get('accept_terms') is not True:return self.reply(400,{'error':'Name and acceptance of terms are required.'})
    salt=secrets.token_hex(16);uid=secrets.token_hex(16)
    try:c.execute('INSERT INTO users VALUES(?,?,?,?,?,?)',(uid,email,name,salt,digest(password,salt),now))
    except sqlite3.IntegrityError:return self.reply(409,{'error':'Unable to create account. Try signing in instead.'})
    u={'id':uid,'email':email,'name':name}
   else:
    row=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone();salt=row['salt'] if row else '00'*16
    valid=hmac.compare_digest(digest(password,salt),row['password'] if row else '0'*128)
    if not row or not valid:return self.reply(401,{'error':'Email or password incorrect.'})
    u={k:row[k] for k in ['id','email','name']}
   token=secrets.token_urlsafe(32);c.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),u['id'],now+28800))
  self.reply(200,{'user':u,'email_verified':False},f'vb_session={token}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=28800')
if __name__=='__main__':
 initialize();ThreadingHTTPServer(('127.0.0.1',18872),Handler).serve_forever()
