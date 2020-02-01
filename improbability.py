from numpy.random import seed
from numpy.random import rand
import random
import argparse
import sys
import time
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import multiprocessing


def animate(improb_fact):
	global xs, ys

	ys.append(improb_fact)

	if len(ys) > 70:
		dist = len(ys) - 70
		ys = ys[dist:]

	xs = range(0, len(ys))

	ax1.clear()
	ax1.plot(xs, ys)

	ax1.set_ylim(-0.001, 0.001)


def norm_improb(a, b, c):
	global improbs, bigskew, smallskew, eskew, triskew, args, alphaskew

	if a < b < c:
		improbs.append(b)

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Jump: " + str(b) + " Improbability Factor: " + str(average))

	if (a - b) > c:
		new = []

		for x in improbs:
			x = x * c
			new.append(x)

		improbs = new

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Skew (Big): " + str(c) + " Improbability Factor: " + str(average))

	if (a - b) < c:
		new = []

		for x in improbs:
			x = x * (1 / c)
			new.append(x)

		improbs = new

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Skew (Small): " + str(c) + " Improbability Factor: " + str(average))

	if ((a ** 2.0) + (b ** 2.0)) == (c ** 2.0):
		new = []

		for x in improbs:
			x = 0.5 * a * x
			new.append(x)

		improbs = new

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Skew (Triangle): " + str(c) + " Improbability Factor: " + str(average))

	if "5" in str(a) and "5" in str(b) and "5" in str(c):
		new = []

		for x in improbs:
			x = x * (1 / (a * b * c) ** 0.5)
			new.append(x)

		improbs = new

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Skew (E): " + str(c) + " Improbability Factor: " + str(average))

	if a > (a - c + b):
		new = []

		for x in improbs:
			x = x * (a - c + b)
			new.append(x)

		improbs = new

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		if args.verbose:
			print("Improbability Skew (Alpha): " + str(a - c + b) + " Improbability Factor: " + str(average))


def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')


def decision(probability):
	return rand() < probability


def epoch(parts, args):
	global iteration, improbs

	iteration = 0

	seed(random.randint(0, 20))

	while iteration < (random.randint(0, args.iterations)):

		a = (0 + (rand() * (100000000 - 0)))
		b = (0 + (rand() * (100000000 - 0)))
		c = (0 + (rand() * (100000000 - 0)))

		norm_improb(a, b, c)

		if args.graph:

			avg = 0
			for i in improbs:
				avg += i

			average = avg / len(improbs)

			animate(average)
			fig.canvas.draw()

		iteration += 1

	avg = 0
	for i in improbs:
		avg += i

	average = avg / len(improbs)

	print(str(iteration) + " iterations for epoch " + str(x) + " ending with an improbability factor of " + str(average))

	parts.append(average)


if __name__ == '__main__':
	xs = []
	ys = []

	parts = []
	procs = []

	print("Number of cpu : ", multiprocessing.cpu_count())

	my_parser = argparse.ArgumentParser(description='Calculate IMPROBABILITY')

	my_parser.add_argument('-i', '--iterations', type=int, help='Calculate improbability for an iteration set or set upper bound of improbability set for epochs.')
	my_parser.add_argument('-e', '--epochs', type=int, help='Calculate improbability for a set of epochs. Requires -i argument.')
	my_parser.add_argument('-g', '--graph', type=str2bool, nargs='?', const=True, default=False, help="Show Graph.")
	my_parser.add_argument('-v', '--verbose', type=str2bool, nargs='?', const=True, default=False, help="Print Skews and Jumps.")
	my_parser.add_argument('-p', '--probability', type=str2bool, nargs='?', const=True, default=False, help="Calculate and display the resulting choice based on improb factor.")

	iteration = 0

	a = 0
	b = 1
	c = 2

	improbs = [0]
	triskew = 0
	bigskew = 0
	smallskew = 0
	eskew = 0
	alphaskew = 0

	args = my_parser.parse_args()

	seed(random.randint(0, 30))

	if args.graph:

		style.use('fivethirtyeight')

		plt.ion()
		fig = plt.figure()
		ax1 = fig.add_subplot(1, 1, 1)

	if args.iterations and not args.epochs:

		print("Starting calculation for " + str(args.iterations) + " iterations of improbability...")
		time.sleep(3)

		while iteration < args.iterations:

			a = (0 + (rand() * (100000000 - 0)))
			b = (0 + (rand() * (100000000 - 0)))
			c = (0 + (rand() * (100000000 - 0)))

			sys.stdout.write("\033[F")  # Cursor up one line
			sys.stdout.write("\033[K")  # Clear to the end of lin

			norm_improb(a, b, c)

			print("[" + str(iteration) + "] iterations...")

			iteration += 1

		avg = 0
		for x in improbs:
			avg +=x

		average = avg / len(improbs)

		sys.stdout.write("\033[F")  # Cursor up one line
		sys.stdout.write("\033[K")  # Clear to the end of lin

		print(str(iteration) + " iterations ending with an improbability factor of " + str(average))

		if args.probability:
			decision = decision(average)
			print("Decision:", decision)

	elif args.epochs and not args.graph:

		print("Starting calculation for " + str(args.epochs) + " epochs of improbability...")
		time.sleep(3)

		if not args.iterations:
			print("No iterations given for epochs... use the -i flag.")
			sys.exit(0)

		with multiprocessing.Manager() as manager:
			parts = manager.list()  # <-- can be shared between processes.

			for x in range(0, args.epochs):
				proc = multiprocessing.Process(target=epoch, args=(parts, args))
				procs.append(proc)
				proc.start()

			for x in procs:
				x.join()

			avg = 0
			for x in parts:
				if decision(.5):
					avg += x
				else:
					avg -= x

			average = (avg / len(parts))

			print(str(args.epochs) + " epochs ending with an improbability factor of " + str(average))

			if args.probability:
				decision = decision(average)
				print("Decision:", decision)

	else:

		print("Starting calculation for infinite* improbability...")
		time.sleep(3)

		start_time = dt.datetime.today().timestamp()

		finite_improb = rand()

		while finite_improb != rand():

			a = (0 + (rand() * (100000000 - 0)))
			b = (0 + (rand() * (100000000 - 0)))
			c = (0 + (rand() * (100000000 - 0)))

			sys.stdout.write("\033[F")  # Cursor up one line
			sys.stdout.write("\033[K")  # Clear to the end of lin

			norm_improb(a, b, c)

			time_diff = dt.datetime.today().timestamp() - start_time

			print("[" + str(iteration) + "] iterations at " + str(iteration // time_diff) + " iter per sec...")

			if args.graph:

				avg = 0
				for x in improbs:
					avg += x

				average = avg / len(improbs)

				animate(average)
				fig.canvas.draw()

			iteration += 1

		avg = 0
		for x in improbs:
			avg += x

		average = avg / len(improbs)

		sys.stdout.write("\033[F")  # Cursor up one line
		sys.stdout.write("\033[K")  # Clear to the end of lin

		print(str(iteration) + " iterations ending with an improbability factor of " + str(average))

		if args.probability:
			decision = decision(average)
			print("Decision:", decision)

