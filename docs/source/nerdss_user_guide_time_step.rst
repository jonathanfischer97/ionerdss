NERDSS and Time-Step Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To maintain at most two-body interactions between all reactant pairs per time-step, the time-step is usually limited by the bimolecular reactions, the density of the reactants, and their diffusion coefficients. Based on the definition of Rmax for the FPR algorithm [3], the minimum time-step for a given reactant B due to binding to A in 3D is:

.. math::

  \Delta t^{3D} = \frac{1}{56(D_A + D_B)} \left( \left( \frac{3}{4\pi\rho_A} + \sigma^3 \right)^{1/3} - \sigma \right)^2

where :math:`\rho_A = \frac{N_A}{V}`.

For 2D binding, the minimum time-step is:

.. math::

  \Delta t^{2D} = \frac{1}{36(D_A + D_B)} \left( \left( \frac{1}{\pi\rho_A} + \sigma^2 \right)^{1/2} - \sigma \right)^2

where :math:`\rho_A = \frac{N_A}{\text{Area}}`, and the diffusion coefficients are the slower values in 2D, comparable to lipid diffusion coefficients (~0.5 µm²/s). The dependence on :math:`\sigma` is weak as it nearly cancels for most systems. The time-step for the system is the minimum of all the time-steps, typically set to default values of 0.1-1 µs.

The time-step can also be limited by the speed of unimolecular reactions. This is mitigated by the fact that unimolecular reactions in NERDSS are determined on a population level. Instead of evaluating the probability for each species individually, the number of events is calculated from a Poisson distribution based on the total number of species. However, for a model where only one molecule can form a complex and dissociate, if :math:`k \cdot \Delta t` is relatively large (e.g., >0.001), errors can occur because more than one event should occur over the course of :math:`\Delta t`, but only one is allowed. Hence, a smaller time-step is necessary.

NERDSS will still propagate dynamics effectively with steps larger than the minimum suggested above. Particularly if systems spend minimal time in their densest state, the error due to choosing a larger step will be small. Empirically, the error for many-body systems is relatively small even when the two-body requirement is not closely maintained. Nonetheless, a smaller time-step will ensure more accurate propagation of dynamics.
