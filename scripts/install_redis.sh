source ../scripts/common.sh

log '*** Executing install_redis.sh'

REDIS_PASSWD_FILE=$HOME_PATH/redis_passwd

log 'Reading password for Redis'

if [[ -f "$REDIS_PASSWD_FILE" && -r "REDIS_PASSWD_FILE" ]]
then
    REDIS_PASSWD=$(cat "$REDIS_PASSWD_FILE")
else
    REDIS_PASSWD=$(generate_password)
    echo "$REDIS_PASSWD" > "$REDIS_PASSWD_FILE"
    chmod -w "$REDIS_PASSWD_FILE"
fi


echo '[program:django_rq_worker_ant]
command=python /home/barun/codes/www/vlabs/manage.py rqworker q_ant
autostart=true
autorestart=true
user=www-data
stderr_logfile=/var/log/django_rq_worker_ant.err.log
stdout_logfile=/var/log/django_rq_worker_ant.out.log' > /etc/supervisor/conf.d/django_rq_worker_ant.conf

supervisorctl reread
supervisorctl update

# Need to place somewhere else
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales