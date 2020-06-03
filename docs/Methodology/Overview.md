**Save for cover image**

**Load Composition Analysis in Support of the **

**NERC Load Modeling Task Force 2019-2020 Field Test of the **

**Composite Load Model **

Authors:

Anthony Faris and Dmitry Kosterev, Bonneville Power Administration

Joseph H. Eto, Lawrence Berkeley National Laboratory

Dave Chassin, Stanford Linear Accelerator Center

Ernest Orlando Lawrence Berkeley National Laboratory

1 Cyclotron Road, MS 90R4000

Berkeley CA 94720-8136

Month 2020

The work described in this study was funded by the U.S. Department of
Energy's Office of Electricity, under Lawrence Berkeley National
Laboratory Contract No. DE-AC02-05CH11231.

Acknowledgements {#acknowledgements .Heading}
================

The work described in this study was funded by the U.S. Department of
Energy's Office of Electricity, under Lawrence Berkeley National
Laboratory Contract No. DE-AC02-05CH11231.

The authors thank the following colleagues for their input on study
approach or review of a draft of this report, or both:

All opinions, errors and omissions remain the responsibility of the
authors. All reference URLs were accurate as of the date of publication.

Table of Contents {#table-of-contents .Heading}
=================

[Acknowledgements i](#acknowledgements)

[Table of Contents ii](#_Toc40779597)

[Table of Figures iii](#table-of-figures)

[List of Tables iii](#list-of-tables)

[Synopsis iv](#synopsis)

[1. The Role of Load Composition Analysis in Supporting the Development
of Composite Load Models 1](#introduction)

[2. Overview of the DOE/BPA Load Composition Analysis Process
5](#overview-of-the-doebpa-load-composition-analysis-process)

[2.1 Step 1. Compilation and analysis of publicly available data
7](#step-1.-compilation-and-analysis-of-publicly-available-data)

[2.2 Step 2. Compilation and application of region-specific information
13](#step-2.-compilation-and-application-of-region-specific-information)

[2.3 Step 3. Mapping end uses to the composite load model
18](#step-3.-mapping-end-uses-to-the-composite-load-model)

[2.4 Step 4. Developing region-specific feeder models
20](#step-4.-developing-region-specific-feeder-models)

[3. Representative Outcomes from the Load Composition Analysis
23](#representative-outcomes-from-the-load-composition-analysis)

[References 26](#references)

Table of Figures {#table-of-figures .Heading}
================

[Figure 1. Load Composition Analysis Process 6](#_Ref39828542)

[Figure 2. Substation Loads Used to Estimate Residential Cooling Loads
(left); Estimated Residential Cooling Load (right) 11](#_Ref39828642)

[Figure 3. Cooling Load Versus Heat Index for Grocery at 4 AM (left);
Cooling Load Versus Heat Index for Grocery at 4 PM (right)
12](#_Ref39828654)

[Figure 4. North American Weather Cities Used in Load Composition
Analysis 14](#_Toc41479608)

[Figure 5. Identification of Summer Peak Day -- example (left);
Identification of Winter Peak Day -- example (right) 15](#_Ref39828693)

[Figure 6. U.S. Census Regions 16](#_Toc41479610)

[Figure 7. Summer Peak Day, Atlanta -- RES Feeder (left); Summer Peak
Day, Atlanta -- MIX Feeder (right) 23](#_Ref39829149)

[Figure 8. Summer Peak Hour (4 pm), Atlanta -- RES Feeder (left); Summer
Peak Hour (4 pm), Atlanta -- MIX Feeder (right) 23](#_Ref39829571)

[Figure 9. MIX Feeder, Toronto, Summer Peak Day (top left); MIX Feeder,
Toronto, Winter Peak Day (top right); MIX Feeder, Toronto, Spring Light
Load Day (bottom) 24](#_Ref39829801)

[Figure 14. MIX Feeder, Toronto, Summer Peak Hour (4 pm) (top left); MIX
Feeder, Toronto, Winter Peak Hour (8 am) (top right); MIX Feeder,
Toronto, Spring Light Load Hour (3 am) (bottom) 25](#_Toc41479614)

List of Tables {#list-of-tables .Heading}
==============

[Table 1. Building Types and End Uses 7](#_Ref39828571)

[Table 2. Residential End-Use Metered Data from the Residential Stock
Building Assessment 8](#_Toc41479616)

[Table 3. Commercial Sector End-Use Load Shaped Data from the California
Commercial End-Use Survey 9](#_Toc41479617)

[Table 4. Electrification Factors -- U.S. Residential 16](#_Ref39828892)

[Table 5. Electrification Factors -- U.S. Commercial 17](#_Ref39828906)

[Table 6. Electrification Factors -- Canadian 17](#_Ref39828920)

[Table 7. Rules of Association for All Commercial Buildings Except Large
Office and Lodging 19](#_Ref39828934)

[Table 8. Rules of Association for Large Office 19](#_Toc41479622)

[Table 9. Rules of Association for Lodging 19](#_Toc41479623)

[Table 10. Rules of Association for Residential Buildings
19](#_Ref39828942)

[Table 11. Composition of Suburban or RES Feeder 20](#_Ref39828959)

[Table 12. Composition of Downtown Urban or COM Feeder
21](#_Ref39828970)

[Table 13. Composition of Hybrid or MIX Feeder 21](#_Ref39828981)

[Table 14. Composition of Rural or RUR Feeder 22](#_Ref39828988)

Synopsis  {#synopsis .Heading}
=========

In 2015, NERC's reliability standards were revised to require the use of
dynamic load models in transmission planning studies.[^1] To comply with
the standards, planners must use load models that explicitly represent
the dynamic behavior of the different constituents of load at each load
bus within their transmission planning models. The most important of
these constituents are motor-driven and power electronics-based loads.
Collectively, these representations are known as composite load
models.[^2]

In anticipation of the compliance date for the new standards, NERC's
Load Modeling Task Force (LMTF), in 2019, initiated a field test of
composite load models involving the regional reliability planning
entities. In support of the field test, DOE and BPA researchers
developed region-specific composite load models that could be assigned
to each non-industrial load bus in the planning models for each of the
North American interconnections.[^3] Separate models were developed for
each hour of a summer peak day, a winter peak day, and a spring
light-load day.

This report is the technical documentation for the load composition
analysis that was conducted to develop these non-industrial composite
load models.

Introduction
============

Transmission planning studies are conducted routinely to ensure that the
bulk electric power system can be operated reliably under anticipated
conditions. A special emphasis of these studies is to ensure continued
operation following unexpected events, such as the unplanned loss of a
large generator or transmission line.

Following the 1996 blackouts on the west coast, transmission planners
found, among other things, that the models they had used to represent
the behavior of loads in their studies were not accurate \[Kosterev, et
al. 1999\]. They found, specifically, that their models did not fully
capture the dynamic behavior of loads under stressed system conditions.
This finding led transmission planners in the Western Interconnection to
begin developing new load models that focused on the dynamic behavior of
motors.

The need for improvements in load modeling, again, became an issue for
transmission planners in the 2000's when it was observed that, contrary
to expectations, system voltages sometimes did not recovery
instantaneously following normally cleared faults on the transmission
system. Upon investigation, they determined that some faults were
causing large numbers of single-phase induction motors used in
residential central air conditioners to stall and continue to depress
system voltages locally until they shut-down. Although the phenomena had
been documented in the past (see, for Willams, et al. 1992), in the
2000's, there was increased concern that "fault induced delayed voltage
recovery" or FIDVR might lead to a cascading voltage collapse.

Industry's concern over this possibility led the US Department of Energy
(DOE) to support a national initiative on the study of FIDVR. DOE and
NERC held several workshops at which technical findings were presented
and discussed.[^4]

In conjunction with these workshops and based on studies that DOE had
sponsored, the transmission planners in the Western Interconnection
developed a new approach for modeling the dynamic behavior loads in
their studies, called the composite load model. The distinguishing
feature of the composite load model is the explicit representation of
the dynamic behavior of the different constituents of load at each load
bus within their transmission planning models. The most important of
these constituents are motor-driven and power electronics-based loads
\[NERC 2016\].

The Western Electric Coordinating Corporation (WECC), which is the
regional reliability planning entity, began phased adoption of the
composite load model in 2011. The use of the composite load model is now
an established practice for planners in the Western interconnection.
WECC currently maintains libraries of composite load models that have
been developed for each load bus within the interconnection. These
libraries are drawn upon routinely by transmission planners in the
Western interconnection.

In 2015, NERC's reliability standards were revised to require the use of
the dynamic load models (i.e., the composite load model) in transmission
planning studies.[^5] The use of the composite load models is a
comparatively new practice for the majority of planners in the Eastern
and Texas interconnections. Currently, there are no interconnection-wide
libraries of composite load models currently available for these
planners to use.

In anticipation of the compliance date for the new standards, NERC's
Load Modeling Task Force (LMTF), in 2019, initiated a field test of
composite load models involving the regional reliability planning
entities in the Eastern and Texas interconnections. In support of the
field test, DOE and BPA researchers developed region-specific composite
load models that could be assigned to each non-industrial load bus in
the planning models for the two interconnections.[^6] Separate models
were developed for each hour of a summer peak day, a winter peak day,
and a spring light-load day.

This report is the technical documentation for the load composition
analysis that was conducted to develop these non-industrial composite
load models. It is an application of methods that have been outlined
previously by NERC \[NERC 2017\].

The report is organized in three sections following this introduction.
In section 2, we provide additional background on the composite load
models and the analysis issues that must be addressed in developing
these models for Eastern and Texas interconnections. In section 3, we
describe and provide documentation on each of the four main steps
involved in the load composition analysis process that was used to
develop composite load models for the field test. In section 4, we
briefly review examples of the output from the load composition
analysis.

The Role of Load Composition Analysis in Supporting the Development of Composite Load Models 
=============================================================================================

Transmission planning studies are conducted using positive-sequence
models that simulate the dynamic behavior of the transmission system
under stressed conditions. The positive-sequence models are, in turn,
supported by (or comprised of) a large number of individual models that
represent the dynamic behaviors of both each generator and each load.
Each load is represented through use of a composite load model.

A composite load model is a portfolio comprised of seven distinct types
of load behaviors. A separate composite load model is specified for each
load bus (or feeder) within the transmission system at which load is
withdrawn (or served). Developing composite load models, therefore,
involves specifying the relative proportions of each the seven different
types of load behaviors, so that collectively they are reflective of all
of loads served at each feeder.

For feeders at which a single (or group of similar) industrial
customer(s) is served, there is already a large library of
industry-specific composite load models, which was developed for
planners in the Western interconnection. These can be readily
transferred and used to represent industrial feeders in the Eastern and
Texas interconnections.

However, the vast majority of feeders in all interconnections serve
non-industrial loads. Developing composite load models for them requires
new methods because these loads can differ considerably from those in
the Western interconnection. One important difference is climate, which
affects the magnitude of weather-sensitive loads, such as air
conditioning (or space cooling) and space heating. Another important
difference is electrification, which affects the magnitude of space
heating, water heating, and cooking loads.

Despite these differences, there are also important similarities among
non-industrial loads in all of the interconnections that facilitate the
development of composite load models. First, they are comprised mainly
of either residential or commercial buildings. Second, for any given
type of residential or commercial building, there are many similarities
in the systems each relies on to provide space cooling, space heating,
water heating, cooking, lighting, refrigeration, etc.

Both these differences and similarities in residential and commercial
buildings' uses of electricity have been studied systematically. In
particular, forty years of demand-side management planning by utilities
has led to the availability of a great deal of information on the uses
of electricity in residential- and commercial-sectors. Much is now known
about the variability (or sensitivity) of end-use loads, such as space
cooling and space heating, on an hourly basis under different climatic
conditions. Similarly, much is also known about the degree or extent of
electrification of certain end uses (space heating, water heating, and
cooking) in different regions of North America.

We draw from this base of information in order to develop composite load
models for non-industrial feeders across North America through a process
we term "load composition analysis."

Overview of the DOE/BPA Load Composition Analysis Process
=========================================================

The objective of DOE/BPA load composition analysis is to develop
composite load models that are reflective of composition of loads in
each of the regions of the Eastern and Texas interconnections. Separate
models are developed for each hour of a summer peak day, a winter peak
day, and a spring light load day. In the end, these models are developed
for four types of feeders for each of 96 weather cities across North
America.

The load composition analysis process consists of four steps. See Figure
1.

*Step 1* involves the compilation and analysis of publicly available
information on the uses of (or end uses for) electricity in the
residential and commercial sector.

*Step 2* involves compilation and application of region-specific
information on weather as well as on the discretionary uses of
electricity (i.e., for space heating, water heating, and cooking) to
develop region-specific hourly loads for each building and end use.

*Step 3* involves mapping the region-specific hourly loads, by building
type and end use, to the seven composite load model load types.

*Step 4* involves the preparation of representative feeder models for
each target region.

The basic unit of analysis is a building type and the electric end uses
within that building type. For the residential sector, a single
representative building type comprised of 13 end uses was used. For the
commercial sector, 11 representative building types each comprised of 12
end uses were used. See Table 1.

![](media/image1.png){width="9.0in" height="5.2972222222222225in"}

[]{#_Ref39828542 .anchor}Figure 1. Load Composition Analysis Process

[]{#_Ref39828571 .anchor}Table . Building Types and End Uses

+------------------+------------------------+-----------------------+
|                  | **Building Types**     | **End Uses**          |
+==================+========================+=======================+
| **Residential ** | Single Family          | Heating -- resistance |
|                  |                        |                       |
|                  |                        | Heating -- heat pump  |
|                  |                        |                       |
|                  |                        | Cooling               |
|                  |                        |                       |
|                  |                        | Hot Water             |
|                  |                        |                       |
|                  |                        | Oven                  |
|                  |                        |                       |
|                  |                        | Refrigeration         |
|                  |                        |                       |
|                  |                        | Freezer               |
|                  |                        |                       |
|                  |                        | Lighting              |
|                  |                        |                       |
|                  |                        | Entertainment         |
|                  |                        |                       |
|                  |                        | Computer              |
|                  |                        |                       |
|                  |                        | Washer                |
|                  |                        |                       |
|                  |                        | Dryer                 |
|                  |                        |                       |
|                  |                        | Plugs                 |
|                  |                        |                       |
|                  |                        | Other                 |
+------------------+------------------------+-----------------------+
| **Commercial **  | Large Office           | Heating               |
|                  |                        |                       |
|                  | Small Office           | Cooling               |
|                  |                        |                       |
|                  | Retail                 | Ventilation           |
|                  |                        |                       |
|                  | Grocery                | Water Heating         |
|                  |                        |                       |
|                  | Restaurant             | Cooking               |
|                  |                        |                       |
|                  | Lodging                | Refrigeration         |
|                  |                        |                       |
|                  | Health                 | Exterior Lighting     |
|                  |                        |                       |
|                  | School                 | Interior Lighting     |
|                  |                        |                       |
|                  | Warehouse              | Office Equipment      |
|                  |                        |                       |
|                  | Refrigerated Warehouse | Miscellaneous         |
|                  |                        |                       |
|                  | Miscellaneous          | Process               |
|                  |                        |                       |
|                  |                        | Motors                |
|                  |                        |                       |
|                  |                        | Air Compressor        |
+------------------+------------------------+-----------------------+

Step 1. Compilation and analysis of publicly available data
-----------------------------------------------------------

The objective of step 1 is to process and transform hourly metered
information collected in one region of North America into a form that
can be re-expressed or extrapolated to be representative of conditions
in other regions of North America.

The methods we employ make several assumptions: First, we assume that
size differences among buildings of a given type can be accounted for by
first normalizing end use load information collected from a group of
building in one region by floor area and then later by multiplying the
normalized values by the floor area of a different group of like
buildings in another region (Step 1a, below). Second, we assume that
non-weather sensitive loads are common to all buildings of a given type
across all regions (Step 1b, below). Third, we assume that weather
sensitive loads recorded in one region can be used to project weather
sensitive loads in another region through the use of statistical
correlations, which we call hourly weather sensitivity factors, that
express hourly loads as a function of hourly measures of weather (Steps
1c, below).

The outputs from step 1 are, for each building type, a series of
normalized, hourly non-weather sensitive loads and hourly weather
sensitivity factors.

The load composition analysis process is based on end-use load
information that have been collected for samples of hourly metered
residential and commercial buildings.

The information for residential buildings was collected by the North
Energy Efficiency Alliance through the Residential Building Stock
Assessment (RBSA) project in 2013-4 \[Ecotope 2014\]. The RBSA project
characterized the existing residential building stock in the Northwest
region based on data from a representative sample of homes. Within the
RBSA project, the RBSA Metering Study was a whole-house metering study
covering most energy end uses in 101 homes in the Pacific Northwest. The
information from the RBSA project was augmented by historic SCADA
information collected by BPA for a predominantly residential feeder near
Vancouver, WA from 2015-7.

The information for commercial buildings was developed by the California
Energy Commission through the California Commercial End-Use Survey
(CEUS) project in 2002 \[Itron 2006\]. CEUS was a comprehensive study of
commercial sector energy use, primarily designed to support the state's
energy demand forecasting activities. A stratified random sample of
2,800 commercial facilities was targeted from the service areas of
Pacific Gas & Electric, San Diego Gas and Electric, Southern California
Edison, Southern California Gas Company and the Sacramento Municipal
Utility District. Simulated energy use for each survey participant was
calibrated to actual historical energy consumption from utility billing
records. The software created end-use load profiles and electricity and
natural gas consumption estimates by end-use for user-defined commercial
market segments.

Tables 2 and 3 show, for each end use, the number and total floor area
of residential homes and the total floor area of the commercial
buildings whose metered or calibrated load shape information was used in
the load composition analysis, respectively.

[]{#_Toc41479616 .anchor}Table . Residential End-Use Metered Data from
the Residential Stock Building Assessment

  **End Use**     **Homes Metered**   **Total Square Footage Metered**
  --------------- ------------------- ----------------------------------
  Computer        73                  158,351
  Dryer           85                  180,009
  Entertainment   83                  178,212
  Freezer         39                  801,38
  Hot Water       47                  917,12
  Lighting        86                  188,275
  Other           33                  77,155
  Oven            56                  111,877
  Plugs           90                  195,081
  Refrigerator    89                  193,885
  Washer          83                  184,895

[]{#_Toc41479617 .anchor}Table . Commercial Sector End-Use Load Shaped
Data from the California Commercial End-Use Survey

  **End Use**         **College**   **Grocery**   **Health**   **Large Office**   **Lodging**   **Misc.**    **Refrig. Warehouse**   **Restaurant**   **Retail**   **School**   **Small Office**   **Warehouse**   **Total**
  ------------------- ------------- ------------- ------------ ------------------ ------------- ------------ ----------------------- ---------------- ------------ ------------ ------------------ --------------- -------------
  Heating             4,871         1,511         9,038        9,374              36,341        14,093       335                     1,148            15,169       16,641       6,408              1,703           **116,632**
  Cooling             11,185        4,307         10,065       9,392              40,383        31,561       336                     5,375            35,346       19,174       15,105             1,891           **184,120**
  Ventilation         11,732        4,585         10,069       9,392              40,573        33,871       339                     5,375            36,247       19,678       15,105             1,891           **188,857**
  Water Heating       3,277         2,205         367          1,907              16,638        19,437       2,722                   484              34,102       13,269       13,322             9,514           **117,244**
  Cooking             11,497        5,313         11,169       9,691              42,848        35,657       2,722                   6,132            33,446       20,005       15,611             4,136           **198,227**
  Refrigeration       11,968        5,582         11,169       9,691              42,848        37,968       2,722                   6,132            39,535       20,005       18,175             7,941           **213,736**
  Exterior Lighting   11,968        4,032         10,468       9,691              41,652        37,175       2,722                   2,455            39,718       20,005       15,810             7,941           **203,637**
  Interior Lighting   11,968        5,582         11,169       9,691              42,848        39,342       2,722                   6,132            44,597       20,005       18,469             15,307          **227,832**
  Office Equipment    11,968        5,582         11,169       8,648              42,848        38,989       2,722                   6,132            44,066       20,005       18,449             14,432          **225,010**
  Miscellaneous       10,402        5,582         10,468       9,691              40,017        39,114       2,635                   5,877            38,962       19,649       16,904             14,848          **214,149**
  Process             0             0             731          0                  375           2,288        0                       0                3,373        0            516                0               **7,283**
  Motors              9,786         3,604         6,350        5,991              37,604        24,461       2,722                   1,950            15,442       10,327       4,951              2,588           **125,776**
  Air Compressors     10,908        0             7,086        3,232              14,832        13,282       416                     0                10,597       3,274        2,586              4,058           **70,271**
  **Segment Total**   **11,968**    **5,582**     **11,169**   **9,691**          **42,848**    **39,342**   **2,722**               **6,132**        **44,597**   **20,005**   **18,469**         **15,307**      **227,832**

*Step 1a. Normalization of load information using building floor area*

For each building type, all hourly load information was first normalized
by the floor area of the buildings from which the loads were collected.
This was accomplished by summing the loads, separately for each end use
and for each hour, and then dividing each by the total floor area of the
buildings from which loads had been metered.

*Step 1b. Development of non-weather sensitive hourly loads by season*

Non-weather sensitive load shapes were developed by averaging,
separately for each non-weather sensitive end use, the normalized loads
for each hour across all weekdays in each season (also excluding
holidays).

For the residential building analysis, summer hourly load shapes were
developed from loads metered during the months of June through
September. Winter hourly loads were developed from loads metered during
the months of December through February. Spring hourly loads were
developed from loads metered during the months of April and May.

For the commercial building analysis, summer hourly load shapes were
developed from loads metered during the months of July through
September. Winter hourly loads were developed from loads metered during
the months of December through February. Spring hourly loads were
developed from loads metered during the months of March through May.

*Step 1c. Development of hourly weather sensitivity factors*

Hourly weather sensitivity factors were developed by correlating
statistically hourly weather sensitive loads to hourly measures of
weather. A separate sensitivity factor was developed for each hour of
the day. Hourly cooling and heating sensitivity factors were developed
using hourly load and weather information from weekdays (excluding
holidays) during the same summer and winter months used to develop
non-weather sensitive loads.

The hourly measure of weather is based on a well-established metric
called the heat index \[National Weather Service 20202\]. It is a linear
combination of both dry bulb temperature and humidity.

*Equation 1*

**HI = -42.379 + 2.04901523\*T + 10.14333127\*RH - .22475541\*T\*RH -
.00683783\*T\*T - .05481717\*RH\*RH + .00122874\*T\*T\*RH +
.00085282\*T\*RH\*RH - .00000199\*T\*T\*RH\*RH**

T -- temperature (F)

RH -- relative humidity (%)

To account for thermal lag effects, a weighted version of heat index is
used in the past two hourly values of index are combined with the
current hourly value.

*Equation 2 *

***HI~adj~ = (0.6 \* HI~t~) + (0.3 \* HI~t-1~) + (0.1 \* HI~t-2~)***

The correlation between the hourly weighted heat index and hourly
cooling or heating load is estimated using a simple linear regression.
The regression yields both a constant (or intercept term) and
coefficient that depends on the hourly weighted heat index value. The
constant and coefficient, taken together, are the hourly weather
sensitivity factor.

Hourly weather sensitivity factors for residential cooling and heating
were developed using SCADA data collected by BPA from a predominantly
residential feeder in Vancouver, WA in a four-step process. First,
hourly SCADA data from a time of the year when little or no cooling or
heating was expected were used to develop an hourly non-weather
sensitive feeder load (a "mild day" load). Second, this load was
subtracted from hourly feeder loads on selected days during the summer
and winter months when cooling and heating, respectively, were expected.
See Figure 2 for an illustration of the steps involved in applying this
process to estimate summer cooling loads. Third, the resultant hourly
summer cooling and winter heating feeder loads were normalized by an
estimate of the total floor area of residences in the feeder.[^7]
Fourth, the hourly weighted heat index on these summer and winter days
were regressed against the normalized summer cooling and winter heating
loads, respectively.

  -------------------------------------------------------------------- --------------------------------------------------------------------
  ![](media/image2.emf){width="3.1in" height="1.9713221784776902in"}   ![](media/image3.emf){width="3.1in" height="1.9720100612423448in"}
  -------------------------------------------------------------------- --------------------------------------------------------------------

[]{#_Ref39828642 .anchor}Figure . Substation Loads Used to Estimate
Residential Cooling Loads (left); Estimated Residential Cooling Load
(right)

The hourly weather sensitivity factors for commercial building cooling
and heating were developed by applying the same regression-based
approach to the aggregated and normalized CEUS commercial buildings by
type. The regressions relied on the hourly weighted heat indices and the
hourly weekday loads drawn from the same months used to develop the
non-weather sensitive loads for these building types (again excluding
holidays).

Figure 3 present examples of this analysis process for cooling loads in
grocery stores for two different hours (4 AM and 4 PM). Each figure
displays the hourly normalized cooling loads that were measured along
with the regression line that best correlates these loads with the
weighted hourly heat index values.

  -------------------------------------------------------------------- -------------------------------------------------------------------
  ![](media/image4.emf){width="3.1in" height="1.9713232720909886in"}   ![](media/image5.emf){width="3.1in" height="1.971324365704287in"}
  -------------------------------------------------------------------- -------------------------------------------------------------------

[]{#_Ref39828654 .anchor}Figure . Cooling Load Versus Heat Index for
Grocery at 4 AM (left); Cooling Load Versus Heat Index for Grocery at 4
PM (right)

Step 2. Compilation and application of region-specific information
------------------------------------------------------------------

The outputs from step 1 are, for each building type, hourly weather
sensitivity factors for both cooling and heating, and seasonal,
normalized, hourly non-weather sensitive loads. Step 2 applies
region-specific information on hourly weather and on the discretionary
use of electricity for space cooling, space heating, water heating, and
cooking to adjust these outputs to develop region-specific hourly loads
for all buildings and end uses.

Step 2 involves identifying weather stations and developing
representative hourly weather information for them for each region, and
then applying this information to the weather sensitivity factors to
estimate hourly weather-sensitive loads (step 2a). It then involves
developing information on extent to which electricity is used for space
cooling, space heating, water heating, and cooking in each region, and
then using this information adjust the hourly load shapes for each of
these end uses (step 2b).

The outputs from step 2 are, for each building type and for these end
uses, alone, a region-specific, normalized, set of hourly loads for a
summer peak day, winter peak day, and spring light load day. Step 2 does
not involve adjustments to any of the remaining end uses (i.e., those
other than space cooling, space heating, water heating, and cooking).
These are simply passed directly from step 1 on to step 3.

*Step 2a. Estimation of region-specific hourly weather-sensitive loads*

The estimation of region-specific hourly weather-sensitive loads
involves three intermediate steps. First, representative weather cities
were identified by transmission planners in each of the regions. Second,
20 years of historic weather information was reviewed and 24-hour heat
index profiles were developed to be representative of summer peak day,
winter peak day, and spring light load day conditions. Third the hourly
profiles were applied to the weather sensitivity factors to produce
hourly weather-sensitive loads for both cooling and heating.

Leadership of the NERC LMTF met with representatives of each of the NERC
regional reliability planning entities to identify cities (airports)
whose weather would be best reflective of conditions across each region.
A total of 96 weather cities were identified through this process. See
Figure 4.

![](media/image6.png){width="6.5in" height="4.445833333333334in"}

[]{#_Toc41479608 .anchor}Figure . North American Weather Cities Used in
Load Composition Analysis

For each weather city, 20 years of historic hourly weather information
(from 1999 through 2018) was assembled from the National Centers for
Environmental Information and Government of Canada Historical Climate
Data \[NCEI 2020, Government of Canada 2020\] and the heat index was
calculated for each hour. The identification of hourly weather for a
representative summary peak, winter peak, and spring light load day is
based on selecting the day from this historical record based on the
following criteria.

For the summer peak day, the criteria were that the day had to be drawn
from the months of July and August and that the highest daily hourly
heat index value had to correspond to the 90^th^ percentile across all
highest daily hourly heat index values recorded over the 20-year record.
See Figure 5.

For the winter peak day, the criteria were that the day had to be drawn
from the period between December 15^th^ and February 15^th^ and that the
lowest daily hourly heat index value had to correspond to the 90^th^
percentile across all lowest daily hourly heat index values recorded
over the 20-year record. See Figure 5.

For the spring light load day, the criteria were that the day had to be
drawn from the months of April and May and that the highest daily hourly
heat index value had to be between 68 and 72 degrees.

  -------------------------------------------------------------------- --------------------------------------------------------------------
  ![](media/image7.emf){width="3.1in" height="1.8172659667541557in"}   ![](media/image8.emf){width="3.1in" height="1.8175371828521434in"}
  -------------------------------------------------------------------- --------------------------------------------------------------------

[]{#_Ref39828693 .anchor}Figure . Identification of Summer Peak Day --
example (left); Identification of Winter Peak Day -- example (right)

The 24-hour heat index values for the summer peak, winter peak, and
spring light load day are then lagged (see Equation 2) and then combined
with the weather sensitivity factors to yield 24 normalized hourly
cooling and heating loads for each building type.

*Step 2b. Estimation of region-specific hourly loads for discretionary
electricity end uses*

The estimation of region-specific hourly loads for space cooling, space
heating, water heating, and cooking involves scaling the normalized
hourly loads for these end uses by electrification factors that reflect
the extent to which electricity is used for these end uses in each
region.

The electrification factors for the weather cities in the United States
were taken from survey research conducted by the US Energy Information
Administration (EIA). The surveys relied on a statistically-based
sampling procedure that produces electrification factors that are
representative of each building type for each of nine census regions in
the US. See Figure 6.

![U.S. Census Regions and Divisions Map](media/image9.png){width="3.9in"
height="3.1233070866141732in"}

[]{#_Toc41479610 .anchor}Figure . U.S. Census Regions

The residential electrification factors were taken from the EIA
Residential Energy Consumption Survey (RECS) \[US EIA 2015\]. RECS is a
periodic study that provides detailed information about energy usage in
U.S. homes. For the 2015 survey, which is the basis for the residential
electrification factors, approximately 5700 surveys were conducted. See
Table 4.

[]{#_Ref39828892 .anchor}Table . Electrification Factors -- U.S.
Residential

  **Region**           **Heat Pump**   **Other Electric Heat**   **Cooling**   **Water Heating**   **Cooking**
  -------------------- --------------- ------------------------- ------------- ------------------- -------------
  New England          3%              10%                       75%           36%                 59%
  Middle Atlantic      3%              11%                       88%           31%                 43%
  East North Central   3%              17%                       92%           34%                 57%
  West North Central   4%              18%                       92%           40%                 75%
  South Atlantic       24%             32%                       95%           72%                 78%
  East South Central   24%             39%                       93%           76%                 75%
  West South Central   8%              45%                       95%           58%                 71%
  Mountain             8%              19%                       78%           31%                 67%
  Pacific              7%              25%                       66%           32%                 53%

The commercial electrification factors were taken from the Commercial
Building Energy Consumption Survey (CBECS) \[US EIA 2012\] CBECS is a
national sample survey that collects information on the stock of U.S.
commercial buildings, including their energy-related building
characteristics and energy usage data (consumption and expenditures).
For the 2012 survey, which is the basis for the commercial
electrification factors, approximately 6700 surveys were conducted. See
Table 5.

[]{#_Ref39828906 .anchor}Table . Electrification Factors -- U.S.
Commercial

  **Region**           **Heat Pump**   **Other Electric Heat**   **Cooling**   **Water Heating**   **Cooking**
  -------------------- --------------- ------------------------- ------------- ------------------- -------------
  New England          9%              2%                        77%           45%                 27%
  Middle Atlantic      9%              6%                        89%           41%                 31%
  East North Central   5%              8%                        90%           39%                 33%
  West North Central   7%              14%                       87%           49%                 32%
  South Atlantic       27%             20%                       91%           62%                 30%
  East South Central   17%             23%                       88%           59%                 31%
  West South Central   10%             30%                       81%           47%                 25%
  Mountain             10%             13%                       84%           40%                 31%
  Pacific              15%             21%                       88%           51%                 22%

The electrification factors for the weather cities in Canada were
provided be Canadian members of the Northeast Power Coordinating
Council. See Table 6.

[]{#_Ref39828920 .anchor}Table . Electrification Factors -- Canadian

  **City**            **Residential Resistive Heating**   **Residential Heat Pump**   **Commercial Resistive Heating**   **Commercial Heat Pump**
  ------------------- ----------------------------------- --------------------------- ---------------------------------- --------------------------
  **Fredericton**     0.67                                0                           0.78                               0
  **Halifax**         0.33                                0                           0.34                               0
  **Ottawa**          0.28                                0                           0.17                               0
  **Quebec City**     0.77                                0                           0.62                               0
  **Thunder Bay**     0.26                                0                           0.19                               0
  **Sudbury**         0.15                                0                           0.12                               0
  **Montreal**        0.77                                0                           0.62                               0
  **Rouyn Noranda**   0.77                                0                           0.62                               0
  **Toronto**         0.15                                0                           0.12                               0
  **SeptIles**        0.77                                0                           0.62                               0
  **Calgary**         0.08                                0                           0.08                               0

***\
***

Step 3. Mapping end uses to the composite load model
----------------------------------------------------

Step 3 involves mapping, by building type, the seasonal, normalized,
hourly end-use loads to the seven composite load model load types used
in transmission planning modeling studies.

The outputs from Step 3 are, for each building type, a region-specific,
normalized, set of hourly loads each of the seven composite load model
load types for a summer peak day, winter peak day, and spring light load
day.

The mapping is embodied in a series of "look-up" tables---one for each
building type---that are known collectively as the Rules of Association.
The original Rules of Association were developed by transmission
planners and industry experts in the Western Interconnection. In 2019,
aspects of the Rules of Association were updated by information from a
recently completed DOE assessment of motor systems in the commercial and
industrial sectors \[Rao, et al 2019\].

The DOE Motor System Market Assessment project was a field assessment of
the current stock, electricity consumption, and cost-effective energy
savings opportunity for motor systems in U.S. commercial building and
industrial facilities. The assessment involved field surveys of over 300
industrial and 150 commercial facilities across the United States. The
assessment documents the increased reliance on variable speed drives for
many fan and pumping motors in the commercial sector (compared to what
was indicated in the original Rules of Association).

Table 7 through Table 10 present the updated Rules of Association used
in the load composition analysis for all commercial, large office,
lodging, and residential buildings, respectively.

[]{#_Ref39828934 .anchor}Table . Rules of Association for All Commercial
Buildings Except Large Office and Lodging

![](media/image10.emf){width="8.9in" height="1.0308562992125985in"}

[]{#_Toc41479622 .anchor}Table . Rules of Association for Large Office

![](media/image11.emf){width="8.9in" height="1.0308562992125985in"}

[]{#_Toc41479623 .anchor}Table . Rules of Association for Lodging

![](media/image12.emf){width="8.9in" height="1.0308562992125985in"}

[]{#_Ref39828942 .anchor}Table . Rules of Association for Residential
Buildings

![](media/image13.emf){width="8.9in" height="1.0308562992125985in"}

Step 4. Developing region-specific feeder models
------------------------------------------------

Step 4 involves developing region-specific feeder models that are
representative of different "economic" activities, which are be used to
distinguish non-industrial feeders from among one another.

The outputs from step 4 are composite load models for feeders for 96
region-specific sets of hourly loads for a summer peak day, a winter
peak day, and a spring light load day.

Four distinct feeder models were developed. Each feeder model is
comprised of a floor-area weighted combination of the normalized hourly
loads for different combinations of building types.

The first feeder model, RES, is representative of a feeder serving loads
in a suburban area. This model is comprised largely of residential
buildings. However, it also contains a variety of low-rise
non-residential buildings, such as small office, retail, grocery,
restaurants, schools, hospitals, etc. See Table 11.

[]{#_Ref39828959 .anchor}Table . Composition of Suburban or RES Feeder

  **Building Type**        **Number**   **Avg. SqFt/Building**   **Total SqFt**   
  ------------------------ ------------ ------------------------ ---------------- -------
  Res. Home                4000         1500                     6000000          81.2%
  College                  0            500000                   0                0.0%
  Grocery                  2            45000                    90000            1.2%
  Health                   4            10000                    40000            0.5%
  Large Office             0            700000                   0                0.0%
  Lodging                  0            50000                    0                0.0%
  Miscellaneous            1            10000                    10000            0.1%
  Refrigerated Warehouse   0            50000                    0                0.0%
  Restaurant               20           5000                     100000           1.4%
  Retail                   30           20000                    600000           8.1%
  School                   4            100000                   400000           5.4%
  Small Office             0            50000                    0                0.0%
  Warehouse                3            50000                    150000           2.0%

The second feeder model, COM, is representative of a feeder serving
loads in downtown, urban area. This model features, uniquely among the
four feeder models, large high-rise offices, which feature central HVAC
plants. In contrast to low-rise buildings which rely on composite load
motor type A for cooling, high-rise buildings rely on composite motor
type B for cooling. See Table 12.

[]{#_Ref39828970 .anchor}

Table . Composition of Downtown Urban or COM Feeder

  **Building Type**        **Number**   **SqFt/Building**   **Total SqFt**   
  ------------------------ ------------ ------------------- ---------------- -------
  Res. Home                0            1500                0                0.0%
  College                  0            500000              0                0.0%
  Grocery                  2            45000               90000            1.5%
  Health                   4            10000               40000            0.6%
  Large Office             6            700000              4200000          68.1%
  Lodging                  20           50000               1000000          16.2%
  Miscellaneous            1            10000               10000            0.2%
  Refrigerated Warehouse   0            50000               0                0.0%
  Restaurant               25           5000                125000           2.0%
  Retail                   30           20000               600000           9.7%
  School                   0            100000              0                0.0%
  Small Office             2            50000               100000           1.6%
  Warehouse                0            50000               0                0.0%

The third feeder model, MIX, is a hybrid that combines as aspects of
both the RES and COM feeder models. It is representative of feeders
serving transition zones between largely residential suburban areas and
dense high-rise urban areas. It contains fewer residential buildings
than RES, but also does not contain large offices, which are prominent
in COM. See Table 13.

[]{#_Ref39828981 .anchor}Table . Composition of Hybrid or MIX Feeder

  **Building Type**        **Number**   **SqFt/Building**   **Total SqFt**   
  ------------------------ ------------ ------------------- ---------------- -------
  Res. Home                2000         1500                3000000          49.9%
  College                  0            500000              0                0.0%
  Grocery                  3            45000               135000           2.2%
  Health                   6            10000               60000            1.0%
  Large Office             0            700000              0                0.0%
  Lodging                  6            50000               300000           5.0%
  Miscellaneous            2            10000               20000            0.3%
  Refrigerated Warehouse   2            50000               100000           1.7%
  Restaurant               40           5000                200000           3.3%
  Retail                   40           20000               800000           13.3%
  School                   4            100000              400000           6.7%
  Small Office             12           50000               600000           10.0%
  Warehouse                8            50000               400000           6.7%

The fourth feeder model, RUR, is representative of feeders serving rural
areas. Like RES, it contains a significant amount of residential
buildings. But, it differs from RES in the variety and proportions of
non-residential buildings. See Table 14.

[]{#_Ref39828988 .anchor}

Table . Composition of Rural or RUR Feeder

  **Building Type**        **Number**   **SqFt/Building**   **Total SqFt**   
  ------------------------ ------------ ------------------- ---------------- -------
  Res. Home                400          1500                600000           43.5%
  College                  0            500000              0                0.0%
  Grocery                  1            45000               45000            3.3%
  Health                   0            10000               0                0.0%
  Large Office             0            700000              0                0.0%
  Lodging                  1            50000               50000            3.6%
  Miscellaneous            0            10000               0                0.0%
  Refrigerated Warehouse   0            50000               0                0.0%
  Restaurant               5            5000                25000            1.8%
  Retail                   3            20000               60000            4.3%
  School                   1            100000              100000           7.2%
  Small Office             0            2000                0                0.0%
  Warehouse                10           50000               500000           36.2%

Representative Outcomes from the Load Composition Analysis
==========================================================

The outputs from the load composition analysis are composite load models
for four sets of feeders for 96 region-specific sets of hourly loads for
a summer peak day, a winter peak day, and a spring light load day.
Figure 7 shows, for a single region/weather-city (Atlanta) how the
hourly loads vary over the hours of the summer peak day for the RES and
MIX feeder models. Figure 8 shows how the composite load model
proportions vary at the time of summer peak demand for these same four
feeders.

![](media/image14.png){width="6.200536964129483in"
height="2.3868733595800524in"}

[]{#_Ref39829149 .anchor}Figure . Summer Peak Day, Atlanta -- RES Feeder
(left); Summer Peak Day, Atlanta -- MIX Feeder (right)

![](media/image15.png){width="6.499498031496063in"
height="2.45454615048119in"}

[]{#_Ref39829571 .anchor}Figure . Summer Peak Hour (4 pm), Atlanta --
RES Feeder (left); Summer Peak Hour (4 pm), Atlanta -- MIX Feeder
(right)

Figure 9 shows, for the MIX feeder model in a different
region/weather-city (Toronto), how the hourly loads vary over the hours
of the summer peak, winter peak, and spring light load day. Figure 14
shows how the composite load model proportions vary at the time of peak
demand for these three seasons.

![](media/image16.png){width="6.3in" height="5.099904855643045in"}

[]{#_Ref39829801 .anchor}Figure . MIX Feeder, Toronto, Summer Peak Day
(top left); MIX Feeder, Toronto, Winter Peak Day (top right); MIX
Feeder, Toronto, Spring Light Load Day (bottom)

![](media/image17.png){width="6.5in" height="4.947222222222222in"}

[]{#_Toc41479614 .anchor}Figure . MIX Feeder, Toronto, Summer Peak Hour
(4 pm) (top left); MIX Feeder, Toronto, Winter Peak Hour (8 am) (top
right); MIX Feeder, Toronto, Spring Light Load Hour (3 am) (bottom)

**\
**

References {#references .Heading}
==========

Ecotope, Inc. 2014. Residential Building Stock Assessment: Metering
Study. Report \#E14-283. Prepared for Northwest Energy Efficiency
Alliance. April 28.
<http://ecotope.com/project/residential-building-stock-assessment-metering-rbsam/>

Government of Canada. 2020. "Historical Climate Data." Website accessed
May 16, 2020, at <https://climate.weather.gc.ca/>.

Itron, Inc. 2006. California Commercial End-Use Survey.
CEC-400-2006-005. Prepared for California Energy Commission. March.
<https://ww2.energy.ca.gov/2006publications/CEC-400-2006-005/CEC-400-2006-005.PDF>

Kosterev, D., C. Taylor, and W. Mittelstadt. 1999. "Model Validation for
the August 10, 1996 WSCC System Outage." *IEEE Transactions on Power
Systems.* Vol. 14, No. 3, August.

National Centers for Environmental Information (NCEI). 2020. "U.S.
Climatological Data (LCD)." Webpage accessed May 14, 2020, at
<https://www.ncei.noaa.gov/access/search/data-search/local-climatological-data>.

National Weather Service. 2020. "Heat Index." Webpage accessed May 15,
2020 at <https://www.weather.gov/safety/heat-index>.

North American Electric Reliability Corporation (NERC). 2016. Technical
Reference Document, Dynamic Load Modeling. December.
[https://www.nerc.com/comm/PC/LoadModelingTaskForceDL/\
Dynamic%20Load%20Modeling%20Tech%20Ref%202016-11-14%20-%20FINAL.PDF](https://www.nerc.com/comm/PC/LoadModelingTaskForceDL/Dynamic%20Load%20Modeling%20Tech%20Ref%202016-11-14%20-%20FINAL.PDF)

North American Electric Reliability Corporation. 2017. Reliability
Guideline, Developing Load Model Composition Data. March.
[https://www.nerc.com/comm/PC\_Reliability\_Guidelines\_DL/\
Reliability\_Guideline\_-\_Load\_Model\_Composition\_-\_2017-02-28.pdf](https://www.nerc.com/comm/PC_Reliability_Guidelines_DL/Reliability_Guideline_-_Load_Model_Composition_-_2017-02-28.pdf)

Rao, P., P. Sheaffer, P. Scheihing. 2019. "Method for Assessing the U.S.
Industrial and Commercial Motor Systems Markets." ACEEE 2019 Industry
Summer Study on Energy Efficiency. Portland, OR. August 12-14.
<https://www.aceee.org/2019-industry-summer-study>

U.S. Energy Information Administration. 2012. Commercial Building Energy
Consumption Survey.
<https://www.eia.gov/consumption/commercial/data/2012/>

U.S. Energy Information Administration. 2015. Residential Energy
Consumption Survey.
<https://www.eia.gov/consumption/residential/data/2015/>

Williams, B., W. Schmus, and D. Dawson. 1992. "Transmission Voltage
Recovery Delayed by Stalled Air Conditioner Compressors. IEEE
Transactions on Power Systems. Vol. 7, No. 3.

[^1]: <https://www.nerc.com/_layouts/15/PrintStandard.aspx?standardnumber=TPL-001-4&title=Transmission%20System%20Planning%20Performance%20Requirements&jurisdiction=United%20States>

[^2]: [https://www.nerc.com/comm/PC/LoadModelingTaskForceDL/\
    Dynamic%20Load%20Modeling%20Tech%20Ref%202016-11-14%20-%20FINAL.PDF](https://www.nerc.com/comm/PC/LoadModelingTaskForceDL/Dynamic%20Load%20Modeling%20Tech%20Ref%202016-11-14%20-%20FINAL.PDF)

[^3]: The industrial load bus models that were used in the field test
    were based on ones that had been previously developed for planners
    in the Western interconnection.

[^4]: <https://certs.lbl.gov/initiatives/fidvr/>

[^5]: <https://www.nerc.com/_layouts/15/PrintStandard.aspx?standardnumber=TPL-001-4&title=Transmission%20System%20Planning%20Performance%20Requirements&jurisdiction=United%20States>

[^6]: The industrial load bus models that were used in the field test
    were based on ones that had been previously developed for planners
    in the Western interconnection. These models were reviewed and
    updated as appropriate for use in the Eastern and Texas
    interconnections through a separate analysis.

[^7]: The total floor area of the residences in the feeder was estimated
    by dividing the mild day load by the normalized non-weather
    sensitive loads estimated in step 1b.
