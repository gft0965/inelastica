NEB of hydroxyl switching
=========================

Nudged elastic band example OH molecule on Cu substrate.
The H atom has two enegetically equivalent positions pointing to the left/right of the O atom.
To do a NEB calculation you have to modify the starting images since the linear interpolation
moves the hydrogen straight through the oxygen atom. You do this by using the `-s` flag to initiate the geometries.

For instance:

    NEB -s L R -n 11 

Creates 11 images where the H atom just moves through the oxygen.

The python script FixStartGeom.py:

    python FixStartGeom.py 

edits the geometries fixing the O-H bond length and tries to equipartition the steps between the images.
Then you can run the NEB calculation as usual, e.g.,

      NEB -n 11 -p 8 L R 

At the end of the calculation you will find a very sharp barrier when the H is straight above the oxygen.

Note: The `FixStartGeom.py` script can be seen as an example of how to use `python` and `Inelastica` to control geometries.
