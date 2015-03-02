		*** Setup steps for celeryd ***

1. Install Celery 2.3
2. Install django-celery
3. Copy celeryd to /etc/init.d/
        Changes:
            #if [ -n "$CELERYD_CHDIR" ]; then
            #DAEMON_OPTS="$DAEMON_OPTS --workdir=\"$CELERYD_CHDIR\""
            #fi
4. sudo vi /etc/default/celeryd
5. sudo update-rc.d celeryd defaults
6. python /home/barun/codes/www/vlabs/manage.py syncdb
7. Mount /dev/shm if required:
    http://stackoverflow.com/questions/2009278/python-multiprocessing-permission-denied#comment-6467139
8. Verify that all are running fine by doing
    ps -ef | grep rabbit
    ps -ef | grep celeryd



		*** RabbitMQ Troubleshooting ***

If you execute a simulation (in the Exercises page) and find that its 
output is not displayed, it is likely that RabbitMQ is not working on 
the server.


        ### Verify RabbitMQ is running ###

$ sudo rabbitmqctl status

Status of node rabbit@host_name ...
[{running_applications,[{rabbit,"RabbitMQ","1.7.2"},
                        {mnesia,"MNESIA  CXC 138 12","4.4.12"},
                        {os_mon,"CPO  CXC 138 46","2.2.4"},
                        {sasl,"SASL  CXC 138 11","2.1.8"},
                        {stdlib,"ERTS  CXC 138 10","1.16.4"},
                        {kernel,"ERTS  CXC 138 10","2.13.4"}]},
 {nodes,[rabbit@host_name]},
 {running_nodes,[rabbit@host_name]}]
...done.

$ ps -ef | grep rabbitmq

rabbitmq   183     1  0 10:59 ?        00:00:00 /usr/lib/erlang/erts-5.7.4/bin/epmd -daemon
rabbitmq  7978     1 13 18:38 ?        00:00:00 /usr/lib/erlang/erts-5.7.4/bin/beam.smp -W w -K true -A30 -- -root /usr/lib/erlang -progname erl -- -home /var/lib/rabbitmq -- -noshell -noinput -sname rabbit -boot /usr/lib/rabbitmq/lib/rabbitmq_server-1.7.2/sbin/../ebin/rabbit -kernel inet_default_listen_options [{nodelay,true}] -kernel inet_default_connect_options [{nodelay,true}] -sasl errlog_type error -kernel error_logger {file,"/var/log/rabbitmq/rabbit.log"} -sasl sasl_error_logger {file,"/var/log/rabbitmq/rabbit-sasl.log"} -os_mon start_cpu_sup true -os_mon start_disksup false -os_mon start_memsup false -mnesia dir "/var/lib/rabbitmq/mnesia/rabbit" -noshell -noinput
rabbitmq  8040  7978  0 18:38 ?        00:00:00 inet_gethost 4
rabbitmq  8041  8040  0 18:38 ?        00:00:00 inet_gethost 4
rabbitmq  8042  7978  0 18:38 ?        00:00:00 /usr/lib/erlang/lib/os_mon-2.2.4/priv/bin/cpu_sup



        ### Verify user and host exists

$ sudo rabbitmqctl list_users

Listing users ...
ant			<--- This is the user name specified during setup; if you have used a different name, that should be displayed here
guest
...done.


If the RabbitMQ user and vhost is not found to exisit, they should be 
re-created.



        ### If RabbitMQ is NOT running ###


[/var/lib/rabbitmq]$ sudo mv mnesia _mnesia.old
[/var/lib/rabbitmq]$ ls -l
total 724
-rw-r----- 1 rabbitmq rabbitmq 731916 Nov 29 18:40 erl_crash.dump
-rw-r--r-- 1 rabbitmq rabbitmq     26 Nov 29 11:01 pids

[/var/lib/rabbitmq]$ sudo rabbitmq-server -detached

[/var/lib/rabbitmq]$ sudo rabbitmqctl status
Status of node rabbit@host_name ...
[{running_applications,[{rabbit,"RabbitMQ","1.7.2"},
                        {mnesia,"MNESIA  CXC 138 12","4.4.12"},
                        {os_mon,"CPO  CXC 138 46","2.2.4"},
                        {sasl,"SASL  CXC 138 11","2.1.8"},
                        {stdlib,"ERTS  CXC 138 10","1.16.4"},
                        {kernel,"ERTS  CXC 138 10","2.13.4"}]},
 {nodes,[rabbit@host_name]},
 {running_nodes,[rabbit@host_name]}]
...done.

[/var/lib/rabbitmq]$ ls -l
total 728
-rw-r----- 1 rabbitmq rabbitmq 731916 Nov 29 18:40 erl_crash.dump
drwxr-xr-x 3 rabbitmq rabbitmq   4096 Nov 29 18:43 mnesia/
-rw-r--r-- 1 rabbitmq rabbitmq     26 Nov 29 11:01 pids
