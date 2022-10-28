docker build -t ffmpeg-python-layer-factory:latest .
rm -rf $(pwd)/source
mkdir $(pwd)/source
docker run --rm -it -v $(pwd)/source:/source ffmpeg-python-layer-factory cp /var/task/python.zip /source
