FROM r.bingo.soft.798.cn/library/centos-74-el7:latest
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && yum install -y bingo-nginx bingo-nginx-lvscheck \
    && yum groupinstall -y "Development tools" \
    && yum install -y python-devel zlib-devel bzip2-devel pcre-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel mysql-devel openldap-devel \
    && yum clean all \
    && pip install uwsgi==2.0.11.1 django==1.8.3 djangorestframework==2.4.6 django-axes==1.3.9 drf-compound-fields==0.2.2 MySQL-python ldap python-ldap simplejson querystring_parser xlwt poster idna certifi distribute urllib3