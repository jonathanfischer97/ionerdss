Volume Exclusion Implementation
-------------------------------

Volume exclusion is enforced only between species that can react with each other. To implement volume exclusion, a pair of interfaces must be assigned a bimolecular/binding reaction. If the reaction rate is set to 0, they will never react but will still exclude volume.

- By default, once a pair of molecules reacts/associates, they stop excluding volume. To force bound molecules to continue excluding volume, use the reaction flag `excludeVolumeBound=true`. By default, this is set to `false` because all sites must still participate in bimolecular reactions even when they cannot bind, which is computationally expensive. This flag is important for very dense systems to prevent reactants from overlapping after dissociation events.

For interfaces that attempt to associate but decide not to, all their reaction probabilities with their `Nrxn` partners are set to zero. This ensures that when the molecule updates its position, it avoids overlapping with all `Nrxn` partners by not positioning within the exclusion distance (`sigma`).

Multi-Site Molecules: For interfaces that do perform association, all other interfaces on that molecule are forbidden from performing reactions. Consequently, all reaction probabilities for these interfaces are set to zero, ensuring they avoid overlap with reaction partners despite being unable to bind.
