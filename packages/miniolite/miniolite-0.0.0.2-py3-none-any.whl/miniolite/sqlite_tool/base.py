#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2024/09/08 21:21:51
#########################################################################

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from functools import wraps
from contextlib import contextmanager

import json
import os

SqlalchemyBase = declarative_base()

class SqliteBase:
    def __init__(self, db_path= "tmp/info.db"):
        SQLALCHEMY_DB_URI = f"sqlite:///{db_path}"
        self.engine = sqlalchemy.create_engine(SQLALCHEMY_DB_URI)
        self.SessionClass = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    def close(self):
        self.engine.dispose()
        
    def init_tables(self):
        # create all tables
        SqlalchemyBase.metadata.create_all(self.engine)
    def reset_tables(self):
        SqlalchemyBase.metadata.drop_all(bind=self.engine)
        self.init_table()

    @contextmanager
    def session_scope(self):
        """上下文管理器自动获取session"""
        session = self.SessionClass()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def with_session(cls,func):
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            with self.session_scope() as session:
                try:
                    result = func(self,session, *args, **kwargs)
                    session.commit()
                    return result
                except:
                    session.rollback()
                    raise
        return wrapper
    
    # @with_session()
    # @with_session
    # def get_all(self, session, cls):
    #     return session.query(cls).all()