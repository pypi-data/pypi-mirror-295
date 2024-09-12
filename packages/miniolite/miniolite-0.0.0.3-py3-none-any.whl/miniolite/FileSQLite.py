#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2024/09/08 21:21:51
#########################################################################
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from miniolite.sqlite_tool.base import SqliteBase,SqlalchemyBase


# 文件夹表
class Folder(SqlalchemyBase):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('folders.id'))
    parent = relationship('Folder', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Folder(name={self.name}, parent_id={self.parent_id})>"

# 文件表
class File(SqlalchemyBase):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    folder = relationship('Folder', backref='files')
    content = Column(String, nullable=True)

    def __repr__(self):
        return f"<File(name={self.name}, folder_id={self.folder_id})>"



class FileSQLite(SqliteBase):
    def __init__(self, db_path= "tmp/info.db"):
        super().__init__(db_path)
        self.init_tables()
        self.root_name = "Root"
        self.add_root_folder()
    
    def add_root_hearder_to_path(self,path):
        path= path.strip('/')
        path = self.root_name+'/'+path
        return path
    def split_path_step(self,path):
        dir_list  = path.strip('/').split('/')
        dir_list = list(filter(None, dir_list))
        return dir_list
    

    @SqliteBase.with_session
    def add_root_folder(self,session):
        root_folder = session.query(Folder).filter_by(name=self.root_name).first()
        if root_folder is None:
            folder = Folder(name=self.root_name, parent_id=None)
            session.add(folder)
            session.commit()
        else:
            return root_folder

    @SqliteBase.with_session
    def force_add_folder(self,session,path):
        dir_list = self.split_path_step(path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                folder = Folder(name=dir_name, parent_id=parent_id)
                session.add(folder)
                session.commit()
                parent_id = folder.id
            else:
                parent_id = folder_now.id

    @SqliteBase.with_session
    def delete_folder(self,session,path):
        path = self.add_root_hearder_to_path(path)
        dir_list = self.split_path_step(path)
        assert len(dir_list) >=2, "try to delete root folder, not allowed!"
        delete_dir_name = dir_list[-1]
        parent_id = session.query(Folder).filter_by(name=dir_list[-2]).first().id
        delete_folder = session.query(Folder).filter_by(name=delete_dir_name,parent_id=parent_id).first()
        session.delete(delete_folder)

    @SqliteBase.with_session
    def list_folder(self,session,path):
        dir_list = self.split_path_step(path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError(f"No directory found at {dir_name}")
            else:
                parent_id = folder_now.id
        list_folders = session.query(Folder).filter_by(parent_id=parent_id).all()
        list_folders_name = [folder.name for folder in list_folders]
        return list_folders_name
    @SqliteBase.with_session
    def add_file(self,session,file_path,content):
        parent_path, file_name = os.path.split(file_path)
        dir_list = self.split_path_step(parent_path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError((f"No directory found at {dir_name}"))
            else:
                parent_id = folder_now.id
        file = session.query(File).filter_by(name=file_name, folder_id=parent_id).first()
        if file is not None:
            raise FileExistsError((f"File {file_name} already exists in {parent_path}"))
        else:
            file = File(name=file_name, folder_id=parent_id,content=content)
            session.add(file)
            session.commit()
            return True
    @SqliteBase.with_session
    def update_file(self,session,file_path,content):
        parent_path, file_name = os.path.split(file_path)
        dir_list = self.split_path_step(parent_path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError((f"No directory found at {dir_name}"))
            else:
                parent_id = folder_now.id
        file = session.query(File).filter_by(name=file_name, folder_id=parent_id).first()
        if file is not None:
            file.content = content
            session.commit()
            return True
        else:
            file = File(name=file_name, folder_id=parent_id,content=content)
            session.add(file)
            session.commit()
            return True
    @SqliteBase.with_session
    def read_file(self,session,file_path):
        parent_path, file_name = os.path.split(file_path)
        dir_list = self.split_path_step(parent_path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError((f"No directory found at {dir_name}"))
            else:
                parent_id = folder_now.id
        file = session.query(File).filter_by(name=file_name, folder_id=parent_id).first()
        if file is not None:
            content = file.content
            session.commit()
            return content
        else:
            raise FileNotFoundError((f"No file found at {file_name}"))
        
    @SqliteBase.with_session
    def list_files(self,session,folder_path):
        dir_list = self.split_path_step(folder_path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError((f"No directory found at {dir_name}"))
            else:
                parent_id = folder_now.id
        list_files = session.query(File).filter_by(folder_id=parent_id).all()
        list_files_name = [file.name for file in list_files]
        return list_files_name
    
    @SqliteBase.with_session
    def delete_file(self,session,file_path):
        parent_path, file_name = os.path.split(file_path)
        dir_list = self.split_path_step(parent_path)
        parent_id = session.query(Folder).filter_by(name=self.root_name).first().id
        for dir_name in dir_list:
            folder_now = session.query(Folder).filter_by(name=dir_name,parent_id=parent_id).first()
            if folder_now is None:
                raise FileNotFoundError((f"No directory found at {dir_name}"))
            else:
                parent_id = folder_now.id
        file = session.query(File).filter_by(name=file_name, folder_id=parent_id).first()
        if file is None:
            raise FileNotFoundError((f"File {file_name} not exists in {parent_path}"))
        else:
            session.delete(file)
            session.commit()
            return True