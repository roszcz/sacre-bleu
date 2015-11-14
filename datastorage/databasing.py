""" This should be visible only as db.update_base(key, val)? """
import tables
import settings as s

# For every photo we define a set of data called a Particle
class Particle(tables.IsDescription):
    # Beacause timestamping is crap in pytables 
    # we'll do custom timestamp -> string serialization
    #timestamp = tables.Time64Col()
    # Date should be in table meta-data?
    date_YMD = tables.StringCol(8)
    time_HMS = tables.StringCol(6)
    red      = tables.UInt32Col()
    green    = tables.UInt32Col()
    blue     = tables.UInt32Col()

# The name of our HDF5 filename
filename = "zupa.h5"

print("Creating file:", filename)

# Open a file in "w"rite mode
h5file = tables.open_file(filename, mode="a", title="Test file")

# Create a new group under "/" (root)
group = h5file.create_group("/", 'detector', 'Detector information')
group2 = h5file.create_group("/detector", 'dupector', 'Detector information')
print("Group '/detector' created")

# Create one table on it
table = h5file.create_table(group, 'readout', Particle, "Readout example")
print("Table '/detector/readout' created")

table2 = h5file.create_table(group2, 'dupadupa', Particle, 'duuupa')

p1 = table.row
p2 = table2.row
for it in range(10):
    p1['date_YMD'] = str(it**it)
    p1['red'] = it
    p2['blue'] = 1./(1 + it)
    p1.append()
    p2.append()
table.flush()
table2.flush()
