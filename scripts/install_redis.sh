source ../scripts/common.sh

log '*** Executing install_redis.sh'

REDIS_PASSWD_FILE=$HOME_PATH/redis_passwd
REDIS_CONF_FILE=/etc/redis/redis.conf
TMP_FILE=$REDIS_CONF_FILE.tmp

log "Reading password for Redis from $REDIS_PASSWD_FILE"

if [[ -f "$REDIS_PASSWD_FILE" && -r "$REDIS_PASSWD_FILE" ]]
then
    REDIS_PASSWD=$(cat "$REDIS_PASSWD_FILE")
else
    REDIS_PASSWD=$(generate_password)
    echo "$REDIS_PASSWD" > "$REDIS_PASSWD_FILE"
    chmod -w "$REDIS_PASSWD_FILE"
fi

# Add (replace) password to the Redis configuration file
grep -v '^[[:space:]]*requirepass' "$REDIS_CONF_FILE" > "$TMP_FILE"
cat "$TMP_FILE" > "$REDIS_CONF_FILE"
echo "requirepass $REDIS_PASSWD" >> "$REDIS_CONF_FILE"
rm "$TMP_FILE"
/etc/init.d/redis-server restart

echo '[program:django_rq_worker_ant]
command=python /home/barun/codes/www/vlabs/manage.py rqworker q_ant
autostart=true
autorestart=true
stderr_logfile=/var/log/django_rq_worker_ant.err.log
stdout_logfile=/var/log/django_rq_worker_ant.out.log' > /etc/supervisor/conf.d/django_rq_worker_ant.conf

# Making it fail-safe
/etc/init.d/supervisor stop
/etc/init.d/supervisor start
# supervisor should be up by now; if not, the following would not have any effect
supervisorctl reread
supervisorctl update
supervisorctl restart django_rq_worker_ant

# Need to place somewhere else
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales
