import { ChartData } from "chart.js";
import RealtimeData from "../types/RealtimeData";

export function getAverageAnnotation(mean?: number) {
  return mean
    ? {
        type: "line",
        borderColor: "black",
        borderDashOffset: 0,
        borderWidth: 10,
        drawTime: "beforeDatasetsDraw",
        label: {
          display: true,
          backgroundColor: "black",
          borderColor: "black",
          borderRadius: 10,
          borderWidth: 2,
          content: (ctx: any) => {
            const t: number =
              ctx.chart.options.plugins.annotation.annotations.average.value;
            return `Average for the last 15 seconds: ${t}`;
          },
          // content: "Average for the last 15 seconds",
          rotation: "auto",
        },
        scaleID: "y",
        value: mean,
        z: 10,
      }
    : undefined;
}

export function getMinimumAnnotation(min?: number) {
  return min
    ? {
        type: "line",
        borderColor: "green",
        borderDashOffset: 0,
        borderWidth: 10,
        drawTime: "beforeDatasetsDraw",
        label: {
          display: true,
          backgroundColor: "green",
          borderColor: "green",
          borderRadius: 10,
          borderWidth: 2,
          content: (ctx: any) => {
            const t: number =
              ctx.chart.options.plugins.annotation.annotations.minimum.value;
            return `Minimum for the last 15 seconds: ${t}`;
          },
          // content: "Minimum for the last 15 seconds",
          rotation: "auto",
        },
        scaleID: "y",
        value: min,
      }
    : undefined;
}

export function getMaximumAnnotation(max?: number) {
  return max
    ? {
        type: "line",
        borderColor: "red",
        borderDashOffset: 0,
        borderWidth: 10,
        drawTime: "beforeDatasetsDraw",
        label: {
          display: true,
          backgroundColor: "red",
          borderColor: "red",
          borderRadius: 10,
          borderWidth: 2,
          content: (ctx: any) => {
            const t: number =
              ctx.chart.options.plugins.annotation.annotations.maximum.value;
            return `Maximum for the last 15 seconds: ${t}`;
          },
          // content: "Maximum for the last 15 seconds",
          rotation: "auto",
        },
        scaleID: "y",
        value: max,
      }
    : undefined;
}

export function updateData(newData: RealtimeData[], dataLabel: string) {
  const labels: string[] = [];
  const data: number[] = [];
  newData.forEach((datum) => {
    const { time } = datum;
    labels.push(time.format("DD-MM-YYYY HH:mm:ss"));
    data.push(datum.value);
  });

  const chartData: ChartData<"line"> = {
    labels,
    datasets: [
      {
        label: dataLabel,
        data,
      }
    ]
  }
  return chartData;
}
