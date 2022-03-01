from website import db
from website.models import *

import psycopg2

#returns connection
def connect_psycopg2(link):
    return psycopg2.connect(link)