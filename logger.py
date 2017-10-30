import logging
import time

logger = logging.getLogger('cair_maze')
logger.setLevel(logging.DEBUG)


fh = logging.FileHandler('maze_%s.log' % int(time.time()))
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter2 = logging.Formatter('%(message)s')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter2)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)