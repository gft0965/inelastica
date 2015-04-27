version = "SVN $Id$"
print version

import numpy as N
import Scientific.IO.NetCDF as NC

def write(fn,array,label,SinglePrec=False):
    """
    The simplest possible way to write an array to
    a new or existing NetCDF file
    """
    nc = NCfile(fn)
    vartype = 'd'
    if SinglePrec:
        if label in ['He_ph','ReHe_ph','ImHe_ph']:
            vartype = 'f'
    nc.write(array,label,vartype)
    nc.close()

class NCfile:
    
    def __init__(self,fn):
        "Returning instance of class."
        self.file = NC.NetCDFFile(fn,'a')
        self.fn = fn
        self.dimensions = self.file.dimensions
        self.variables = self.file.variables
        self.invdim = {}
        for d in self.dimensions:
            val = self.dimensions[d]
            self.invdim[val] = d
        
    def close(self):
        "Closes the file instance"
        self.file.close()
    
    def write(self,A,label,vartype='d'):
        "Writes numpy array to file"
        dim = self.__checkDimensions(A)
        print 'WriteNetCDF: Writing variable %s(%s) to file %s'%(label,vartype,self.fn)
        try:
            self.file.createVariable(label,vartype,dim)
        except:
            print '  ...variable %s already exist. Overwriting!!!'%label
        self.variables[label][:] = N.array(A,dtype=vartype)
        
    def __checkDimensions(self,A):
        shape = N.shape(A)
        dim = []
        for i in shape:
            try:
                d = self.invdim[i]
            except:
                d = 'd%.2i'%len(self.dimensions)
                'WriteNetCDF: Generating dimension %s'%d                
                self.file.createDimension(d,i)
                self.invdim[i] = d
            dim.append(d)
        return tuple(dim)
    
if __name__ == '__main__':

    # sample arrays
    a = N.ones((3,3))
    b = N.diag([1,2,3])
    c = a-b
    d = N.ones((3,3,3))/10
    e = N.arange(10,dtype=N.float)/100.
    #
    fn = 'test.nc'
    write(fn,a,'a')
    nc = NCfile(fn)
    nc.write(b,'b')
    write(fn,c,'c')
    write(fn,d,'mytest')
    write(fn,e,'energy')
    write(fn,c,'He_ph',True)
    nc.close()
