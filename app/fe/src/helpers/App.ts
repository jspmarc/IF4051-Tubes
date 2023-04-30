export async function getCurrentState() {
  const propertyName = props.propertyName ?? slugify(props.label!);
  console.log(props.url!);
  const response = await fetch(props.url!);
  if (!response.ok) {
    console.error("Can't get data from fetch api, response:", response.statusText);
    return;
  }
  const data = await response.json()
  setSelectedIdx({
    option: data[propertyName].toString(),
    options: props.options,
  });
}
