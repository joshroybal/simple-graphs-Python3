from random import normalvariate, choice, lognormvariate

def normdist(lo, hi):
    return [ normalvariate(0.0, 1.0) for i in range (hi-lo+1) ]

def normints(lo, hi):
    dist = normdist(lo, hi)
    dist.sort()
    scalar = abs(min(dist))
    dist = [ i + scalar for i in dist ]
    normalizer = (hi - lo) / max(dist)
    dist = [ i * normalizer for i in dist ]
    dist = [ lo + round(r) for r in dist ]
    return dist

def randint_normal(lo, hi):
    t = normints(lo, hi)
    return choice(t)

def lognormdist(lo, hi):
    return [ lognormvariate(0.0, 0.25) for i in range (hi-lo+1) ]

def lognormints(lo, hi):
    dist = lognormdist(lo, hi)
    #dist.sort()
    normalizer = (hi - lo) / max(dist)
    dist = [ i * normalizer for i in dist ]
    dist = [ lo + round(r) for r in dist ]
    return dist

def randint_lognormal(lo, hi):
    t = lognormints(lo, hi)
    return choice(t)
