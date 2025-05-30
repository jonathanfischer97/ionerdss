Debugging
---------

1. Always check output for warnings using `grep`. Warnings like "can't solve overlap" or "separation <0" often indicate a bug or a very dense system.
2. Rerun with the same seed to isolate the error: `./nerdss -f parms.inp -s 1234091`
3. Run `sample_inputs/VALIDATE_SUITE`. Ensure it works on initial start (`-f parms.inp`) and on restart (`-r restart.dat`).
4. If you edited an include file, recompile clean by removing the `obj` directory to avoid segmentation faults.
5. Use debuggers like `gdb`, `lldb`, or `valgrind`:
  a. Recompile all code with `CFLAGS=-g` and remove `-O3`.
  b. Launch the debugger: `lldb nerdss`
  c. Run the program: `run -f parms.inp -s 123445`
  d. Use commands like `bt` (backtrace) and `print myVariable` to debug.
  e. On macOS, use `libgmalloc` for strict memory tracking: `env DYLD_INSERT_LIBRARIES=/usr/lib/libgmalloc.dylib`
  f. Use `help [command]` for assistance.
  g. Set breakpoints with `break file1.c:6` or `break my_func`.
  h. Use `step`, `next`, `watch my_var`, `backtrace`, `where`, `finish`, `delete`, `info breakpoints`, `stop`, and other commands as needed.
  i. For heap corruption issues, enable `-fsanitize=address` and reserve space in vectors.
