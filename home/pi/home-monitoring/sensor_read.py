import datetime
import pytz
import time
import psycopg2 as DBMS
import csv
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

# first read and pause for 2 min to allow sensor warmup
for i in range(0,12):
    try:
        temperature = bme280.get_temperature()
        pressure = (bme280.get_pressure() * 0.1) * 7.50062
        humidity = bme280.get_humidity()
    except:
        pass
    time.sleep(10)

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Read settings
filename = '/home/pi/home-monitoring/config.csv'
readcsv=csv.reader(open(filename, 'r'))
for row in readcsv:
    if row[0] == 'user':
        _user = str(row[1])
    elif row[0] == 'password':
        _password = str(row[1])
    elif row[0] == 'database':
        _database = str(row[1])
    elif row[0] == 'host':
        _host = str(row[1])
    elif row[0] == 'port':
        _port = int(row[1])
    elif row[0] == 'tablename':
        _tablename = str(row[1])
    elif row[0] == 'period_sec':
        period_sec = int(row[1])
    elif row[0] == 'cutoff_day':
        cutoff_day = int(row[1])
    elif row[0] == 'timezone':
        _timezone = str(row[1])

# Preparing table
try:
    conn = DBMS.connect(user = _user, password = _password, database = _database, host = _host, port = _port)
    cur = conn.cursor()
    SQL = """CREATE TABLE IF NOT EXISTS %(_tablename)s (timestamp TIMESTAMPTZ,
                                                        temperature float,
                                                        pressure float,
                                                        humidity float);""" % {'_tablename': _tablename}
    cur.execute(SQL)
    conn.commit()
    cur.close()
    conn.close()
except Exception as err:
    print('Error when creating table:')
    print(str(err))
    
while True:
    time_start = datetime.datetime.now()
    time_difference = 0
    while time_difference < period_sec:
        time_difference_obj = datetime.datetime.now() - time_start
        time_difference = time_difference_obj.total_seconds()
        time.sleep(0.25)
    try:
        temperature = bme280.get_temperature()
        pressure = (bme280.get_pressure() * 0.1) * 7.50062
        humidity = bme280.get_humidity()
    except Exception as err:
        print('Error when reading sensor:')
        print(str(err))
        temperature = None
        pressure = None
        humidity = None
    try:
        conn = DBMS.connect(user = _user, password = _password, database = _database, host = _host, port = _port)
        cur = conn.cursor()
        SQL = """INSERT INTO %(_tablename)s (timestamp, temperature, pressure, humidity)
                VALUES (TIMESTAMP '%(_ts)s', %(_temp)s, %(_pres)s, %(_hum)s);""" % {'_tablename': _tablename,
                                                                       '_ts': datetime.datetime.now(pytz.timezone(_timezone)),
                                                                       '_temp': float(temperature),
                                                                       '_pres': float(pressure),
                                                                       '_hum': float(humidity)}
        cur.execute(SQL)
        conn.commit()
        SQL = """DELETE FROM %(_tablename)s
                WHERE timestamp < TIMESTAMP '%(_ts)s' - INTERVAL '%(cutoff_day)s days;'"""  % {'_tablename': _tablename,
                                                                                                 '_ts': datetime.datetime.now(pytz.timezone(_timezone)),
                                                                                                 'cutoff_day': cutoff_day}      
        cur.execute(SQL)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        print('Error when creating table:')
        print(str(err))