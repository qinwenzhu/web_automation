#!/usr/bin/python3
# -*- coding: utf-8 -*-

import redis
import logging


class GetRedisData(object):

    def __init__(self, ip, port=6379):
        """
        连接Redis
        :param ip:
        :param port:
        """
        try:
            pool = redis.ConnectionPool(host=ip, port=port, db=0)
            self.conn = redis.StrictRedis(connection_pool=pool)
        except Exception as err:
            logging.error("connect Redis failed: %s" % err)

    def get_result_from_redis(self, key):
        keys = self.conn.keys()
        if bytes(key, encoding="utf8") in keys:
            result = self.conn.get(key)
            logging.debug("{}的redis值为：{}".format(key, result))
            return result.decode()
        else:
            logging.error('key "{}" has no result found in Redis!'.format(key))
            return False

    def set_value_to_redis(self, key, value):
        try:
            self.conn.set(key, str(value))
            # print(self.conn.get(key))
            assert (self.conn.get(key).decode("utf-8") == value), "set {} error".format(key)
        except Exception as err:
            logging.error("Redis设置{}值出错{}".format(key, err))
