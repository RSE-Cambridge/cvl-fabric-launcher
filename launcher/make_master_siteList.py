import json
newlist=[
    {'name':'NeCTAR - Characterisation VL','url':'https://cvl.massive.org.au/cvl_flavours.json'},
    {'name':'Monash University - MASSIVE','url':'https://cvl.massive.org.au/massive_flavours.json'},
    {'name':'Australian Synchrotron - MASSIVE','url':'https://cvl.massive.org.au/massive_flavours.json'},
    {'name':'CQUniversity - HPC Systesm','url':'http://hpc-stats.cqu.edu.au/cqu.json'}
]

s=json.dumps(newlist,sort_keys=True, indent=4, separators=(',', ': '))
print s
