import re, math

with open('lyft.txt') as f:
  text = f.read()

receipt_strs = text.split('Your ride with')[1:]

'''
Your ride with Sabrina on June 1
Inbox
x

Lyft Ride Receipt <no-reply@lyftmail.com>
10:55 AM (13 hours ago)
to me
 Lyft
Photo of Sabrina
Thanks for riding with Sabrina!
June 1, 2018 at 10:36 AM


Ride Details
Lyft fare (4.93mi, 10m 38s)	$14.22

 PayPal account	$14.22
This and every ride is carbon neutral

Learn more
Ride Map

Pickup	10:36 AM
 	362 Joost Ave, San Francisco, CA

Drop-off	10:47 AM
 	25 Decatur St, San Francisco, CA
'''

'''
Ride Details
Base fare $2.00
9m 14s  $2.03
5.37 mi $6.50
Service fee $2.00
Tip $1.00
'''

def parse_rides():
  class Ride:
    pass

  for receipt_str in receipt_strs:
    try:
      second_part = receipt_str.split('Thanks for riding with ', 1)[1]
      datetime_str, third_part = second_part.split('Ride Details', 1)
      datetime_str = datetime_str.split('!')[1].strip()
      if ' fare (' in third_part:
        stats_str = third_part.splitlines()[1].split(' fare (')[1]
        miles_time_str, price = re.split(r'\)\s+\$', stats_str, 1)
        miles_str, time_str = miles_time_str.split('mi, ')
      else:
        stats_part = third_part.split('Ride Map', 1)[0]
        time_str = stats_part.strip().splitlines()[1].split('$', 1)[0]
        price = stats_part.rsplit('$', 1)[-1]
      if 'Lyft Line Discount' in third_part:
        is_line = True
      else:
        is_line = False
      minutes_str, seconds_str = time_str.split('m ')
      seconds_str = seconds_str.split('s')[0]
      minutes, seconds = int(minutes_str), int(seconds_str)
      fourth_part = re.split(r'Pickup\s', third_part)[1]
      pickup_address = fourth_part.splitlines()[1].strip()
      pickup_street = pickup_address.split(' ', 1)[1].split(' ', 1)[0]
      dropoff_address = fourth_part.splitlines()[4].strip()
      dropoff_street = dropoff_address.split(' ', 1)[1].split(' ', 1)[0]
    except:
      print 'failed to parse:'
      print second_part
      import pdb; pdb.set_trace()
      raise

    ride = Ride()
    ride.pickup_street = pickup_street
    ride.dropoff_street = dropoff_street
    # print 'miles_str:', miles_str
    ride.minutes = minutes
    ride.seconds = seconds
    ride.total_seconds = minutes * 60 + seconds
    ride.is_line = is_line
    # print 'pickup_address:', pickup_address
    # print 'pickup_street:', pickup_street
    # print 'dropoff_address:', dropoff_address
    # print 'dropoff_street:', dropoff_street
    # print
    yield ride

rides = parse_rides()
from_to_times = {}
for ride in rides:
  if ride.is_line:
    continue
  from_to_times.setdefault(ride.pickup_street, {})
  from_to_times[ride.pickup_street].setdefault(ride.dropoff_street, [])
  from_to_times[ride.pickup_street][ride.dropoff_street].append(ride.total_seconds)

from_to_del = []
for from_street in from_to_times:
  to_to_del = []
  for to_street in from_to_times[from_street]:
    if len(from_to_times[from_street][to_street]) <= 1:
      to_to_del.append(to_street)
  for del_key in to_to_del:
    del from_to_times[from_street][del_key]
  if not from_to_times[from_street]:
    from_to_del.append(from_street)
for del_key in from_to_del:
  del from_to_times[del_key]

def total_trips(from_key):
  sum_ = 0
  for to_key in from_to_times[from_key]:
    sum_ += len(from_to_times[from_key][to_key])
  return sum_

for from_street in sorted(from_to_times, key=lambda from_key: total_trips(from_key)):
  if total_trips(from_street) <= 3:
    continue
  print 'from:', from_street
  for to_street in from_to_times[from_street]:
    seconds_list = from_to_times[from_street][to_street]
    if len(seconds_list) <= 3:
      continue
    avg_seconds = sum(seconds_list) / float(len(seconds_list)) if seconds_list else 0
    print '  to:', to_street, 'n:', len(seconds_list), 'avg:', \
          int(math.floor(avg_seconds / 60)), 'm', int(round(avg_seconds % 60)), 's'
