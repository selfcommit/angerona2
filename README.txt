Angerona2 is a rewrite of Angerona

THIS IS NOT READY TO USE YET

TODO
----
retrieve views
api routes
thottle implementation

document how to setup nginx to safely log

map $request $loggable {
  ~retr/.*  0;
  default 1;
}

server {
...
  access_log     /var/log/nginx/angerona.pw-access.log combined if=$loggable;
...
}