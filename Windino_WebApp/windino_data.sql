DROP TABLE IF EXISTS arduino;

CREATE TABLE arduino (
				   zone TEXT,
				   id TEXT,
				   date DATE,
				   hour TIME,
                   speed FLOAT,
                   power FLOAT,
				   current FLOAT,
				   error TEXT);


-- Zona 1, ID 1
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 1', '2023-03-17', '08:00:00', 6.85, 765.42, 36.64, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 1', '2023-03-17', '09:00:00', 7.32, 802.16, 38.24, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 1', '2023-03-17', '10:00:00', 6.97, 756.88, 37.12, 'no error');

-- Zona 1, ID 2
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 2', '2023-03-17', '08:00:00', 7.08, 789.71, 38.24, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 2', '2023-03-17', '09:00:00', 6.62, 726.96, 35.84, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 2', '2023-03-17', '10:00:00', 7.12, 789.09, 37.92, 'no error');

-- Zona 1, ID 3
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 3', '2023-03-17', '08:00:00', 7.29, 813.37, 39.04, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 3', '2023-03-17', '09:00:00', 7.63, 845.29, 40.56, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 1', 'id 3', '2023-03-17', '10:00:00', 6.98, 763.74, 37.28, 'no error');

-- Zona 2, ID 1
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 1', '2023-03-17', '08:00:00', 6.85, 765.42, 36.64, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 1', '2023-03-17', '09:00:00', 7.92, 702.67, 34.14, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 1', '2023-03-17', '10:00:00', 6.31, 642.88, 28.89, 'no error');

-- Zona 2, ID 2
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 2', '2023-03-17', '09:00:00', 9.03, 549.32, 17.67, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 2', '2023-03-17', '09:00:00', 8.51, 612.74, 20.35, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 2', '2023-03-17', '10:00:00', 8.72, 577.91, 19.76, 'no error');

-- Zona 2, ID 3
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 3', '2023-03-17', '08:00:00', 7.39, 825.01, 31.15, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 3', '2023-03-17', '09:00:00', 6.51, 794.11, 27.98, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 2', 'id 3', '2023-03-17', '10:00:00', 7.12, 718.22, 29.94, 'no error');

-- Zona 3, ID 1
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 1', '2023-03-17', '08:00:00', 8.11, 891.02, 42.88, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 1', '2023-03-17', '09:00:00', 7.93, 876.17, 42.08, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 1', '2023-03-17', '10:00:00', 8.07, 894.27, 43.04, 'no error');

-- Zona 3, ID 2
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 2', '2023-03-17', '08:00:00', 7.95, 878.10, 42.24, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 2', '2023-03-17', '09:00:00', 8.03, 889.80, 42.88, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 2', '2023-03-17', '10:00:00', 8.21, 908.33, 43.84, 'no error');

-- Zona 3, ID 3
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 3', '2023-03-17', '08:00:00', 8.17, 903.42, 43.52, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 3', '2023-03-17', '09:00:00', 8.12, 897.22, 43.36, 'no error');
INSERT INTO arduino (zone, id, date, hour, speed, power, current, error)
VALUES ('zona 3', 'id 3', '2023-03-17', '10:00:00', 7.95, 878.10, 42.24, 'no error');

