import type Alarm from "./Alarms";
import type AppMode from "./AppMode";
import type Dht22Kafka from "./Dht22Kafka";
import type Mq135Kafka from "./Mq135Kafka";

interface AppState {
	current_mode: AppMode;
	servo_multiple: number;
	active_alarms: Alarm[];
	dht22_statistics: Dht22Kafka;
	mq135_statistics: Mq135Kafka;
}

export default AppState;
