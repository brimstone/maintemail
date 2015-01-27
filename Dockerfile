FROM ubuntu:12.04

RUN apt-get update \
 && apt-get install -y python-markdown python-vobject python-mailer
