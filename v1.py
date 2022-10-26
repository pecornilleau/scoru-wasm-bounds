import math

vs=6000000
period=7 * 24 * 60 * 60
security_margin = 0.95

class Config:
	def __init__(self, log_base, speedup, binary, on_snapshot):
		self.log_base = log_base
		self.speedup = speedup
		self.binary = binary
		self.on_snapshot = on_snapshot

	def __str__(self):
		return "fast mode speedup={:d}\nlog base={:d}\nBinary search={:b}".format(self.speedup, self.log_base, self.binary)

	def lim_geo(self):
		ratio = 1.0 / self.log_base
		lim=1 / ( 1 - ratio)
		return lim

	def coef_Vf (self):
		if self.binary:
			return 5 * self.lim_geo()
		else:
			return self.lim_geo()

	def coef_Vs_p1(self, Ns):
		if self.on_snapshot:
			return 0
		elif self.binary:
			return 5 * math.log(Ns,self.log_base)
		else:
			return 32 * math.log(Ns,self.log_base)

	def coef_Vs_p2(self):
		return self.lim_geo()




c_linear = Config(2 , 5000, False , False)
c_precise = Config(2 , 5000, False , True)
c_linear_evenly = Config(32 , 5000, False , False)
c_binary = Config(2 , 5000, True , False)
c_binary_evenly = Config(32 , 5000, True , False)
c_precise_evenly = Config(32 , 5000, False , True)


def ls_of_ns(c,Ns):
	term_Vf = c.coef_Vf() * Ns / c.speedup
	term_Vs = c.coef_Vs_p1(Ns)  + c.coef_Vs_p2()
	nticks = vs * period * security_margin
	Ls = nticks / (term_Vf + term_Vs)
	return Ls

def print_from_ns(c,Ns):
	Ls = ls_of_ns(c,Ns)
	print ("----------------------")
	# print c
	# print ("------"
	print ("Ns = {:.2e}".format(Ns))
	print ("Ls = {:.2e}".format(Ls))
	print ("Lc = {:.2e}".format(Ls * Ns))


def ns_of_ls(c,Ls_target):
	Ns = 100000000
	while True:
		Ns = math.floor(Ns * 0.99)
		Ls = ls_of_ns(c,Ns)
		if Ls > Ls_target:
			break

	return Ns

def print_from_ls(c,Ls):
	Ns = ns_of_ls(c,Ls)
	print_from_ns(c,Ns)

print ("\n********************************\nNs = 50\n")
print_from_ns(c_linear,50)
print_from_ns(c_linear_evenly,50)
print_from_ns(c_binary,50)
print_from_ns(c_binary_evenly,100)

print ("\n********************************\nNs = 100\n")
print_from_ns(c_linear,100)
print_from_ns(c_linear_evenly,100)
print_from_ns(c_binary,100)
print_from_ns(c_binary_evenly,100)

print ("\n********************************\nNs = 1000\n")
print_from_ns(c_linear,1000)
print_from_ns(c_linear_evenly,1000)
print_from_ns(c_binary,1000)
print_from_ns(c_binary_evenly,1000)

# print ("\n********************************\nNs = 1000\n"
# print_from_ns(c_linear,1000)
# print_from_ns(c_binary,1000)
# print_from_ns(c_binary_evenly,1000)


# print ("\n********************************\nNs = 10000\n"
# print_from_ns(c_linear,10000)
# print_from_ns(c_binary,10000)
# print_from_ns(c_binary_evenly,10000)


# print ("\n***********************************\n"
# print_from_ns(c_linear,25)
# print_from_ns(c_linear_evenly,100000)
# # ls_of_ns(c_linear,50)
# # ls_of_ns(c_linear,100)
# # ls_of_ns(c_binary,5000)
# # ls_of_ns(c_binary,10000)
# print_from_ns(c_binary,20000)
# print_from_ns(c_binary_evenly,100000)

# print ("\n**************** LS = 25B *******************\n")
# Ls=25*1000000000
# print ("current")
# print (ns_of_ls(c_linear,Ls))
# print ("current + evenly distributed hashes")
# print (ns_of_ls(c_linear_evenly,Ls))
# print ("current + binary search")
# print (ns_of_ls(c_binary,Ls))
# print ("current + phase 1 on snapshots")
# print (ns_of_ls(c_precise,Ls))
# print ("current + evenly distributed + binary search")
# print (ns_of_ls(c_binary_evenly,Ls))
# print ("current + p1 on snapshots + evenly distributed")
# print (ns_of_ls(c_precise_evenly,Ls))


# print ("\n**************** LS = 36B *******************\n")
# Ls=36*1000000000
# print ("current")
# print (ns_of_ls(c_linear,Ls))
# print ("current + evenly distributed hashes")
# print (ns_of_ls(c_linear_evenly,Ls))
# print ("current + binary search")
# print (ns_of_ls(c_binary,Ls))
# print ("current + phase 1 on snapshots")
# print (ns_of_ls(c_precise,Ls))
# print ("current + evenly distributed + binary search")
# print (ns_of_ls(c_binary_evenly,Ls))
# print ("current + p1 on snapshots + evenly distributed")
# print (ns_of_ls(c_precise_evenly,Ls))


print ("\n**************** LS = 50B *******************\n")
Ls=50*1000000000
print ("current")
print (ns_of_ls(c_linear,Ls))
print ("current + evenly distributed hashes")
print (ns_of_ls(c_linear_evenly,Ls))
print ("current + binary search")
print (ns_of_ls(c_binary,Ls))
print ("current + phase 1 on snapshots")
print (ns_of_ls(c_precise,Ls))
print ("current + evenly distributed + binary search")
print (ns_of_ls(c_binary_evenly,Ls))
print ("current + p1 on snapshots + evenly distributed")
print (ns_of_ls(c_precise_evenly,Ls))


# print ("\n**************** LS = 100B *******************\n")
# Ls=100*1000000000
# print ("current")
# print_from_ls(c_linear,Ls)
# print ("current + evenly distributed hashes")
# print_from_ls(c_linear_evenly,Ls)
# print ("current + binary search")
# print_from_ls(c_binary,Ls)
# print ("current + phase 1 on snapshots")
# print_from_ls(c_precise,Ls)
# print ("current + evenly distributed + binary search")
# print_from_ls(c_binary_evenly,Ls)
# print ("current + p1 on snapshots + evenly distributed")
# print_from_ls(c_precise_evenly,Ls)

# import plotext as plt

# def f(x):
# 	return (x * ns_of_ls(c_linear,x))

# def g(x):
# 	return (x * ns_of_ls(c_linear_evenly,x))

# def h(x):
# 	return (x * ns_of_ls(c_binary,x))

# def i(x):
# 	return (x * ns_of_ls(c_precise,x))

# B=1000000000
# x = list(range(5 * B,100 * B,math.floor(0.1 * B)))
# y1 = list(map(f,x))
# y2 = list(map(g,x))
# y3 = list(map(h,x))
# y4 = list(map(i,x))
# # plt.plot(x,y1)
# plt.plot(x,y2)
# # plt.plot(x,y3)
# plt.plot(x,y4)
# plt.show()