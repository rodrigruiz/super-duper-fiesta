import json

class table:
    particles=["nu", "anu"]
    flavors  =["e", "mu", "tau"]
    channels =["cc", "nc"]

    def __init__(self):

    def flux(self):
        flux={}
        fm={}
        fm["units"]=None
        flux["metadata"]=fm

        astro={}
        astro["phi"]  =None
        astro["gamma"]=None
        astro["e0"]   =None
        astro["c0"]   =None

        flux["astro"] =astro

        atm={}
        for p in particles:
            for f in flavors:
                m={'emin': None, 'emax': None}
                d={'phi': None, 'gamma': None}
                atm[p+'_'+f]={'metadata': m, 'data': d}

        flux["atm"]=atm
        return flux

    def xs(self):
        xs={}
        xm={'units': None}
        xs['metadata']=xm
        for p in particles:
            for c in channels:
                m={'emin': None, 'emax': None}
                d={'a1': None, 'a2': None, 'b1': None, 'b2': None}
                xs[p+'_'+c]={'metadata': m, 'data': d}
        return xs

    def prob(self):
    def write(self, filename):
    def set_atm_flux(self):
    def get_atm_flux(self):
    def set_xs(self):
    def get_xs(self):
    def set_proba(self):
    def get_proba(self):
