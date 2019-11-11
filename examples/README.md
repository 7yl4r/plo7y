
The `./examples/test_outputs/` dir is populated by output files from reporters
and/or plotters run on test data.
These plots are checked into git for easy viewing, but running the suite of
tests will overwrite these files.
The test example outputs *should* be identical but minor changes between
versions of libraries used and improperly-seeded random data generators could
break that; no guarantees.
