#!/bin/bash
. ${SCRIPTS}/environment.bash
set -x

if [ ! -z "$UUID" ] && [ ! -z "$USER" ]; then
  adduser --shell /bin/bash --uid $UUID --disabled-password --gecos "" $USER
  echo >> /etc/sudoers
  echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
  echo >> /etc/sudoers

  # Build frontend
  su $USER -c "cd ${EDCTF_EMBER} \
    && npm install \
    && bower install -q \
    && sudo cp -R ${DJANGO_ADMIN_STATIC} ${EDCTF_ADMIN_STATIC} \
    && sudo cp -R ${REST_FRAMEWORK_CSS_DIR} ${EDCTF_REST_STATIC}"

  # Start postgres
  /etc/init.d/postgresql start

  # Build backend
  su $USER -c "${SCRIPTS}/build_backend.bash"
  su $USER -c "${SCRIPTS}/reset_db.bash"

  # Start apache
  /usr/sbin/apache2ctl -k restart

  # Entrypoint
  su $USER
else
  # Build frontend
  ${SCRIPTS}/build_frontend-dev.bash

  # Start services
  /etc/init.d/postgresql start && /usr/sbin/apache2ctl -k restart

  # Build backend
  ${SCRIPTS}/build_backend.bash

  # Entrypoint
  /bin/bash
fi
