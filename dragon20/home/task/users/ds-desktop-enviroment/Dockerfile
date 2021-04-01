FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y
RUN apt upgrade -y

# prepare GUI
RUN apt install -y xorg gnome-core
RUN apt install -y gnome-session-flashback xvfb x11vnc

# install tools
RUN apt install -y sudo nano xdotool wget curl xvfb x11vnc gconf2 gconf-service libappindicator1 locales netcat

# fix locales
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

# prepare users
RUN useradd -m -d /home/admin -s /bin/bash admin
RUN useradd -m -d /home/guest -s /bin/bash guest
RUN mkdir -p /home/admin/data
RUN mkdir -p /home/admin/Desktop
RUN chown admin:admin /home/admin/data
RUN chown admin:admin /home/admin/Desktop
RUN chmod 700 /home/admin/data
RUN chmod 700 /home/admin/Desktop
RUN echo "admin ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# copy main scripts
COPY start.sh /start.sh
COPY admin.sh /admin.sh
COPY admin-ui.sh /admin-ui.sh
RUN chmod 755 /start.sh /admin.sh /admin-ui.sh

# run
CMD /bin/bash /start.sh
