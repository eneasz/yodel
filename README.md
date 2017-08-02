Simple script in python3 to track on delivery day for Yodel parcel.

I found it very useful to be able how many deliveries are before me.
Running script in the background will keep checking every 120s delivery
queue and if it reach less than 5 parcel will sound alarm.
Every time it checks queue, will print status update.

To install dependencies run:

	pip install -r require.txt

After that run:

	python3 yodel.py
