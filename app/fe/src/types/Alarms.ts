import type { Dayjs } from "dayjs";
import AppMode from "./AppMode";

interface Alarm {
	time: Dayjs;
	is_active: boolean;
	servo_multiple: number;
	mode: AppMode;
	label?: string;
}

export default Alarm;
