import { Ref } from "vue";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import type RawRealtimeData from "../types/RawRealtimeData";
import type RealtimeData from "../types/RealtimeData";

dayjs.extend(utc)

export async function getRealtimeData(
  realtimeData: Ref<{
    humidity?: RealtimeData[];
    temperature?: RealtimeData[];
    co2?: RealtimeData[];
  }>,
  beUrl: string,
) {
  const rawRealtimeData: {
    humidity?: RawRealtimeData[];
    temperature?: RawRealtimeData[];
    co2?: RawRealtimeData[];
  } = await(
    await fetch(
      `${beUrl}/realtime-data?time_range=-30s&data=temperature&data=co2`
    )
  ).json();

  for (const key in rawRealtimeData) {
    if (key !== "humidity" && key !== "temperature" && key !== "co2") {
      continue;
    }

    const data = rawRealtimeData[key];
    if (!data) {
      continue;
    }

    realtimeData.value[key] = data.map((datum) => {
      const time = dayjs.utc(datum[0]).local();

      return {
        time,
        value: datum[1],
      };
    });
  }

  return realtimeData;
}
