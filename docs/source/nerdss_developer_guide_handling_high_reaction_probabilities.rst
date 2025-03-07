Handling High Reaction Probabilities
------------------------------------

For reactions with very large rates occurring in relatively large time steps (Δt), the probabilities can become significant. For bimolecular (2nd order) reactions involving diffusion to collision, it is challenging to reach such high levels. However, if probabilities approach 1, reducing the time step is necessary.

The primary issue is that with very high probabilities, individual molecules are more likely to perform multiple reactions per step. For example, one interface may undergo dissociation while another interface undergoes association. For multi-site molecules, multiple events per time-step are not allowed. For complexes, reactions are not restricted, only diffusion. This means that reactions with a high probability of occurring to one molecule are prohibited if another highly probable reaction has already occurred. 

For high-probability coupled reactions (binding and unbinding), particularly in assembled complexes, discrepancies in expected events can occur due to one event/reaction prohibiting another reaction from occurring. This deviates from the expectation for fully independent reactions. Typically, these issues arise when kon >= 100 nm³/µs and koff >= 10,000/s. If either reaction is slower, the number of events does not diverge significantly from the expectation for independent events, making the error negligible.

Unimolecular Reactions
~~~~~~~~~~~~~~~~~~~~~~

Unimolecular reactions are treated in two ways: either one-at-a-time or as a population. The population method is faster but does not maintain consistent kinetics in the large rate/time-step regime. The two methods do not sample identical mean values, requiring a correction when mixed. If both forward and reverse reactions use the population method, no correction is needed for equilibrium, but kinetics depend on the timestep. If both use the one-at-a-time method, kinetics are accurate, and a small correction is needed for high-probability regimes to achieve the correct equilibrium.

Loop-Closure Reactions
~~~~~~~~~~~~~~~~~~~~~~

When association reactions occur within a complex, such as a trimer closing, the reaction does not involve diffusion and is treated as a unimolecular reaction with generally high probability. The population method cannot be used here because association reactions are evaluated per reaction pair based on their spatial distribution. An inconsistency arises because the population method used for dissociation and the one-at-a-time method used for loop-closure reactions do not have the same mean except as Δt approaches small values.

Correction for Loop-Closure Reactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In high-rate and large time-step regimes, too few association reactions occur due to performing only 0 or 1 reaction per reactant pair (one-at-a-time), relative to dissociation reactions following the population mean. The mean for the population is:

.. math::

  \bar{x}_{\text{pop}} = k_{\text{close}} \Delta t

The mean for the one-at-a-time method is:

.. math::

  \bar{x}_{\text{one}} = 1 - \exp(-k_{\text{close}} \Delta t)

From the Taylor expansion, \(\exp(-k_{\text{close}} \Delta t) \approx 1 - k_{\text{close}} \Delta t\), these are the same in the limit of small \(k_{\text{close}} \Delta t\). The relative error in the mean is:

.. math::

  \frac{\delta \bar{x}}{\bar{x}} = \frac{k_{\text{close}} \Delta t - 1 + \exp(-k_{\text{close}} \Delta t)}{k_{\text{close}} \Delta t}

To correct this discrepancy, we lower the dissociation probability for events attempting dissociation as part of a closed loop. Calculate a new dissociation probability for each of the \(N_{\text{events}}\) selected from the population method:

.. math::

  p_{\text{dissoc}}(\Delta t) = \frac{1 - \exp(-k_{\text{close}} \Delta t)}{k_{\text{close}} \Delta t}

Then,

.. math:: 
  
  if(\text{URN} > p_{\text{dissoc}}(\Delta t))
  
the dissociation event is canceled, and the bond remains intact. Consequently, the number of dissociation events will be slightly reduced compared to the mean expected from the dissociation rate. The number of dissociation events \(n\) is sampled using the binomial distribution, where the probability of an event occurring is:

.. math::

  \text{prob}(\Delta t) = 1 - \exp(-k_{\text{dissoc}} \Delta t)

.. math::

  \text{binomial}(n; \text{prob}(\Delta t), N_{\text{bonds}})
