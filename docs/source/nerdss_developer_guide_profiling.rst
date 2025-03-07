Profiling
---------

1. Use tools like Shark or Gperftools.
2. Code spends most time evaluating bimolecular association. Large complexes may increase time spent breaking apart complexes.
3. Install Gperftools:
  a. On Ubuntu:
    i. `apt-get install libunwind8-dev`
    ii. `apt-get install libtool`
    iii. `git clone https://github.com/gperftools/gperftools.git`
    iv. `sudo apt-get install dh-autoreconf`
    v. `./autogen.sh`
    vi. `./configure`
    vii. `make`
    viii. `sudo make install`
    ix. `sudo ldconfig`
  b. Install `kcachegrind` or `qcachegrind` for output visualization:
    i. On Ubuntu:
      1. `sudo apt install kcachegrind`
      2. `sudo apt-get install graphviz gv`
    ii. On macOS:
      1. `brew install graphviz`
      2. `brew install qcachegrind --with-graphviz`
  c. Include `<gperftools/profiler.h>` and bracket the code to profile with `ProfilerStart()` and `ProfilerStop()`.
  d. Compile NERDSS with debugging symbols enabled and `-lprofiler`.
  e. Run the program.
  f. Convert `profile.log` to callgrind format: `pprof --callgrind ./nerdss profile.log > profile.callgrind`
  g. Visualize with `qcachegrind` (macOS) or `kcachegrind` (Ubuntu).