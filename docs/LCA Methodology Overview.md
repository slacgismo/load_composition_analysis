# LCA front end and outline 
20 April 2020

## Synopsis

In 201[?], NERC’s reliability standards were revised to require the use of dynamic load models in transmission planning studies. Modeling the dynamic behavior of loads requires an explicit representation of the end-use composition of loads, especially of motor-driven and power electronics-based loads. These representations – known as composite load models - must be adjusted based on the characteristics of the load served. While use of composite load models is a long-standing practice for planners in the Western Interconnection, use of these models is a new practice for the majority of planners in the Eastern Interconnection and ERCOT.

In 2019 in anticipation of the compliance date for the new standards, NERC’s Load Modeling Task Force initiated a field test of composite load models for planners in the Eastern Interconnection and ERCOT. In support of the field test, DOE and BPA researchers developed 96 region-specific composite load models for use by transmission planners to represent each of four distinct types of non-industrial feeders. The results were made available to planners in the form of composite load models for a summer peak hour, a winter peak hour, and a spring light-load hour. This report is the technical documentation for the load composition analysis that was conducted to develop these composite load models.

# The Role of Load Composition Analysis in Supporting the Development of Composite Load Models

Transmission planning studies are conducted using positive-sequence load flow models that simulate the dynamic behavior of the transmission system under stressed conditions. The influence of loads on the dynamic behavior of the system under these conditions is introduced through the use of composite load models.

A separate composite load model must be specified for each node (or feeder) within the transmission system at which load is withdrawn. Each composite load model involves dividing the loads served at each feeder into one of seven categories. Each of the seven categories represents a different type of behavior that will load exhibit in the dynamic simulation studies.

For nodes at which a single or group of like industrial customer is served, there is a growing library of industry-specific composite load models. However, for the vast majority of nodes that serve non-industrial loads, methods must be developed, which account for the enormous diversity that exists in the composition of non-industrial feeders. This diversity ranges from feeders that are dominated by residential sector customers to feeders that are dominated by commercial sector customers. Within the commercial sector, itself, there is even greater diversity in the range of activities that must be taken into account, such as offices versus restaurants, retail businesses versus hospitals, and so on.

Fortunately, 40 years of demand-side management planning by utilities has led to a great deal of publicly available information on residential- and commercial-sector uses of electricity. Much is now known about the variability of certain loads, such as heating and cooling, under different climatic conditions. Similarly, much is also known about the common features of loads that serves specific, identifiable purposes, such as lighting, refrigeration, cooking, etc. 

The application of information on residential and commercial sector electricity use to develop composite load models for non-industrial feeders is called load composition analysis.

## Overview of the DOE/BPA Load Composition Analysis Process

The load composition analysis process consisted of three steps. Step 1 involved the compilation and analysis of publicly available information on residential and commercial sector end-use loads. Step 2 involved compilation of region-specific information on weather and on the use of electricity for certain, discretionary end-uses (such as space heating, water heating, and cooking). Step 3 involves the preparation of representative feeder models for each target region based on using the information developed in Step 2 to adjust and transform the information developed in Step 1.

TONY – I AM ONLY GOING TO SKETCH WHAT I UNDERSTAND TO BE THE MAJOR STEPS IN THE REMAINDER OF THIS OUTLINE – ONCE YOU AND I TALK AND CONFIRM WHAT IT IS YOU REALLY DID, I WILL FINALIZE THIS OUTLINE AND MOVE THE MATERIAL FROM YOUR EARLIER WORKING DRAFT UNDER THE CORRECT SUB-HEADINGS BELOW

NOTE THAT (BESIDES BEING WRONG IN SOME PLACES) THE EXPLANATION I PRESENT BELOW DOES NOT LITERALLY FOLLOW THE STEPS IN YOUR ANALYSIS PROCEDURES – BUT I DO THINK IT IS USEFUL TO ORGANIZE THE STEPS IN THE SEQUENCE I HAVE OUTLINED – OBVIOUSLY WE WILL DISCUSS AND AGREE ON ALL OF THIS BEFORE THIS DOCUMENT IS FINAL

### Step 0.  ANALYSIS ELEMENTS

The unit of analysis is building types and the end uses within each building type.

For the residential sector, 1 building type is used

For the commercial sector, 11 buildings types were used – list them (not College)

For each building type in both sectors, 13 end-uses are used

The rules association map each of the 13 end-uses, varying by some (but not all of the) building types, to 7 composite load model fractions.

### Step 1. ANALYSIS OF LOAD INFORMATION

The analysis is based on end-use metering data collected from representative samples of residential and commercial buildings.

The sources of end-use metering data are residential non-weather sensitive X; residential weather sensitive Y; commercial all end uses CEC CEUS.

#### Step 1a. aggregation of end-use metering sites

End-use meter information for like building types are combined and then normalized by floor area

TABLE 1a1 shows number of end use metered buildings that were aggregated for each building type and end use

#### Step 1b. extraction of load shape characteristics

The development of base load shapes varies according to three types of end uses: 1) weather sensitive (heating and cooling); 2) discretionary electricity (space heating, water heating, cooking); 3) electricity only (all others, e.g., lighting, etc.)

##### Step 1b1. Weather sensitive

Historic weather recorded at the time of the end-use metering is regressed separately for each hour against electricity consumption. Weather is represented by hourly temperature for heating; and by hourly temperature severity index (a weighting of dry bulb temperature and humidity) for cooling

Heating analysis relied on weather and end use metering for winter months (LIST MONTHS and whether weekend/holiday excluded)

Cooling analysis relied on weather and end use metering for summer months (LIST MONTHS and whether weekend/holiday excluded)

The outcome is 24 sets of hour regression coefficients (intercept and slope) – one set for heating; one set for cooling.

##### Step 1b2. Electricity discretionary

Only end use metered data from buildings relying on electricity for space heating, water heating, or cooking were aggregated in Step 1

For water heating and cooking, 24 hourly values, separate for each of the three sessions is developed by averaging over (weekday only?) from (which months?)

Region-specific information is used in step 2 to adjust these “pure” (or 100% electric saturation) load shapes up or down

The outcome is 24 hour load shapes for each end use for each season

##### Step 1b3 Electricity only load shapes

The floor area normalized 24 hourly values, separate for each of the three sessions is developed by averaging over (weekday only?) from (which months?)

The outcome is 24 hour load shapes for each end use for each season

### Step 2. INTRODUCTION OF REGION-SPECIFIC INFORMATION / APPLICATION OF RULES OF ASSOCIATION

Two sources of region-specific information were used to adjust the base information developed in step 1

First, information on region-specific adoption of electricity for space heating, water heating, and cooking is used to adjust the magnitude of the relative contributions of these end uses to the total electricity load

The source of the information is either US EIA CBECS or RECS for the US weather cities, or information provided by Canadian planners for the Canadian cities.  See TABLE 2-1

Second, 24 hourly values of temperature and humidity are used to adjust the electricity used for heating and cooling on an hourly basis using the weather sensitivity coefficients developed in Step 1

The source of hourly temperature and humidity information is based on review of 25 years of historical weather for each city. Separate groupings of months of historical weather were reviewed to develop the Winter, Summer, and Spring values used in the analysis. LIST THE MONTHS USED FOR EACH SEASON. For the peak winter and summer day, the 24 hours associated with the historical day that came closest to the 95% of the peak hour was selected.  For the spring light load day, ….

FIGURE 2-1 96 WEATHER CITIES

In a final step, building type specific rules of association assign end use values to one of seven composite load types.

Aspects of the Rules of Association were update in 2019 based on information from a recent LBNL national survey of motors.

TABLE 2-2 final rules of associations

The outcome is a 24 hour load shape for each season, for each building type, and for each of the seven composite load types.

### Step 3. FORMATION OF REGION-SPECIFIC FEEDERS

Four distinct feeder models were developed for each of the 96 weather cities

Each feeder model is comprised of a floor-area weighted combination of different building types

Table 3-1 shows the compositions of the four feeder models by building type

For each feeder model, 24-hour load shapes (each hour comprised of allocations of load among the 7 composite load types) were prepared for a study day in each of three seasons
