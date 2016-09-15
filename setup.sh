#!/usr/bin/env bash

file_not_cgi_bin="drawing.svg"

if [[ $USER != "root" ]]; then
    echo "You must be root. Use \"sudo ./$(basename \"$0\")\" "
else
    cp cgi-bin/* -r /usr/lib/cgi-bin/
    if [[ $file_not_cgi_bin != "" ]]; then
        cp $file_not_cgi_bin -r /var/www/html/
    fi
    chmod 766 /var/www/html/
    chmod 766 /var/www/html/*
fi
