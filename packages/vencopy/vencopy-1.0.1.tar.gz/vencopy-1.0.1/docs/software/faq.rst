.. venco.py documentation source file, created for sphinx

.. _faq:


Frequently Asked Questions (FAQs)
===================================

1. What is the geographical resolution of venco.py? venco.py is currently based 
on the national travel survey for passenger vehicles in Germany (MiD2017) and, 
as such, intrinsically provides information on demand and flexibility 
in high temporal resolution - down to 10 minutes - for EVs at national scale. 
As these profiles are provided with respect to an average vehicle, they can 
however be scaled to a higher geographical resolution (e.g. subnational, 
regional level) by multiplying them with vehicle fleet details (number of 
vehicles).


2. Which aggregation methods are employed to go from single profiles to fleet 
profiles? Currently, to go from single profiles to a fleet profile, venco.py 
employs an averaging method for uncontrolled charging, drain and rated power. 
For fleet battery profile calculations, a security parameter *alpha* is 
employed. The *alpha* value is a percentage value that selects the nth highest 
value for each hour of the minimum and maximum profiles. For example, if 
*alpha* equals 10 (10 is the default value), the 10% highest (respectively 10% 
smallest) values are disregarded in the calculation of the maximum and minimum 
state of charge of the fleet battery. 


3. Is the the MiD dataset open-access? The MiD dataset(s) is not open-access 
but can be requested for scientific purposes :ref:`here
<https://daten.clearingstelle-verkehr.de/279/>`.


4. Are seasonal differences accounted for in venco.py output profiles? 
(temperature dependency etc.) Currently, temperature dependency is not 
accounted for in the calculation of the electricity consumption but may be part 
of the next release.


5. Can representative profiles be derived in order not to have to do an 
aggregation to fleet level? It is possible to use individual profiles by 
avoiding the aggregation step in the FlexEstimator class. However, venco.py 
currently does not calculate profiles representative for specific charging station types (e.g. 
home charging, public charging).


6. Are multi-day SoC and plugging behaviour accounted for? Plugging behaviour 
and multi-day SoC are currently not included. However, because of the iteration
procedure in the FlexEstimator, it is ensured that the SoC is equal at 
beginning and end of each day for almost every profile. 


7. Are charging availabilities and distributions modelled? The grid 
infrastructure can be modelled with a simple binary True-False mapping based 
on purpose for which the trip was carried out, or based on charging 
availabilities distributions.
