with open('lyft.txt') as f:
  text = f.read()

recipt_strs = text.split('Your ride with')[1:]

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

for recipt_str in recipt_strs:
  second_part = recipt_str.split('Thanks for riding with ', 1)[1]
  datetime_str, third_part = second_part.split('Ride Details', 1)
  datetime_str = datetime_str.split('!')[1].strip()
  stats_str = third_part.splitlines()[1].split('Lyft fare (')[1]
  miles_time_str, price = stats_str.split(')\t$')
  miles_str, time_str = miles_time_str.split('mi, ')
  fourth_part = third_part.split('Pickup\t')[1]
  pickup_address = fourth_part.splitlines()[1].strip()
  dropoff_address = fourth_part.splitlines()[4].strip()
  dropoff_street = dropoff_address.split(' ', 1)[1]

  print 'datetime:', datetime_str
  print 'miles_str:', miles_str
  print 'time_str:', time_str
  print 'pickup_address:', pickup_address
  print 'dropoff_address:', dropoff_address
  print 'dropoff_street:', dropoff_street
