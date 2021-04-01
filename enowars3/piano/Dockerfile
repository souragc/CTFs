FROM php:7.3.5-apache

COPY src/ /var/www/html/
RUN mkdir /var/www/data/

RUN chown -R www-data:www-data /var/www/data && a2enmod rewrite