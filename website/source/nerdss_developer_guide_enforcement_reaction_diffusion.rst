Enforcement of Reaction and Diffusion Events per Timestep (Δt)
--------------------------------------------------------------

**isDissociated**: A property of the molecule used only when evaluating reaction probabilities for species undergoing 0th, 1st, or 2nd order reactions. Once reaction probabilities are set, it is not used for decision-making.

**moleculeList[mol].trajStatus**: Options include `trajStatus::propagated`, `trajStatus::none`, and `trajStatus::canBeResampled`. When a molecule undergoes a reaction, it should be set to `trajStatus::propagated`. Ideally, this should be a property of the complex, as it affects all molecules within the complex equally.

**moleculeList[mol].probvec[crossItr] = 0**: This vector belongs to each molecule but sums over all interfaces and possible reactions for that molecule. These probabilities decide if a reaction occurs for an interface on a molecule. They are set to zero for any molecule once any interface undergoes a reaction. They still need to be recorded for any pair of reaction partners with `r < Rmax` as `probvec = 0` to ensure volume exclusion.

1. **Creation Events**:

  - Occur first. If a molecule is created during the timestep Δt, it is prohibited from further diffusion by setting `moleculeList[mol].trajStatus = trajStatus::propagated`. This status must be synchronized/shared by every molecule in a complex, so it should ideally be a property of the complex.
  
  - The molecule is also prohibited from further reactions by setting `moleculeList[molItr].isDissociated = true`. This flag is unique to the molecule and not synchronized for every element in a complex. It prevents the molecule and its interfaces from undergoing further reactions but still allows volume exclusion. These interfaces will be listed in the reaction zone of nearby reaction partners (if they have free interfaces) but with reaction probabilities set to zero.

2. **Dissociation Events**:

  - Occur second. If an interface dissociates during the timestep Δt, the molecule containing that interface is prohibited from further diffusion by setting `moleculeList[mol].trajStatus = trajStatus::propagated`, along with every member of its complex.
  
  - The entire molecule is also prohibited from further reactions, including all other interfaces on this molecule, by setting `moleculeList[molItr].isDissociated = true`. This flag prevents the molecule and its interfaces from undergoing further reactions but still allows volume exclusion. These interfaces will be listed in the reaction zone of nearby reaction partners with reaction probabilities set to zero.
  
  - **Loop Closure Dissociation**: The probability of association reactions can be undersampled if the rate is high relative to the timestep. This is because first-order reactions are calculated one-at-a-time using a Poisson probability, which does not allow more than one reaction per evaluation. To correct this, the probability of dissociation is adjusted.

3. **Association Reactions**:

  - Occur last. All molecules are looped over to evaluate reaction probabilities for all interfaces within `Rmax` of a reaction partner. If a molecule has `isDissociated = true`, it cannot perform a reaction, so the probability is set to zero. However, the molecule is still present in the neighbor list of partners/interfaces to exclude volume with.
  
  - If molecules are in the same complex, the probability is evaluated using the first-order reaction rate.

4. **Association Events**:

  - Once all probabilities are evaluated, decisions are made on whether to perform an association event for a molecule. If an association occurs, `moleculeList[mol].trajStatus = trajStatus::propagated` is set for the molecule and every other molecule in its complex. `isDissociated` is not used in subsequent functions, so it does not need to be reset. All other reaction probabilities for this molecule, on all interfaces, are set to zero to prevent additional interactions. Other interfaces will still exclude volume.
