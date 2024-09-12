# RenderProviderConductor
Website: https://www.conductortech.com/

# AUTH
https://docs.conductortech.com/reference/configuration/#api-key

# Performance/Price optimization
With Conductor you pay for the instance type with an
added fee for licenses used. Since core-counts pricing 
scales linearly, you usually want to use the fastest performing
core count to minimize time spent on license cost payments (licenses
are priced per instance NOT per core).
HOWEVER: In some cases more core counts does not scale linearly with performance.
Therefore, in some cases adding more cores may increase costs.

# HOUDINI KARMA CPU PERF
In my tests on KARMA CPU with Houdini 20.0.547,
using 64 cores seemed to give diminishing returns!

In waving flag test project (no ceonstock inputs, blownout render),
Using cw xeon3 instances.
30 frames at 960x540 
batch_size of 5.

  4core  ( 16gb mem): $0.42 (2.31min/frame)
  8core  ( 32gb mem): $0.35 (1.27/frame)
  16core ( 64gb mem): $0.46 (1.08min/frame)
  32core (128gb mem): $0.53 (0.70min/frame)
  64core (170gb mem): $0.72 (0.48min/frame)

Note: Make sure that the instance type has enough 
memory, since less cores generally come with less memory
