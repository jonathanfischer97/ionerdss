Adding Input Parameters
-----------------------

1. Add the keyword in the appropriate parser file. E.g., `src/parser/parse_reaction.cpp` for reaction parameters or `src/parser/parse_molFile.cpp` for molecule parameters. Follow existing examples.
2. Define the keyword. E.g., `enum RxnKeyword` in `include/classes/class_Parameters.hpp` or `include/class/class_Rxns.cpp`.
3. Declare the variable. E.g., `include/classes/class_Rxns.hpp` or `include/classes/class_bngl_parser.hpp` or `include/classes/class_MolTemplate.hpp`.
4. Set the variable value from input. E.g., `src/classes/class_bngl_parser_functions.cpp` and `src/classes/class_rxns.cpp`, or `src/classes/class_Parameters.cpp`, or `src/classes/class_MolTemplate.cpp`.
5. For reaction parameters, ensure they are assigned in all relevant places, such as `parsedRxn` and `forwardRxn`. E.g., `src/classes/class_rxns.cpp`.
6. Add the variable to an existing variable, if necessary. E.g., in `src/parser/parse_reaction.cpp`.
7. Add to restart functionality in both `src/io/write_restart.cpp` and `src/io/read_restart.cpp`.
