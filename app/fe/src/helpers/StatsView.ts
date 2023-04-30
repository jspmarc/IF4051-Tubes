import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import type RawRealtimeData from "../types/RawRealtimeData";
import type RealtimeData from "../types/RealtimeData";

dayjs.extend(utc);

export async function getRealtimeData(
  beUrl: string,
  data: "all" | "temp" | "co2"
) {
  let url = `${beUrl}/realtime-data?time_range=-30s`;
  if (data == "all") {
    url += "&data=co2&data=temperature";
  } else if (data == "temp") {
    url += "&data=temperature";
  } else if (data == "co2") {
    url += "&data=co2";
  }
  const rawRealtimeData: {
    humidity?: RawRealtimeData[];
    temperature?: RawRealtimeData[];
    co2?: RawRealtimeData[];
  } = await (await fetch(url)).json();

  const realtimeData: {
    humidity?: RealtimeData[];
    temperature?: RealtimeData[];
    co2?: RealtimeData[];
  } = {};

  for (const key in rawRealtimeData) {
    if (key !== "humidity" && key !== "temperature" && key !== "co2") {
      continue;
    }

    const data = rawRealtimeData[key];
    if (!data) {
      continue;
    }

    realtimeData[key] = data.map((datum) => {
      const time = dayjs.utc(datum[0]).local();

      return {
        time,
        value: datum[1],
      };
    });
  }

  return realtimeData;
}
