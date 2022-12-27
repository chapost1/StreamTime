import garbage_collector
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(asctime)s >> %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p %Z'
)


if __name__ == '__main__':
    garbage_collector.collect_garbage_every_x_minutes(minutes=1)
