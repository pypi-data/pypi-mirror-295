# Known issues
Feel free to drop them as issues [here](https://github.com/FAIRmat-NFDI/pynxtools-apm/issues).
In decreasing order of relevance we are aware of the following technical issues with pynxtools-apm and its use in NOMAD OASIS.

## Eventually slow charge state analysis
When the ranging definitions have molecular ions which are composed from many atoms and elements with many isotopes
it is possible that the interpretation of the ranging definitions can take long. The situation is case dependent.
The reason is that a combinatorial algorithm is used for identifying the charge state(s) from the ranging definitions.
The computation time of this algorithm depends on number of isotopic combinations.

## Many warnings about non-finite values in the parsing log when using NOMAD OASIS
NOMAD Oasis by definition does not index non-finite values in its elasticsearch software component. The charge state analysis
typically though sets the half-life of each candidate to be infinite. This non-finite real value is picked up by NOMAD during
the parsing stage and causes the warning but does not cause the parsing to fail.

## Too complex molecular ions
Pynxtools-apm currently supports to define molecular ions with up to 32 atoms. This covers for almost all cases of molecular
ions typically studied with atom probe. Note that in mass spectrometry fragments with a considerable larger number of atoms
are observed but telling them apart in atom probe would in practice be even more complicated than it is in mass spectrometry.

## Too many ranging definitions when working with paraprobe-toolbox in a NOMAD Remote Tools Hub.
The post-processing software paraprobe-toolbox currently supports working with up to 255 ranging definitions.
In all cases where we have seen range files from groups across the world where more ranging definitions have been made,
these were typically duplicated definitions in the ranging definitions file. Pynxtools-apm does not imply such
restriction. As a result while the NeXus/HDF5 representation in NOMAD OASIS and its mapping on NOMAD metainfo works
when parsing files with more than 255 ranging definitions, these files may cause issues when post-processed using NORTH.

## Too many ranging definitions triggering NOMAD parsing failure
We observed two cases so far where parsing ranging definitions with both more than approximately thousand molecular ions
did not parse successfully, likely because of running limitations as a consequence of conservative default settings
in a default NOMAD installation related to elasticsearch.

A more detailed overview for resolving molecular ions in atom probe is available [in the literature](https://doi.org/10.1016/j.patter.2020.100192).

## Slow verification of instance data against cardinality and existence constraints
Version of pynxtools-apm which used pynxtools<=0.2.1 are known to face the issue that the verification of the instantiated schema can be slow.
With pynxtools>=0.3.1 this has been fixed thanks to a refactored verification algorithm.




