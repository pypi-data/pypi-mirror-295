Ganeti host memory allocation monitoring tool

Requirements:
 - Read only access to ganeti rapi (https://docs.ganeti.org/docs/ganeti/3.0/html/rapi.html#users-and-passwords)


gnt-monitoring:
  -h, --help                        show this help message and exit
  --log-level                       Log level, default: warning
  --warning WARNING                 Warning value, default: 75.000000
  --critical CRITICAL               Critical value, default: 90.000000
  --sentry-dsn SENTRY_DSN           Sentry dsn for remote error logging
  --sentry-env SENTRY_ENV           Envronment name for sentry, defaul: dev
  --rapi-host RAPI_HOST             Gasneti remote api host name, defaul: localhost
  --rapi-port RAPI_PORT             Remote api port, default: 5080
  --rapi-scheme RAPI_SCHEME         Scheme to use, default: https
  --rapi-user RAPI_USER             Username if authentication enabled
  --rapi-password RAPI_PASSWORD     Password for user (UNSECURE, PLEASE USE netrc)
  --netrc-file NETRC_FILE           netrc file for authentication, default: /Users/arunas/.netrc
