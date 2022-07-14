-- ------------------------------------------------------------------
-- Title: Sequential Organ Failure Assessment (SOFA)
-- This query extracts the sequential organ failure assessment (formally: sepsis-related organ failure assessment).
-- This score is a measure of organ failure for patients in the ICU.
-- The score is calculated on the first day of each ICU patients' stay.
-- ------------------------------------------------------------------

-- Reference for SOFA:
--    Jean-Louis Vincent, Rui Moreno, Jukka Takala, Sheila Willatts, Arnaldo De Mendonça,
--    Hajo Bruining, C. K. Reinhart, Peter M Suter, and L. G. Thijs.
--    "The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure."
--    Intensive care medicine 22, no. 7 (1996): 707-710.

-- Variables used in SOFA:
--  GCS, MAP, FiO2, Ventilation status (sourced FROM chartevents)
--  Creatinine, Bilirubin, FiO2, PaO2, Platelets (sourced FROM labevents)
--  Dobutamine, Epinephrine, Norepinephrine (sourced FROM inputevents_mv and INPUTEVENTS_CV)
--  Urine output (sourced from OUTPUTEVENTS)

-- The following views required to run this query:
--  1) urine_output_first_day - generated by urine-output-first-day.sql
--  2) vitals_first_day - generated by vitals-first-day.sql
--  3) gcs_first_day - generated by gcs-first-day.sql
--  4) labs_first_day - generated by labs-first-day.sql
--  5) blood_gas_first_day_arterial - generated by blood-gas-first-day-arterial.sql
--  6) echodata - generated by echo-data.sql
--  7) ventilation_durations - generated by ventilation_durations.sql

-- Note:
--  The score is calculated for *all* ICU patients, with the assumption that the user will subselect appropriate ICUSTAY_IDs.
--  For example, the score is calculated for neonates, but it is likely inappropriate to actually use the score values for these patients.

with wt AS
(
  SELECT ie.icustay_id
    -- ensure weight is measured in kg
    , avg(CASE
        WHEN itemid IN (762, 763, 3723, 3580, 226512)
          THEN valuenum
        -- convert lbs to kgs
        WHEN itemid IN (3581)
          THEN valuenum * 0.45359237
        WHEN itemid IN (3582)
          THEN valuenum * 0.0283495231
        ELSE null
      END) AS weight

  FROM icustays ie
  left join chartevents c
    on ie.icustay_id = c.icustay_id
  WHERE valuenum IS NOT NULL
  AND itemid IN
  (
    762, 763, 3723, 3580,                     -- Weight Kg
    3581,                                     -- Weight lb
    3582,                                     -- Weight oz
    226512 -- Metavision: Admission Weight (Kg)
  )
  AND valuenum != 0
  and charttime between DATETIME_SUB(ie.intime, INTERVAL '1' DAY) and DATETIME_ADD(ie.intime, INTERVAL '1' DAY)
  -- exclude rows marked as error
  AND (c.error IS NULL OR c.error = 0)
  group by ie.icustay_id
)
-- 5% of patients are missing a weight, but we can impute weight using their echo notes
, echo2 as(
  select ie.icustay_id, avg(weight * 0.45359237) as weight
  FROM icustays ie
  left join echo_data echo
    on ie.hadm_id = echo.hadm_id
    and echo.charttime > DATETIME_SUB(ie.intime, INTERVAL '7' DAY)
    and echo.charttime < DATETIME_ADD(ie.intime, INTERVAL '1' DAY)
  group by ie.icustay_id
)
, vaso_cv as
(
  select ie.icustay_id
    -- case statement determining whether the ITEMID is an instance of vasopressor usage
    , max(case
            when itemid = 30047 then rate / coalesce(wt.weight,ec.weight) -- measured in mcgmin
            when itemid = 30120 then rate -- measured in mcgkgmin ** there are clear errors, perhaps actually mcgmin
            else null
          end) as rate_norepinephrine

    , max(case
            when itemid =  30044 then rate / coalesce(wt.weight,ec.weight) -- measured in mcgmin
            when itemid in (30119,30309) then rate -- measured in mcgkgmin
            else null
          end) as rate_epinephrine

    , max(case when itemid in (30043,30307) then rate end) as rate_dopamine
    , max(case when itemid in (30042,30306) then rate end) as rate_dobutamine

  FROM icustays ie
  inner join inputevents_cv cv
    on ie.icustay_id = cv.icustay_id and cv.charttime between ie.intime and DATETIME_ADD(ie.intime, INTERVAL '1' DAY)
  left join wt
    on ie.icustay_id = wt.icustay_id
  left join echo2 ec
    on ie.icustay_id = ec.icustay_id
  where itemid in (30047,30120,30044,30119,30309,30043,30307,30042,30306)
  and rate is not null
  group by ie.icustay_id
)
, vaso_mv as
(
  select ie.icustay_id
    -- case statement determining whether the ITEMID is an instance of vasopressor usage
    , max(case when itemid = 221906 then rate end) as rate_norepinephrine
    , max(case when itemid = 221289 then rate end) as rate_epinephrine
    , max(case when itemid = 221662 then rate end) as rate_dopamine
    , max(case when itemid = 221653 then rate end) as rate_dobutamine
  FROM icustays ie
  inner join inputevents_mv mv
    on ie.icustay_id = mv.icustay_id and mv.starttime between ie.intime and DATETIME_ADD(ie.intime, INTERVAL '1' DAY)
  where itemid in (221906,221289,221662,221653)
  -- 'Rewritten' orders are not delivered to the patient
  and statusdescription != 'Rewritten'
  group by ie.icustay_id
)
, pafi1 as
(
  -- join blood gas to ventilation durations to determine if patient was vent
  select bg.icustay_id, bg.charttime
  , pao2fio2
  , case when vd.icustay_id is not null then 1 else 0 end as isvent
  from {{ref('blood_gas_first_day_arterial')}} bg
  left join {{ref('ventilation_durations')}} vd
    on bg.icustay_id = vd.icustay_id
    and bg.charttime >= vd.starttime
    and bg.charttime <= vd.endtime
  order by bg.icustay_id, bg.charttime
)
, pafi2 as
(
  -- because pafi has an interaction between vent/PaO2:FiO2, we need two columns for the score
  -- it can happen that the lowest unventilated PaO2/FiO2 is 68, but the lowest ventilated PaO2/FiO2 is 120
  -- in this case, the SOFA score is 3, *not* 4.
  select icustay_id
  , min(case when isvent = 0 then pao2fio2 else null end) as pao2fio2_novent_min
  , min(case when isvent = 1 then pao2fio2 else null end) as pao2fio2_vent_min
  from pafi1
  group by icustay_id
)
-- Aggregate the components for the score
, scorecomp as
(
select ie.icustay_id
  , v.meanbp_min
  , coalesce(cv.rate_norepinephrine, mv.rate_norepinephrine) as rate_norepinephrine
  , coalesce(cv.rate_epinephrine, mv.rate_epinephrine) as rate_epinephrine
  , coalesce(cv.rate_dopamine, mv.rate_dopamine) as rate_dopamine
  , coalesce(cv.rate_dobutamine, mv.rate_dobutamine) as rate_dobutamine

  , l.creatinine_max
  , l.bilirubin_max
  , l.platelet_min

  , pf.pao2fio2_novent_min
  , pf.pao2fio2_vent_min

  , uo.urineoutput

  , gcs.mingcs
FROM icustays ie
left join vaso_cv cv
  on ie.icustay_id = cv.icustay_id
left join vaso_mv mv
  on ie.icustay_id = mv.icustay_id
left join pafi2 pf
 on ie.icustay_id = pf.icustay_id
left join {{ref('vitals_first_day')}} v
  on ie.icustay_id = v.icustay_id
left join {{ref('labs_first_day')}} l
  on ie.icustay_id = l.icustay_id
left join {{ref('urine_output_first_day')}} uo
  on ie.icustay_id = uo.icustay_id
left join {{ref('gcs_first_day')}} gcs
  on ie.icustay_id = gcs.icustay_id
)
, scorecalc as
(
  -- Calculate the final score
  -- note that if the underlying data is missing, the component is null
  -- eventually these are treated as 0 (normal), but knowing when data is missing is useful for debugging
  select icustay_id
  -- Respiration
  , case
      when pao2fio2_vent_min   < 100 then 4
      when pao2fio2_vent_min   < 200 then 3
      when pao2fio2_novent_min < 300 then 2
      when pao2fio2_novent_min < 400 then 1
      when coalesce(pao2fio2_vent_min, pao2fio2_novent_min) is null then null
      else 0
    end as respiration

  -- Coagulation
  , case
      when platelet_min < 20  then 4
      when platelet_min < 50  then 3
      when platelet_min < 100 then 2
      when platelet_min < 150 then 1
      when platelet_min is null then null
      else 0
    end as coagulation

  -- Liver
  , case
      -- Bilirubin checks in mg/dL
        when bilirubin_max >= 12.0 then 4
        when bilirubin_max >= 6.0  then 3
        when bilirubin_max >= 2.0  then 2
        when bilirubin_max >= 1.2  then 1
        when bilirubin_max is null then null
        else 0
      end as liver

  -- Cardiovascular
  , case
      when rate_dopamine > 15 or rate_epinephrine >  0.1 or rate_norepinephrine >  0.1 then 4
      when rate_dopamine >  5 or rate_epinephrine <= 0.1 or rate_norepinephrine <= 0.1 then 3
      when rate_dopamine >  0 or rate_dobutamine > 0 then 2
      when meanbp_min < 70 then 1
      when coalesce(meanbp_min, rate_dopamine, rate_dobutamine, rate_epinephrine, rate_norepinephrine) is null then null
      else 0
    end as cardiovascular

  -- Neurological failure (GCS)
  , case
      when (mingcs >= 13 and mingcs <= 14) then 1
      when (mingcs >= 10 and mingcs <= 12) then 2
      when (mingcs >=  6 and mingcs <=  9) then 3
      when  mingcs <   6 then 4
      when  mingcs is null then null
  else 0 end
    as cns

  -- Renal failure - high creatinine or low urine output
  , case
    when (creatinine_max >= 5.0) then 4
    when  urineoutput < 200 then 4
    when (creatinine_max >= 3.5 and creatinine_max < 5.0) then 3
    when  urineoutput < 500 then 3
    when (creatinine_max >= 2.0 and creatinine_max < 3.5) then 2
    when (creatinine_max >= 1.2 and creatinine_max < 2.0) then 1
    when coalesce(urineoutput, creatinine_max) is null then null
  else 0 end
    as renal
  from scorecomp
)
select ie.subject_id, ie.hadm_id, ie.icustay_id
  -- Combine all the scores to get SOFA
  -- Impute 0 if the score is missing
  , coalesce(respiration,0)
  + coalesce(coagulation,0)
  + coalesce(liver,0)
  + coalesce(cardiovascular,0)
  + coalesce(cns,0)
  + coalesce(renal,0)
  as SOFA
, respiration
, coagulation
, liver
, cardiovascular
, cns
, renal
FROM icustays ie
left join scorecalc s
  on ie.icustay_id = s.icustay_id
order by ie.icustay_id
