import { getPassword } from "./password";

export async function getAlerts(beUrl: string, timeRange: string) {
  let url = `${beUrl}/alert?time_range=-${timeRange}`;

  const password = getPassword();
  const xTokenHeader = password
    ? {
        "X-Token": password,
      }
    : null;

  const alerts = await (
    await fetch(`${url}`, {
      //   headers: { ...xTokenHeader },
    })
  ).json();

  return alerts.reverse();
}
