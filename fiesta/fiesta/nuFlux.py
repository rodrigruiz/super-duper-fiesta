def read_flux_file(f):
    d={}
    log_e, nue, numu, nuebar, numubar = ([] for i in range (5))
    File = open(f,"r")
    lines = File.readlines()
    for line in lines:
        columns = line.split(' ')
        log_e.append(float(columns[0]))
        nue.append(float(columns[1]))
        numu.append(float(columns[2]))
        nuebar.append(float(columns[3]))
        numubar.append(float(columns[4]))
    d["log_E"]=np.array(log_e)
    d["E"]=np.power(10, np.array(log_e))
    d["nu_e"]=np.array(nue)
    d["nu_mu"]=np.array(numu)
    d["nu_e_bar"]=np.array(nuebar)
    d["nu_mu_bar"]=np.array(numubar)
    File.close()
    return d

