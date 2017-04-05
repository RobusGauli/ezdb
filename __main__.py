import os
import sys
import functools

from argparse import ArgumentParser
from create_db import createdb


def main():
    parser = ArgumentParser(prog='EazyDeposit')
    parser.add_argument('--host', dest='host', type=str, default='localhost')
    parser.add_argument('--port', dest='port', type=str, default='5432')
    parser.add_argument('--user', dest='user', type=str, default='postgres')
    parser.add_argument('--password', dest='password', type=str, default='postgres')
    parser.add_argument('--dbname', dest='dbname', type=str, default='testdb')

    args = parser.parse_args()

    #now create a tables in the database
    createdb(args.host, args.port, args.user, args.password, args.dbname)

if __name__ == '__main__':
    main()
    