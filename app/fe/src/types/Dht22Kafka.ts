interface Dht22Kafka {
	humidity_avg: number;
    humidity_min: number;
    humidity_max: number;
    temperature_avg: number;
    temperature_min: number;
    temperature_max: number;
    created_timestamp: number;
}

export default Dht22Kafka;
