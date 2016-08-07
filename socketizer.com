# redirect HTTP to HTTPS
server {
	listen 80;
	server_name socketizer.com www.socketizer.com;
	return 301 https://$server_name$request_uri;
}

# same as above for service.socketizer.com
server {
	listen 80;
	server_name service.socketizer.com;
	return 301 https://$server_name$request_uri;
}
# socketizer.com
server {
	listen 443 ssl http2;
	include snippets/ssl-socketizer.com.conf;
	include snippets/ssl-params.conf;
	server_name socketizer.com www.socketizer.com;


	location = /favicon.ico { access_log off; log_not_found off; }


    	location / {
        	include         uwsgi_params;
        	uwsgi_pass      unix:/tmp/socketizer.sock;
    	}


	# lets encrypt setup
        location ~ /\.well-known\/acme-challenge {
		allow all;
		root /srv/www;
        }

}

# service.socketizer.com
server {
	listen 443 ssl http2;
	server_name service.socketizer.com www.service.socketizer.com;
	include snippets/ssl-socketizer.com.conf;
	include snippets/ssl-params.conf;

	location = /favicon.ico { access_log off; log_not_found off; }

    	proxy_pass_header Server;

    	location / {
        	proxy_set_header Host $host;
        	proxy_set_header X-Real-IP $remote_addr;
        	proxy_set_header X-Forward-Proto $scheme;

        	proxy_http_version 1.1;
        	proxy_set_header Upgrade $http_upgrade;
        	proxy_set_header Connection "upgrade";

		# increase timeout from 60 seconds to 10 hours
		proxy_read_timeout  36000s;

        	proxy_pass http://127.0.0.1:8080;
    	}

	# lets encrypt setup
        location ~ /\.well-known\/acme-challenge {
                allow all;
		root /srv/www;
        }

}
