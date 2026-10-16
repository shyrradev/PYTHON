-- sites
SELECT DISTINCT Launch_Site FROM launches ORDER BY Launch_Site;

-- ccaf_first5
SELECT Date, Launch_Site, Payload FROM launches WHERE Launch_Site LIKE 'CCA%' LIMIT 5;

-- nasa_payload
SELECT SUM(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Customer='NASA (CRS)';

-- f9v11_average
SELECT AVG(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Booster_Version LIKE 'F9 v1.1%';

-- first_ground
SELECT MIN(Date) AS date FROM launches WHERE Landing_Outcome='Success (ground pad)';

-- drone_4_6t
SELECT Booster_Version FROM launches WHERE Landing_Outcome='Success (drone ship)' AND PAYLOAD_MASS__KG_>4000 AND PAYLOAD_MASS__KG_<6000;

-- mission_outcomes
SELECT Mission_Outcome, COUNT(*) AS n FROM launches GROUP BY Mission_Outcome;

-- max_payload
SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM launches WHERE PAYLOAD_MASS__KG_=(SELECT MAX(PAYLOAD_MASS__KG_) FROM launches);

-- failures_2015
SELECT Date, Booster_Version, Launch_Site FROM launches WHERE Date LIKE '2015%' AND Landing_Outcome='Failure (drone ship)';

-- landing_rank
SELECT Landing_Outcome,COUNT(*) AS n FROM launches WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY n DESC;