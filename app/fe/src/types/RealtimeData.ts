import type { Dayjs } from "dayjs";

interface RealtimeData {
	time: Dayjs,
	value: number,
}

export default RealtimeData;
