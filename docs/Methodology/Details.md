NERC LMTF Load Modeling Process
===============================

Initial Draft: 2/26/2020

Tony Faris, BPA

Objectives
----------

A composite load model is used by planners across North America to run
power system studies and simulate response of load to system events. The
development of load models can be a complex process, requiring
engineering expertise to collect and interpret large amounts of
historical measurement data. The Load Modeling Task Force (LMTF) of the
North American Electric Reliability Corporation (NERC) began a renewed
effort to generate accurate load models in 2019, by expanding upon
numerous past efforts that have completed across the region.

At the root of the effort is the composition of loads into seven major
load types: Motor A, Motor B, Motor C, Motor D, Power Electronic, Static
Resistive, and Static Current. For any given feeder, the contribution of
each of these load types can vary greatly based on numerous factors,
including season, time of day, and day of week. The goal of LMTF is to
generate load composition data sets for three main periods of interest:
summer peak, winter peak, and spring light load.

When looking across multiple feeders, load patterns and response can be
traced to numerous factors, but perhaps the most fundamental one is
regional climate. For this reason, each of the major areas in NERC
(ERCOT, MRO, NPCC, PJM, SERC, SPP, and WECC) was divided into unique
climate regions. The NERC LMTF worked with each regional entity to
select representative cities within each climate region, and developed
initial composition datasets for these cities. The regional entities
then mapped all of their feeders to the appropriate representative city,
creating a full load composition within the load model. This document
outlines the process undertaken by the NERC LMTF to develop the load
compositions for these representative cities.

Load Modeling Methodology
-------------------------

The overall methodology outlined in Figure 1 is divided into three major
steps. First, offline studies are completed to compile the
*city-dependent* and *city-independent* metadata required for this
process. Using this metadata for each city, 24-hour load shapes are
generated for each of the three seasons under study. Finally, these load
shapes are translated into load composition percentages using "Rules of
Association" mapping information.

![](media/image1.png){width="4.832000218722659in"
height="2.821783683289589in"}

Figure : Load Modeling Methodology

Each city requires three 24-hour weather profiles, identifying summer,
winter, and spring days respectively. Electrification percentages for
heating, cooling, water heating, and cooking are specified for each
city, as well as each type of building. The residential and commercial
buildings are modeled such that end use loads are dependent on the
hour-of-day and weather conditions. The following sections will outline
the process of creating the weather profiles, building models, and
electrification percentages.

Weather Profiles
----------------

When creating weather profiles, it is important to note that both
temperature *and* humidity factor greatly into end use load behavior.
For this reason, a Heat Index (HI) is calculated, as defined by the
National Weather Service (<https://www.weather.gov/safety/heat-index>).
The HI provides an indication of the "feel" of the temperature, and is a
better indicator of behavior than temperature alone.

There are multiple methods for collecting weather data and deriving the
24-hour HI profiles. Past efforts have used the Typical Meteorological
Year (TMY) dataset provided by the National Renewable Energy Laboratory
(NREL) to identify historical peak load days in summer and winter, as
well as light load days in spring. The NERC LMTF team has chosen to
collect historical weather data and use statistical analysis to
determine these days of interest, using the following process:

1.  For each city in the study, 20 years of hourly temperature and
    humidity data were collected. For US cities, this was retrieved from
    the National Oceanic and Atmospheric Administration (NOAA) website
    via their Local Climatological Data (LCD) set. For Canadian cities,
    these data were found on the website for the Government of Canada
    (Canada.ca). Both data sets provide hourly measurements, and
    appropriate steps were taken to interpolate or remove invalid
    points.

2.  The Heat Index was calculated for each hour in the 20 year data set,
    using the NWS algorithm.

3.  Daily high HI and low HI were computed for each day in the 20 year
    data set.

4.  A data range was defined for each season, providing bounds for
    summer, winter, and spring. Only measurements within the specified
    date range were considered during the remainder of the process.

5.  For the 20 years of summer days, calculate the 90^th^ percentile for
    the high Heat Index. This will identify a "hot" or "peak" summer
    day, while avoiding the record high or "super-peak". Figure 2 shows
    a sample histogram for this information, with a dashed line
    indicating the 90^th^ percentile high for this city. Five summer
    dates were recorded when the high Heat Index reached this value.

![](media/image2.emf){width="5.384662073490814in" height="2.7in"}

Figure : Sample Summer Heat Index Histogram

6.  The previous step was repeated for winter, calculating the 10^th^
    percentile low Heat Index. Five winter dates were recorded when the
    low Heat Index reached this value. Figure 3 shows a sample histogram
    for this case.

![](media/image3.emf){width="5.384660979877515in" height="2.7in"}

Figure : Sample Winter Heat Index Histogram

7.  For spring, it was assumed that the minimum amount of cooling and
    heating occurs when the Heat Index is bound between 68 and 72
    degrees. From the 20 year highs and lows, the day where HI was most
    tightly bound in that range was selected as the representative
    spring day.

8.  In reality, end use load behavior (i.e., duty cycle for heating and
    cooling) lags behind current temperature/HI. Therefore, an adjusted
    HI is calculated using a weighted average of the "current" HI and
    the HI recorded during the previous two hours by the following
    equation:

***HI~adj~ = (0.6 \* HI~t~) + (0.3 \* HI~t-1~) + (0.1 \* HI~t-2~)***

This adjusted HI value is used for all steps forward.

9.  Two days with the same high HI may exhibit widely different 24-hour
    profiles. For example, the ideal summer day for study contains a
    peak Heat Index in the late afternoon (4:00 to 6:00 pm). Also, the
    HI at the end of the day (11:00 pm) will be roughly equal to the HI
    at the beginning of the day (12:00 midnight). However, not all days
    display this behavior, as weather events throughout the day may
    affect the 24-hour HI profile. To account for this, plots are
    created for the 24-hour HI measurements for the five recorded dates
    described in steps 5 (for summer) and 6 (for winter). An example is
    shown in Figure 4:

![](media/image4.emf){width="5.384660979877515in" height="2.7in"}

Figure : Sample 24-Hour Heat Index Profiles

From the plot, it's clear that Day 1 reaches a peak at an atypical time,
and would be a poor choice for a representative weather profile.
However, Day 3 reaches a peak in late afternoon and "completes a cycle",
with the HI at the end of the day similar to the HI at the beginning.
Therefore, Day 3 is a more appropriate choice for a representative
weather profile for this city. The 24-hour HI values are recorded, and
the process is repeated for winter.

10. Steps 1-9 are repeated for every city in the study. These 24-hour
    Heat Index profiles are recorded for all three seasons.

Building Models
---------------

Both residential and commercial models are generated using a collection
of end use load types. For residential buildings, these end uses are
defined by the Residential Building Stock Assessment (RBSA) created by
the Northwest Energy Efficiency Alliance (NEEA). For commercial
buildings, these end uses are defined by the California Commercial
End-Use Survey (CEUS). Each end use is categorized by its dependence on
weather (temperature/humidity) and hour-of-day. Table 1 lists all the
end uses, as well as their application to building types and their
dependencies.

Table : Residential and Commercial End Uses and Categories

  End Use             Residential   Commercial   Weather-Dependent   Time-Dependent
  ------------------- ------------- ------------ ------------------- ----------------
  Resistive Heating   X             X            X                   X
  Heat Pump           X             X            X                   X
  Cooling             X             X            X                   X
  Air Compressor                    X                                X
  Computer            X                                              X
  Cooking                           X                                X
  Dryer               X                                              X
  Entertainment       X                                              X
  Freezer             X                                              X
  Lighting            X             X                                X
  "Miscellaneous"                   X                                X
  Motor                             X                                X
  Office Equipment                  X                                X
  "Other"             X                                              X
  Oven                X                                              X
  Plugs               X                                              X
  Process                           X                                X
  Refrigeration       X             X                                X
  Ventilation                       X                                X
  Washer              X                                              X
  Water Heating       X             X                                X

Weather-dependent end uses (heating and cooling) are assigned an hourly
slope and intercept dependent on the Heat Index for that given hour. All
model parameters are defined on a kW-per-square foot basis. For example,
residential resistive heating, heat pump, and AC load (in kW/sqFt) for
hour 0 and hour 1 are defined as:

*RH(t=0) = Slope~RH~(t=0) x HI + Int~RH~(t=0) RH(t=1) = Slope~RH~(t=1) x
HI + Int~RH~(t=1)*

*HP(t=0) = Slope~HP~(t=0) X HI + Int~HP~(t=0) HP(t=1) = Slope~HP~(t=1) X
HI + Int~HP~(t=1)*

*AC(t=0) = Slope~AC~(t=0) X HI + Int~AC~(t=0) AC(t=1) = Slope~AC~(t=1) X
HI + Int~AC~(t=1)*

Similarly, weather-independent end uses (e.g. lighting, cooking, etc.)
are assigned an hourly kW per square foot, which varies by hour of day.
However, since Heat Index does not impact these end uses, no linear
coefficients are necessary.

With these values defined, the residential and commercial building
models are essentially lookup tables, defining hourly kW/sqFt for each
end use, or the weather-dependent linear coefficients used to generate
kW/sqFt. The following sections describe the process of determining the
values to populate the lookup tables.

### Residential Building Model

As part of their RBSA study, NEEA compiled one year of hourly end-use
measurements from roughly 100 homes in the Northwest. This "8760" data
was delivered to the NERC LMTF team, and was used as the basis for
generating the residential building model. Using the square footage
given for each home, an hourly estimate of kW/sqFt for each
*weather-independent* end-use was calculated as the mean across all
buildings in the study. These hourly kW/sqFt values were entered into
the lookup tables for the residential model.

Limited heating and cooling information in the RBSA 8760 data set
required a different process for determining the hourly kW/sqFt for
*weather-dependent* end uses. To calculate the linear coefficients,
three years of historical SCADA data was pulled for a largely
residential distribution substation in the Vancouver, WA area. The
corresponding Heat Index values for the same time period were also
collected, and the following process was completed:

1.  Based on historical weather information, plot the substation load
    for a mild summer day and a relatively warm summer day. Assume only
    base load is present for the mild day, while base load and AC is
    present for the warmer day. Figure 5 shows the observed Heat Index
    for these two days, and Figure 6 shows the corresponding measured
    load.

![](media/image5.emf){width="3.9313648293963253in" height="2.5in"}

Figure : Heat Index for Mild and Warm Summer Days

![](media/image6.emf){width="3.931365923009624in" height="2.5in"}

Figure : Substation Load for Mild and Warm Summer Days

2.  Using warm summer day feeder load, divide by the total
    *weather-independent* end use kW/sqFt determined from the RBSA data
    for each hour. The mean across 24 hours provides an estimate for the
    residential square footage sourced by the feeder under study.

3.  Determine the hourly difference between the load on the warm day and
    the load on the mild day. This provides an estimate of the hourly kW
    of air conditioning, shown in Figure 7.

![](media/image7.emf){width="3.93in" height="2.5in"}

Figure : Estimated Residential Cooling for Substation

4.  Assuming linearity relative to Heat Index, calculate the slope and
    intercept of AC load per square foot. Repeat for each hour in the
    24-hour period under study. The slope across the full 24 hours is
    shown in Figure 8.

![](media/image8.emf){width="3.9313648293963253in" height="2.5in"}

Figure : Slope of Residential Cooling, Relative to kW/SqFt

5.  Repeat steps 1-4 for heating in winter relative to spring base load
    day. Assume only base load and heating (no AC) in winter.

6.  When hourly *weather-dependent* linear coefficients are determined,
    input them into the lookup table. For the summer building model,
    assume coefficients of 0 for heating. Similarly, assume coefficients
    of 0 for AC in the winter building model. For spring, use both the
    summer AC and winter heating coefficients as calculated.

Note that the analysis software provides a cutoff that will limit
heating and cooling loads to positive values only. If the linear
equation for heating or cooling produces a negative value based on a
given Heat Index, the load for that end use is fixed to zero.

### Commercial Building Model

Similar to the RBSA, the CEUS provides an 8760 hourly end-use dataset
based on metering and simulations for fifteen climate zones across
California. Figure 9 shows a map of these climate zones.

![http://capabilities.itron.com/ceusweb/images/CACZMzp\_ForecastingCZs.bmp](media/image9.png){width="2.074501312335958in"
height="2.4479997812773404in"}

Figure : California Climate Zones Used in CEUS

Information in the CEUS is categorized by commercial building type,
including: college, grocery, health, lodging, large office,
miscellaneous, refrigerated warehouse, restaurant, retail, school, small
office, and warehouse. The CEUS provides the square footage for each
building type for each zone, as well as the square footage of building
area for each end use. For example, the CEUS lists the number of square
feet of restaurants with air conditioning for each climate zone in the
study.

For the purposes of this study, region 6 (Sacramento area) was primarily
used to develop the commercial building models. However, a similar
process can be followed for other regions to further refine the model.
The methodology for developing the model is as follows:

1.  Collect hourly historical weather data for the selected region for
    the time period reported by the CEUS. Compute the corresponding Heat
    Index.

2.  Retrieve historical weather for the summer time period.

3.  Select a building type (e.g., grocery or restaurant) and retrieve
    the hourly end use kW and square footage information for that
    building type for summer.

4.  Calculate the hourly kW/sqFt for each end use.

5.  Generate hourly scatter plots for each recorded end use, including
    both weather-independent and weather-dependent loads. Figures 10 and
    11 show examples of interior lighting load observed at 4:00 am and
    4:00 pm during summer days at grocery stores. Note the values are
    relatively constant across all days, but as expected, lighting load
    is nearly double in the afternoon relative to the early morning.

![](media/image10.emf){width="3.93in" height="2.5in"}

Figure : Grocery Store Lighting Load at 4:00 am

![](media/image11.emf){width="3.93in" height="2.5in"}

Figure : Grocery Store Lighting Load at 4:00 pm

6.  For *weather-independent* loads, calculate the hourly mean of
    kW/sqFt. Insert these values into lookup table for the selected
    building.

7.  For *weather-dependent* loads, perform a linear regression fit to
    determine the coefficients for hourly kW/sqFt. Insert these values
    into the lookup table for the selected building. Figures 12 and 13
    show cooling load for grocery stores at 4:00 am and 4:00 pm
    respectively. Note the higher overall load, as well as greater
    sensitivity to Heat Index (larger slope of the regression fit) for
    the afternoon when compared to the early morning.

![](media/image12.emf){width="3.9313648293963253in" height="2.5in"}

Figure : Grocery Store Cooling Load at 4:00 am

![](media/image13.emf){width="3.931362642169729in" height="2.5in"}

Figure : Grocery Store Cooling Load at 4:00 pm

8.  Repeat steps 3-6 for all building types in the CEUS.

9.  Repeat steps 2-8 for spring and winter time periods.

Feeder composition
------------------

Load composition can vary greatly depending on the number of each
building type supported by a given feeder. For this study, feeder
composition is classified into four categories:

> ***Residential/Suburban (RES):*** Mostly single family residential
> homes, with smaller commercial buildings, including schools, retail,
> restaurants, etc.
>
> ***Commercial (COM):*** Downtown areas primarily made up of large
> office buildings and condominiums
>
> ***Mixed residential and commercial (MIX):*** Areas comprised of
> single family residential homes with small offices and shopping
> centers.
>
> ***Rural/agricultural (RAG):*** Rural areas, with farms, small
> restaurants, and retail.

For each city in the study, a set of city/feeder pairs are created,
combining the city with the each of the four feeder types. For example,
Boston is assigned four city/feeder pairs: BOS\_RES, BOS\_COM, BOS\_MIX,
and BOX\_RAG. Each pair is provided a feeder composition, listing an
estimate of the number of square foot of each commercial building type
(as provided by CEUS), as well as a single family residential. Table 2
shows the default feeder composition initially applied to all cities,
though these values are user-definable per city/feeder pair.

Table : Default Feeder Composition

  Building Type            RES Square Ft.   COM Square Ft.   MIX Square Ft.   RAG Square Ft.
  ------------------------ ---------------- ---------------- ---------------- ----------------
  Residential Home         6000000          0                3000000          600000
  College                  0                0                0                0
  Grocery                  90000            90000            135000           45000
  Health                   40000            40000            60000            0
  Large Office             0                4200000          0                0
  Lodging                  0                1000000          300000           50000
  Miscellaneous            10000            10000            20000            0
  Refrigerated Warehouse   0                0                100000           0
  Restaurant               100000           125000           200000           25000
  Retail                   600000           600000           800000           60000
  School                   400000           0                400000           100000
  Small Office             0                100000           600000           0
  Warehouse                150000           0                400000           500000

Electrification
---------------

To determine end use load shapes, electrification percentages for
heating, cooling, water heating, and cooking are required for each
building type, both residential and commercial. Individual
electrification values are difficult to acquire for each city, so
default percentages are estimated using the Residential Energy
Consumption Survey (RECS) and Commercial Energy Consumption Survey
(CBECS), provided by the U.S. Energy Information Administration (EIA).
These sample surveys use the U.S. census regions and divisions (Figure
14) and provide estimates of total square footage for each building type
within a region. They also list the square footage serviced by electric
heating, cooling, water heating, and cooking. From this information,
electrification percentages are estimated for each of these four end
uses on a per-region basis.

![U.S. Census Regions and Divisions
Map](media/image14.png){width="3.7160640857392826in"
height="2.976000656167979in"}

Figure : U.S. Census Regions Used for RECS and CBECS

Based on the location (region) of each city, a lookup table is created
with these electrification percentages for all city/feeder pairs. The
values in Tables 3 and 4 are defaults, and can be user-defined if more
accurate information is acquired for a given city.

Table : Default Residential Electrification Percentages

  Region               Heat Pump   Other Electric Heat   Cooling   Water Heating   Cooking
  -------------------- ----------- --------------------- --------- --------------- ---------
  New England          3%          10%                   75%       36%             59%
  Middle Atlantic      3%          11%                   88%       31%             43%
  East North Central   3%          17%                   92%       34%             57%
  West North Central   4%          18%                   92%       40%             75%
  South Atlantic       24%         32%                   95%       72%             78%
  East South Central   24%         39%                   93%       76%             75%
  West South Central   8%          45%                   95%       58%             71%
  Mountain             8%          19%                   78%       31%             67%
  Pacific              7%          25%                   66%       32%             53%

Table : Default Commercial Electrification Percentages

  Region               Heat Pump   Other Electric Heat   Cooling   Water Heating   Cooking
  -------------------- ----------- --------------------- --------- --------------- ---------
  New England          9%          2%                    77%       45%             27%
  Middle Atlantic      9%          6%                    89%       41%             31%
  East North Central   5%          8%                    90%       39%             33%
  West North Central   7%          14%                   87%       49%             32%
  South Atlantic       27%         20%                   91%       62%             30%
  East South Central   17%         23%                   88%       59%             31%
  West South Central   10%         30%                   81%       47%             25%
  Mountain             10%         13%                   84%       40%             31%
  Pacific              15%         21%                   88%       51%             22%

Software data flow
------------------

Once all metadata is compiled, the algorithm can be run to compute load
composition. This process is divided into two main stages: calculating
load shapes and applying the rules of association.

### Calculating Load Shapes

The process for calculating load shapes is as follows:

1.  Select a city/feeder pair.

2.  Retrieve the 24 hour Heat Index profile for the given city for
    summer. A sample plot is given in Figure 15.

![](media/image15.emf){width="3.931362642169729in" height="2.5in"}

Figure 15. Heat Index Profile for Portland, Summer

3.  For each building type, retrieve electrification percentages for
    heating, cooling, water heating, and cooking.

4.  Cycle through all the end uses for each building type, referencing
    the lookup table for hourly building model coefficients. For heating
    and cooling, this will be a slope and intercept. For other end uses,
    this will be a single value for a given hour.

5.  Apply the 24 hour Heat Index profile to the *weather-dependent* end
    uses. This will create a 24-hour kW/sqFt value for each end use, per
    building.

6.  Apply electrification percentages and feeder composition to each end
    use. This creates the final load shapes, per end use for each
    building type. As an example, Figure 16 shows a plot of three end
    use load shapes for restaurants in a Portland Mixed feeder during
    summer. Note that refrigeration is relatively constant throughout
    the day, cooking is highest during business hours, and cooling
    reaches a peak at a time corresponding to the peak Heat Index for
    the day.

![](media/image16.emf){width="3.93in" height="2.5in"}

Figure : Sample End Use Load Shapes

7.  Repeat steps 2-6 for winter and spring.

8.  Repeat steps 1-7 for all city/feeder pairs.

For the purposes of load composition, only end use load shapes are
calculated, and remain separated by building type. However, for
confirmation and analysis, total end use load shapes are calculated and
plotted, as required. Figures 17, 18, and 19 show total load shapes for
Portland RES, COM, and MIX feeders, respectively, under all three
seasonal conditions.

![](media/image17.emf){width="3.931362642169729in" height="2.5in"}

Figure : Total Load Shapes, Portland RES Feeder

![](media/image18.emf){width="3.93in" height="2.5in"}

Figure : Total Load Shapes, Portland COM Feeder

![](media/image19.emf){width="3.931362642169729in" height="2.5in"}

Figure : Total Load Shapes, Portland MIX Feeder

### Applying Rules of Association

The rules of association provide a mapping of end use load shapes to the
seven load types by defining a fraction of each end use associated with
each type. For example, residential air conditioning is defined as 80%
Motor D, 10% Motor B, and 10% Motor C. Four individual tables have been
created based on building types: residential, lodging/condominium,
large/downtown office, and general commercial. To calculate the total
load composition factors:

1.  For each building, retrieve the corresponding rules of association
    table.

2.  Cycle through end uses, multiplying load shapes by percentages
    referenced in the rules of association. Calculate the sum of all kW
    for each load type.

3.  Calculate the load composition as a percentage of the total. Figures
    20, 21, and 22 show the 24 load composition for Portland RES, COM,
    and MIX feeders, respectively.

![](media/image20.emf){width="3.931362642169729in" height="2.5in"}

Figure : Load Composition for Portland RES Feeder

![](media/image21.emf){width="3.9313648293963253in" height="2.5in"}

Figure : Load Composition for Portland COM Feeder

![](media/image22.emf){width="3.93in" height="2.5in"}

Figure : Load Composition for Portland MIX Feeder

4.  Repeat the process for each city/feeder pair, and for each season.

Conclusions and Next Steps
--------------------------

The process undertaken by NERC LMTF has yielded positive results,
generally in agreement with past efforts for load modeling and
composition. Load composition values align with common sense
expectations and trends are consistent across regions. However, much
work remains to help minimize assumptions throughout the process, tune
building models, and refine results. As of this writing, numerous
metering studies are underway to increase the breadth of residential and
commercial datasets, allowing for more accurate and modernized building
models. Regional entities are increasing their involvement, which will
improve visibility and refinement of such factors as electrification and
feeder composition.

Appendix: Sample Results
------------------------

Planning studies are primarily concerned with load composition at peak
or light load times. For the initial data set, the periods of interest
are defined as:

-   Summer at 4:00 pm

-   Winter at 8:00 am

-   Spring at 3:00 am

Results for a particular time slice can be visualized with pie charts.
Samples of these pie charts are provided below. **Note: Pie charts are
available for all city/feeder pairs, and can be added if necessary.**

### Boston

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829271332960.png](media/image23.png){width="3.9984087926509186in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829271470580.png](media/image24.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829271990900.png](media/image25.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829272314320.png](media/image26.png){width="3.9984087926509186in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829272469280.png](media/image27.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829272618830.png](media/image28.png){width="3.998413167104112in"
height="3.0in"}

### Miami

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829273421420.png](media/image29.png){width="3.99in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829273595530.png](media/image30.png){width="3.99in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829273653630.png](media/image31.png){width="3.99in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829274123370.png](media/image32.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829274414520.png](media/image33.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829274225320.png](media/image34.png){width="4.0in"
height="3.0in"}

### Phoenix

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829275904270.png](media/image35.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829275968760.png](media/image36.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829276009820.png](media/image37.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829276443170.png](media/image38.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829276490200.png](media/image39.png){width="4.0in"
height="3.0in"}

![C:\\Users\\Tony\\AppData\\Local\\Temp\\ConnectorClipboard6316831190965338276\\image15829276547250.png](media/image40.png){width="4.0in"
height="3.0in"}
