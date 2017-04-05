import os
import sys
import enum
import functools
import operator
import itertools

from sqlalchemy import Column, String, Integer, Text, Enum, DateTime, Boolean
from sqlalchemy import Float, CheckConstraint, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, func, ForeignKey
from sqlalchemy import create_engine


#Instantiate the Base class

Base  = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_type = Column(String(100), nullable=False, unique=True)

    #manytomany
    tellers = relationship('TellerRole', back_populates='role')

class Teller(Base):
    __tablename__ = 'tellers'

    id = Column(Integer, primary_key=True)
    teller_id = Column(String(300), unique=True, nullable=False)
    password = Column(String, nullable=False) #SHA1 hash
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    access_token = Column(String, nullable=False, unique=True)
    expiry_date = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)
    activate = Column(Boolean, default=False)
    teller_cash_account = Column(String, nullable=False) #should be unique or not?
    remarks = Column(String, nullable=True)
    #foreign key
    branch_id = Column(Integer, ForeignKey('branches.id'))
    #relationship
    teller_branch = relationship('Branch', back_populates='branch_tellers')

    #manytomany relationship
    roles = relationship('TellerRole', back_populates='teller')

class TellerRole(Base):
    __tablename__ = 'tellerrole'

    teller_id = Column(ForeignKey('tellers.id'), primary_key=True)
    role_id = Column(ForeignKey('roles.id'), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    #relationship
    teller = relationship('Teller', back_populates='roles')
    role = relationship('Role', back_populates='tellers')


class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer, primary_key=True) #surrogate key as a primary key
    name = Column(String(300), nullable=False, unique=True)
    branch_code = Column(String(300), nullable=False, unique=True)
    address = Column(String(300))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    remarks = Column(String)
    #relationshipde
    branch_tellers = relationship('Teller', back_populates='teller_branch', cascade='all, delete, delete-orphan')
    branch_deposits = relationship('Deposit', back_populates='deposit_branch', cascade='all, delete, delete-orphan')


class Denomination(Base):
    __tablename__ = 'denominations'

    id = Column(Integer, primary_key=True)
    unit = Column(String(200), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    remarks = Column(String)

class Deposit(Base):
    __tablename__ = 'deposits'

    id = Column(Integer, primary_key=True)
    cvs_tranid = Column(String) #should be nullable or not?
    status = Column(Enum('failed', 'success', 'pending', name='status'))
    teller_id = Column(String(300)) #should be foreign key or not?
    teller_cash_account = Column(String(300))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    cvs_trantime = Column(DateTime) 
    deposit_amount = Column(String) #decimal type #check contraint
    deposit_amount_words = Column(String)
    customer_name = Column(String(500))
    deposit_acc_num = Column(String)
    branch_id = Column(Integer, ForeignKey('branches.id'))

    #relationship
    deposit_branch = relationship('Branch', back_populates='branch_deposits')


