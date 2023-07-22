# Introduction
The source code of 
RAP-Plan, Window and 
Frame algorithms
used by _**RAP: A Policing Mechanism
Guaranteeing Sub-microsecond Determinism
against Abnormal Traffic in TSN**_ in RTSS 2023 paper #131.


# Getting Started

* Package installation
```commandline
pip install -r requirement.txt
```

# Run
* Run the file in the 
`\bin` directory to run 
the corresponding 
algorithm, e.g.,
```commandline
python main_for_RAP_demo.py
```

# Constraints in Phase II of RAP-Plan

**1. Period Constraint.**


This constraint requires that the TS frame of a period 
must be scheduled during the current period.
There are two reasons.
First, this constraint could reduce the buffered frames in the switch.
If the frame of (k+1)-th period has arrived 
while the frame of the k-th period has not been scheduled, 
then the switch needs to buffer two frames.
Yet the on-chip memory is limited.
Second, the constraint can reduce the search space 
to a reasonable range.
This constraint corresponds to 
the Frame constraint in citation#18.

![Period Constraint](.\res\constraints\1.png)

**2. Sequence Constraint.**

The routing of a TS frame is sequential.
The scheduling time on the upstream link must be 
earlier than the scheduling time on the downstream link.
Besides, the scheduling time between neighbor links 
must be larger than the worst processing and transmission delay.
Otherwise, the frame has not arrived 
at the downstream link but the link is 
already scheduling the frame.
The _rst_ has been lengthened in Phase I, 
thus the scheduling time of downstream 
only needs to be one _rst_ larger than 
the scheduling time of the upstream link.
This constraint corresponds to the 
Flow Transmission constraint in citation#18.

![Sequence Constraint](.\res\constraints\2.png)

**3. Queue Resource Constraint.**

The number of queues in the switch is typically less than 8.
The queues that can be used by TS frames are limited.
This constraint corresponds to 
the last sentence Section-4-2 in citation#18.

![Queue Resource Constraint](.\res\constraints\3.png)


**4. Deadline Constraint.**
TS streams have a strict end-to-end deadline.
The planned end-to-end delay must be 
less than the allowed maximum end-to-end delay.
This constraint corresponds to 
the End-to-End constraint in citation#18.

![Deadline Constraint](.\res\constraints\4.png)


**5. Contention-free constraint.**

Contention-free constraint ensures that 
frames through the same link cannot use the same raster.

![Contention-free constraint](.\res\constraints\5.png)

**6. Zero-aggregation constraint.**

If frames enter the same queue at link _(a,b)_,
once the gate of this queue opens at some raster,
frames in this queue will be scheduled 
at the same raster according to TAS.
This obeys the first sub-goal above.
Therefore, there should be only 
a single frame in a queue at the same time, 
i.e., zero-aggregation.

To avoid aggregation, the scheduling time 
for any two TS frames from upstream links 
can only be one of the following cases: 
(1) After the former frame has been scheduled 
to the downstream link, 
the latter frame is just scheduled at the upstream link; 
(2) The two frames use different queues.
The formulation of the first case is as Eq.(6).

![Zero-aggregation constraint](.\res\constraints\6.png)


We represent 
Eq.(6)
as $\Pi_{i,j}^{(a,b)}$. 
The complete constraint is 
shown in Eq.(7).

![Zero-aggregation constraint](.\res\constraints\7.png)

Contention-free constraint along with 
zero-aggregation constraint collaboratively 
achieves the first sub-goal.


**7. Single-frame-per-raster constraint.**


To achieve the second sub-goal, this constraint guarantees 
that frames from different upstream links 
$(x,a)$ and $(y,a)$ arrive at 
the current link $(a,b)$ 
at different rasters.

![Single-frame-per-raster constraint](.\res\constraints\8.png)