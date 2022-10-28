FROM lambci/lambda:build-python3.8

WORKDIR /var/task/python

# download ffmpeg
# RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz --output ffmpeg-release.tar.xz
RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz --output ffmpeg-release.tar.xz
RUN tar -xf ffmpeg-release.tar.xz
RUN mv ffmpeg-*/ffmpeg ffmpeg
RUN mv ffmpeg-*/ffprobe ffprobe
RUN rm -rf ffmpeg-*-static
RUN rm -rf ffmpeg-release.tar.xz

# install pillow
RUN python3.8 -m pip install pillow==7.0.0 -t ./

WORKDIR /var/task

# zip
RUN zip -r9 /var/task/python.zip /var/task/python

# clean
RUN rm -rf /var/task/python

CMD ls
