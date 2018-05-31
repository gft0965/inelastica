from Inelastica.SetupRuns import *

# After finishing the CGrun calculation we can
# generate FCrun and OSrun directoris with this script:

FCgroups = [[i, i+3] for i in range(46, 73, 4)]

for F, L in FCgroups:
    SetupFCrun('./CGrun', './FCrun_%i-%i'%(F, L), FCfirst=F, FClast=L, submitJob=True)

SetupOSrun('./CGrun', './OSrun')
