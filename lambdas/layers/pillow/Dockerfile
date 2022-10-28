FROM lambci/lambda:build-python3.8

WORKDIR /var/task/python

# install pillow
RUN python3.8 -m pip install pillow==9.2.0 -t ./

WORKDIR /var/task

# zip
RUN zip -r9 /var/task/python.zip /var/task/python

# clean
RUN rm -rf /var/task/python

CMD ls
