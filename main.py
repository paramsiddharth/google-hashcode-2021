# Google Hash Code 2021

# Libraries
from pprint import pp
from math import floor

TIME_SLICE = 1

# d -> Duration of simulation
# i -> Number of intersections
# s -> Number of streets
# v -> Number of cars
# f -> Bonus for each car that finishes
d, i, s, v, f = map(int, input().split())

streets = {}
for _ in range(s):
	# b -> Starting intersection
	# e -> Ending intersection
	# l -> Time taken to cross the street
	b, e, name, l = input().split()
	b, e, l = map(int, (b, e, l))
	streets[name] = {
		'start': b,
		'end': e,
		'duration': l
	}

cars = []
for _ in range(v):
	# p -> Number of streets
	# streets -> Names of streets
	p, *streets_ = input().split()
	p = int(p)
	cars.append({
		'street_count': p,
		'street_names': streets_,
		'position': streets[streets_[0]]['duration']
	})

special_streets = set()

for street_name, street in streets.items():
	if all([
		(street_name == car['street_names'][-1]
		and street_name not in car['street_names'][:-1])
		or street_name not in car['street_names']
		for car in cars
	]):
		special_streets.add(street_name)


intersections = dict.fromkeys(range(i), None)

for street_name, street in streets.items():
	if intersections[street['start']] is None:
		intersections[street['start']] = {
			'incoming': 0,
			'outgoing': 0,
			'incoming_streets': {},
			'outgoing_streets': {},
			'schedule': {}
		}
	intersections[street['start']]['outgoing'] += 1
	if intersections[street['end']] is None:
		intersections[street['end']] = {
			'incoming': 0,
			'outgoing': 0,
			'incoming_streets': {},
			'outgoing_streets': {},
			'schedule': {}
		}
	intersections[street['end']]['incoming'] += 1
	intersections[street['end']]['incoming_streets'][street_name] = street['duration']
	intersections[street['start']]['outgoing_streets'][street_name] = street['duration']

for ID, intersection in intersections.items():
	if all([
		street in special_streets
		for street in intersection['incoming_streets']
	]):
		continue
	
	if intersection['incoming'] == 1:
		intersection['schedule'][
			tuple(intersection['incoming_streets'].keys())[0]
		] = TIME_SLICE
	else:
		incoming_streets = list(intersection['incoming_streets'].items())
		incoming_streets.sort(key=lambda t: t[1], reverse=True)
		seconds = 1
		last_duration = None
		for street, duration in incoming_streets:
			intersection['schedule'][street] = seconds
			if duration != last_duration:
				seconds += 1
			last_duration = duration

count = len(tuple(filter(lambda sched: len(sched.keys()) > 0, (
	intersection['schedule'] for ID, intersection in intersections.items()
))))

print(count)
for ID, intersection in intersections.items():
	if len(intersection['schedule'].keys()) < 1:
		continue
	print(ID)
	print(len(intersection['schedule'].items()))
	for street_name, duration in intersection['schedule'].items():
		print(street_name, duration)