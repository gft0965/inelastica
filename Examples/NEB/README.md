Nudget elastic band (NEB)
=========================

The NEB command calculates a series of images between the start and end image (which I usually call `Left/Right L/R`). It can be used simply as

    NEB L R

where `L/R` are directories which contain a subdirectory `CGrun` which contain the two geometries, a `RUN.out` file and a `.XV` file with the converged geometries.

`NEB` uses the `SetupRuns` part of `Inelastica` which writes job files and submit them to the queue system. It then waits for the jobs to complete before submitting new jobs with updated geometries to find the NEB solution. Please see the documentation about the `~/.pbs` directory and `qsub` command useful for your cluster.  
