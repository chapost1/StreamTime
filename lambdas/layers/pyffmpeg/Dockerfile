FROM lambci/lambda:build-python3.8

WORKDIR /var/task/python

# download ffmpeg
RUN curl https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-4.1.4-amd64-static.tar.xz --output ffmpeg-release.tar.xz
RUN tar -xf ffmpeg-release.tar.xz
RUN mv ffmpeg-*/ffmpeg ffmpeg
RUN mv ffmpeg-*/ffprobe ffprobe
RUN rm -rf ffmpeg-*-static
RUN rm -rf ffmpeg-release.tar.xz

WORKDIR /var/task

# zip
RUN zip -r9 /var/task/python.zip /var/task/python

# clean
RUN rm -rf /var/task/python

CMD ls
