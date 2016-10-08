# socketizer

Socketizer is the front end site, for the socketizer service; a WebSockets based service used by the [Socketizer-WordPress](https://github.com/stef-k/socketizer-wordpress) plugin

The whole project is based uppon 3 sub-projects:

 * Socketizer (this repository) which is the front-end, that showcases the service, registers new users, made with Python and Django
 * [Socketizer-Service](https://github.com/stef-k/socketizer-service) which is the WebSockets server, responsible for pushing live updates to WordPress sites, made with Go
 * [Socketizer-WordPress](https://github.com/stef-k/socketizer-wordpress) which is the WordPress plugin, responsible to call the websocket server API, made with PHP
