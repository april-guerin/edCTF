#!/bin/bash

# set edCTF root
export EDCTF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# set subdirectories
export EDCTF_EMBER="${EDCTF_DIR}/ember"
export EDCTF_DJANGO="${EDCTF_DIR}/edctf"
export EDCTF_SCRIPTS="${EDCTF_DIR}/scripts"
export EDCTF_CONFIG="${EDCTF_DIR}/config"

# set static directories
export EDCTF_STATIC="${EDCTF_DJANGO}/static"
export EDCTF_EMBER_STATIC="${EDCTF_STATIC}/ember"
export EDCTF_ADMIN_STATIC="${EDCTF_STATIC}/admin"
export EDCTF_REST_STATIC="${EDCTF_STATIC}/rest_framework"

# set dependancy paths
export APACHE_CONFIG="/etc/apache2/sites-enabled"
export DJANGO_ADMIN_STATIC="/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin"
export REST_FRAMEWORK_CSS_DIR="/usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework"

# set database information
export EDCTF_DATABASE="edctf"
