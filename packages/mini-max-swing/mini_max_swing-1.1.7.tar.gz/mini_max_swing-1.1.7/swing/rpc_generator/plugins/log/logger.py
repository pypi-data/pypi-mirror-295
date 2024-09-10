import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]-[%(process)d]-[%(levelname)s]- %(message)s')

logger = logging.getLogger("rpc_generator")