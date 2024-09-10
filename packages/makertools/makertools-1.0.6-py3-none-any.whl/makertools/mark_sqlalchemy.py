#! /usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from timeit import default_timer
from loguru import logger



metadata = MetaData()
engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_HOST, settings.MYSQL_PORT, settings.MYSQL_DBNAME))
Session = sessionmaker(bind=engine)



class UsingAlchemy(object):
    def __init__(self, commit=True, log_time=False, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._session = Session()

    def __enter__(self):
        if self._log_time is True:
            self._start = default_timer()
        return self

    def __exit__(self, *exc_info):
        if self._commit:
            self._session.commit()
        if self._log_time is True:
            diff = default_timer() - self._start
            logger.info('%s: %.6f 秒' % (self._log_label, diff))

    @property
    def session(self):
        return self._session

    def use_table(self,table_name):
        ex_table_obj = Table(table_name, metadata, autoload_with=engine)
        return ex_table_obj