
import neo

#create a reader
reader = neo.io.NeoHdf5IO(filename='Results/NeuroMLTest_nest.h5')
# read the blocks
blks = reader.read(cascade=True, lazy=False)
print blks
# acces to segments
for blk in blks:
    print blk.name
    for seg in blk.segments:
        print seg.name
        for asig in seg.analogsignals:
            print asig
        for asiga in seg.analogsignalarrays:
            print asiga.name
            print asiga
        for st in seg.spiketrains:
            print st


