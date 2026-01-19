FROM prestashop/prestashop:1.7.8

RUN rm -rf /var/www/html/*
COPY --chown=33:33 --chmod=755 ./prestashop /var/www/html
COPY --chown=33:33 --chmod=644 ./script/parameters.php /var/www/html/app/config/parameters.php
COPY apache-conf/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY apache-conf/ssl /etc/ssl/certs

EXPOSE 443