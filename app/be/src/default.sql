CREATE TABLE IF NOT EXISTS state (
	id INTEGER NOT NULL,
	current_mode VARCHAR(8),
	servo_multiple INTEGER,
	active_alarms JSON,
	dht22_statistics JSON,
	mq135_statistics JSON,
	PRIMARY KEY (id)
);

INSERT INTO state
	VALUES (
		1, "Ai", 0, '[{"tmp":"asd"}]',
		'{
			"humidity_avg": 0,
			"humidity_min": 0,
			"humidity_max": 0,
			"temperature_avg": 0,
			"temperature_min": 0,
			"temperature_max": 0,
			"created_timestamp": 0
		}',
		'{
			"co2_avg": 0,
			"co2_min": 0,
			"co2_max": 0,
			"created_timestamp": 0
		}'
	)
	ON CONFLICT DO NOTHING;
