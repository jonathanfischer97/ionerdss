Adding a New Reaction Type
---------------------------

1. Add a new keyword for the reaction type in the `ReactionType` structure in `classes/class_Rxns.hpp`.
2. In `parse_reactions.cpp`, determine the reaction type based on the number of reactants and the "+" sign. Reactants appear before the arrow.
3. Create a temporary molecule type for each reactant in `parse_molecule_bngl` (line 138). Identify the molecule type based on parentheses "()" in the text.
4. Match the molecule type to the list of `MolTemplates` (line 139).
5. Create a temporary molecule type for each product in `parse_molecule_bngl` (line 170). Identify the molecule type based on parentheses "()" in the text.
6. Match the molecule type to the list of `MolTemplates` (line 171).
7. Set `molTypeIndex` to -2 if the `molTemplate` doesn't exist but the word "compartment" is present. Use this to decide the reaction type is transmission.
8. Determine which interfaces are involved in the reactions (line 228). This can only be done if the molecule has a `MolTemplate`.
