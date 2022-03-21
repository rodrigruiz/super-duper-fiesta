import json
import sys

class table:
    ''' 
    A class to handle the table with the analysis parameters. It includes the parameters for the fluxes, cross sections and probabilities.
    '''
    particles=["nu", "anu"]
    flavors  =["e", "mu", "tau"]
    channels =["cc", "nc"]

    def __init__(self, data=None):
        if (data is None):
            self.d={}
            self.d["xs"]=self.xs_default()
            self.d["flux"]=self.flux_default()
            self.d['p_cascade']=self.prob_default()
        else:
            d={}
            d["xs"]=self.xs_default()
            d["flux"]=self.flux_default()
            d['p_cascade']=self.prob_default()
            if (self.test_format(d,data)):
                self.d = data
            else:
                sys.exit("ERROR: The table does not match the format.")
            
    def get_table(self):
        return self.d

    def test_format(self, d, data):
        for key in d:
            if (key not in data):
                return False
            if (type(d[key]) is dict and type(data[key]) is dict):
                self.test_format(d[key],data[key])
        return True

    @classmethod
    def from_dict(cls, d):
        return cls(d)
        
    @classmethod
    def from_json(cls, path):
        with open(path,'r') as json_file:
            d=json.load(json_file)
        json_file.close()
        return cls(d)
        
    def flux_default(self):
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
        for p in self.particles:
            for f in self.flavors:
                m={'emin': None, 'emax': None}
                d={'phi': None, 'gamma': None}
                atm[p+'_'+f]={'metadata': m, 'data': d}

        flux["atm"]=atm
        return flux

    def xs_default(self):
        xs={}
        xm={'units': None}
        xs['metadata']=xm
        for p in self.particles:
            for c in self.channels:
                m={'emin': None, 'emax': None}
                d={'a1': None, 'a2': None, 'b1': None, 'b2': None}
                xs[p+'_'+c]={'metadata': m, 'data': d}
        return xs

    def prob_default(self):
        prob={}
        for p in self.particles:
            for f in self.flavors:
                for c in self.channels:
                    m={'emin': None, 'emax': None}
                    d={'phi': None, 'gamma': None}
                    prob[p+'_'+f+'_'+c]={'metadata': m, 'data': d}
        return prob

    def write(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.d, outfile)
        outfile.close()

    def set_atm_flux(self, neutrino, emin, emax, phi, gamma):
        if (neutrino in [str(i)+'_'+str(j) for i in self.particles for j in self.flavors]):
            self.d['flux']['atm'][neutrino]['metadata']['emin']=emin
            self.d['flux']['atm'][neutrino]['metadata']['emax']=emax
            self.d['flux']['atm'][neutrino]['data']['phi']=phi
            self.d['flux']['atm'][neutrino]['data']['gamma']=gamma
        else:
            print('WARNING: unknown flavor. Table is not updated')
        
    # def get_atm_flux(self):
    # def set_xs(self):
    # def get_xs(self):
    # def set_proba(self):
    # def get_proba(self):
