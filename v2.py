import math

Vs=6000000
period=7 * 24 * 60 * 60
max_int = 2**63 -1
threshold=0.0001

def lim_geo(partition):
	ratio = 1.0 / partition
	lim=1 / ( 1 - ratio)
	return lim

class Current:
    def __init__(self, Lc, evenly, binary):
        self.Lc = Lc
        if evenly:
            self.log_base = 32
            self.lim = lim_geo(32)
        else:
            self.log_base = 8
            self.lim = lim_geo(8)
        if binary:
            self.nb_check = 5
            self.iter_vf = 5
        else:
            self.nb_check = 32
            self.iter_vf = 1

    def ls_(self,Ns):
        return (period - (self.iter_vf * self.lim * 15 * 60)) / (self.nb_check * math.log(Ns, self.log_base) + self.lim) * Vs

    def ns(self,seed):
        Ns = self.Lc / seed
        Ls_new = self.ls_(Ns)
        error = abs(seed - Ls_new) / seed
        if error < threshold:
            return Ns
        else:
            return self.ns(Ls_new)

    def ls(self):
        return self.ls_(self.ns(1))

class SnapshotFirst:
    def __init__(self, Lc, evenly):
        self.Lc = Lc
        if evenly:
            self.lim = lim_geo(32)
        else:
            self.lim = lim_geo(8)

    def ls(self):
        return (period - (self.lim * 15 * 60)) / self.lim * Vs

def improvement(value,ref):
    return abs(value - ref) / ref

def print_value_improv(value,ref):
    print ("Ls={:.2e}".format(value))
    print ("improvement={:.2f} %".format(improvement(value,ref)))

def compare(scenario,ref):
    value = scenario.ls()
    value_ref = ref.ls()
    print_value_improv(value,value_ref)

# Current situation
current = Current(max_int,False,False)
Ls_current = current.ls()
print ("Current situation")
print ("Lc={:.2e}".format(max_int))
print ("Ls={:.2e}".format(Ls_current))


# How accurate is the approximation of ignoring the "1.14"

Lc = max_int
lim = lim_geo(8)

def ls_approx(Ns):
    return period / (32 * math.log(Ns,8)) * Vs

def ns(Ls):
    Ns = Lc / Ls
    Ls_new = ls_approx(Ns)
    error = abs(Ls - Ls_new)

    if error / Ls < threshold:
        return Ns
    else:
        return ns(Ls_new)

Ls_seed = 1
Ns = ns(Ls_seed)
Ls_approx = ls_approx(Ns)
approx = abs((Ls_current - Ls_approx) / Ls_current)
print ("margin of error of approximation in design doc: {:f} %".format(improvement(current.ls(),Ls_approx)))

# Current situation but Lc estimated with speedup 50000
Vf = 50000 * Vs
Lc = 15 * 60 * Vf
optimistic_current = Current(Lc, False, False)
print ("\nCurrent situation but more precise Lc (speedup 50000)")
print ("Lc={:.2e}".format(Lc))
compare(optimistic_current, current)

# Target refutation
target = SnapshotFirst(max_int, False)
print ("\nTarget refutation vs Current situation")
compare(target,current)

# Binary search
binary = Current(max_int, False, True)
print ("\nCurrent situation + binary vs Current situation")
compare(binary,current)

# Even distribution
even = Current(max_int, True, False)
print ("\nCurrent situation + even distribution vs Current situation")
compare(even,current)

# Target refutation + even
target_even = SnapshotFirst(max_int, True)
print ("\nTarget refutation + even distribution vs Target")
compare(target_even,target)

