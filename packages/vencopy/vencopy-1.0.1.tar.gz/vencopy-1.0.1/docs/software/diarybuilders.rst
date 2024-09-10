.. venco.py documentation source file, created for sphinx

.. _diarybuilders:


DiaryBuilders Level
===================================

.. image:: ../figures/IOdiarybuilder.svg
	:width: 800
	:align: center

DiaryBuilders Input
---------------------------------------------------
**Config File (user_config.yaml):**

* time_resolution: <value> - User-specific time resolution in minutes
* is_week_diary: bool - Determine if the activity data set comprises weekly
  activity chains (synthesized by WeekDiaryBuilder)


**venco.py Classes:**

 * FlexEstimator class output


DiaryBuilders Output
---------------------------------------------------


**Output Functions:**

 * diary = DiaryBuilder(configs=configs, activities=flex.activities)
 * diary.create_diaries()


**Disk Files:**

 * Electric battery drain (.csv) `drain`
 * Available charging power (.csv) `charging_power`
 * Uncontrolled charging profile (.csv) `uncontrolled_charging`
 * Maximum battery energy level (.csv) `max_battery_level`
 * Minimum battery energy level (.csv) `min_battery_level`


DiaryBuilders Structure
---------------------------------------------------

In this step of the workflow, individual, time-discrete profiles are being created from columns of the activities 
dataset. Thus one activities-column with a activity id, start and end time, is discretized in a pre-defined temporal 
resolution. For a 15 minutes resolution, every profile consists of 24x60=1440 values for a full day. Since an explicit 
temporal dimension is added to the data, the output profiles are stored in individual class variables in a wrapper 
class, the DiaryBuilder. This class then calls a function of the class TimeDiscretizer, 
namely TimeDiscretizer.discretise(), in which the resolution and the discretization method is given. 


DiaryBuilder Class
#################################################################

The Class DiaryBuilder is the interface between the central venco.py workflow and the individual profile 
discretizations. Rounding to the user-defined temporal resolution occurs on this level before the individual 
discretisation of columns is called. After discretization (see below), profiles are written to disk, if requested in 
the user-config. 


TimeDiscretiser Class
#################################################################

The discretisation approach implemented in venco.py varies according to the
considered profile. Below, the different approaches are presented:

- Profile for uncontrolled charging `uncontrolled_charging`: The uncontrolled charging profile is discretised
  in a step-wise linear manner (function :py:meth:`diarybuilders.TimeDiscretiser.__value_non_linear_charge`). This means
  the value for each timestamp is calculated using a stepwise linearly increasing list of values capped to the upper 
  battery capacity. The discretisation approach changes depending on whether the vehicles are driving (function
  :py:meth:`diarybuilders.TimeDiscretiser.__uncontrolled_charging_driving`) or are parked (function
  :py:meth:`diarybuilders.TimeDiscretiser.__uncontrolled_charging_parking`).
- Profile for the electric demand `drain`: The discretisation and timeseries creation for the drain profiles is carried 
  out by distributing the value for the profile equally across the number of timestamp in which there is an electric 
  consumption (function :py:meth:`diarybuilders.TimeDiscretiser.__value_distribute`). E.g. a 10 kWh electric consumption 
  in a 15 minutes resolution results in a specific consumption of 2.5 kWh for each of the 4 timestamps in one hour.
- Profile for the charging capacity of the fleet `charging_power`: The charging power profiles is discretised in which 
  the same value (in kW) is assigned for each timestamp in which there is a connection capacity available, 
  independently of the temporal resolution selected by the user 
  (function :py:meth:`diarybuilders.TimeDiscretiser.__value_select`). 
- Maximum and minimum battery level profile `max_battery_level` and `min_battery_level`: Similarly to the uncontrolled 
  charging profile, the minimum and maximum battery level are also discretised dynamically (function
  :py:meth:`diarybuilders.TimeDiscretiser.__value_non_linear_level`). This means the values for each timestamp are 
  calculated using a stepwise-linearly increasing list of values capped to upper and lower battery capacity 
  limitations. The discretisation approaches changes depending on whether the vehicles are driving (function
  :py:meth:`diarybuilders.TimeDiscretiser.__delta_battery_level_driving`) or are parked (function
  :py:meth:`diarybuilders.TimeDiscretiser.__delta_battery_level_charging`). 