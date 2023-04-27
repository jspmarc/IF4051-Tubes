<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import slugify from 'slugify'

/**
 * Selection component properties
 * @interface SelectionProps
 * @member {string[]} options options to store/send value
 * @member {string[]} [optionsDisplay] options to display, if not set: use options
 * @member {string} [label] label to display, if not set: only display options
 * @member {string} [url] url to send request to, if not set: do nothing
 * @member {string} [propertyName] property name to send to server, if not set: use slugified label
 * @example 
 * <Selection label="Mode"
 *            :optionsDisplay="['Auto', 'Override']"
 *            :options="['ai', 'override']"
 *            :url="`localhost:8080/mode`"
 *            propertyName="current_mode" />
 */
interface SelectionProps {
  options: string[],
  optionsDisplay?: string[],
  label?: string,
  url?: string,
  propertyName?: string
}

const props = defineProps<SelectionProps>();
const state = reactive({ 
  selectedIdx: 0, 
  protocol: '' 
});
let wsConnection: WebSocket;

function defineProtocol() {
  if (props.url == null) {
    console.error('url is not set')
    return;
  }
  const protocol = props.url!.split(':')[0]
  switch (protocol) {
    case "http":
    case "https":
      state.protocol = 'rest';
      break;
    case "ws":
    case "wss":
      state.protocol = 'websocket';
      wsConnection = new WebSocket(props.url!);
      break;
    default:
      console.debug(`protocol ${protocol} not supported`)
      break;
  }
}

async function setupInitState() {
  // functions
  async function getCurrentState() {
    const propertyName = props.propertyName ?? slugify(props.label!)
    const response = await fetch(props.url!, {
      method: 'GET'
    })
    response.json().then((data: any) => {
      setSelectedIdx({ option: data[propertyName].toString(), options: props.options })
    })
  }

  function setupWebsocket() {
    const propertyName = props.propertyName ?? slugify(props.label!)
    wsConnection.onmessage = (event) => {
      let data = JSON.parse(event.data);
      setSelectedIdx({ option: data[propertyName].toString(), options: props.options })
    }
  }

  // main logic
  switch (state.protocol) {
    case 'rest':
      await getCurrentState();
      break;
    case 'websocket':
      setupWebsocket();
      break;
    default:
      break;
  }
}

onMounted(async () => {
  // do some props validation
  if (props.url != null && props.label == null && props.propertyName == null) {
    console.warn('url is set but no propertyName or label set')
  }
  if (props.optionsDisplay != null && props.optionsDisplay.length != props.options.length) {
    console.error('optionsDisplay and options are not the same length')
  }

  defineProtocol();
  await setupInitState();
})

/**
 * set `state.selectedIdx` based on option or index; the index takes precedence
 * @param option option to set as selected
 * @param index index of option to set as selected
 * @returns void
 */
function setSelectedIdx({index, option, options}: {index?: number, option?: string, options?: string[]}) {
  // guards
  if (index != null && option != null) {
    console.warn('both index and option are set, index takes precedence')
  }
  if (index != null && options != null) {
    console.warn('index is set and options is set, index will be used')
  }
  if (index == null && option == null) {
    console.error('neither index nor option is set')
    return
  }
  if (option != null && options == null) {
    console.error('option is set but options is not set')
    return
  }

  // main logic
  if (index != null) {
    state.selectedIdx = index
    return
  } 
  
  if (option != null && options != null) {
    state.selectedIdx = options.indexOf(option)
    return
  }
}

function sendData(selectedIdx: number) {
  // functions
  function sendRestData(value: string, propertyName: string) {
    fetch(props.url!, { 
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify({ [propertyName]: value })
    })
  }

  function sendWebsocketData(value: string, propertyName: string) {
    wsConnection.send(JSON.stringify({ [propertyName]: value }))
  }

  // main logic
  setSelectedIdx({ index: selectedIdx })
  let value = props.options[selectedIdx]
  let propertyName = props.propertyName ?? slugify(props.label!) // use slugified label if propertyName is not set

  switch (state.protocol) {
    case 'rest':
      sendRestData(value, propertyName)
      break;
    case 'websocket':
      sendWebsocketData(value, propertyName)
      break;
    default:
      break;
  }
}
</script>

<template>
  <div class="selection flex flex-row justify-between items-center">
    <div class="label" v-if="label != null">
      {{ label }}
    </div>
    <div class="selection gray-1 rounded-full p-1">
      <button type="button" class="rounded-full py-1" 
              v-for="(option, index) in optionsDisplay" 
              :class="{'blue': state.selectedIdx == index}" 
              @click="sendData(index)">
        {{ option }}
      </button>
    </div>
  </div>
</template>

<style scoped>
/* kalau pengen dibikin bagus silakan hehe */
button {
  transition: all 0.3s ease-in-out;
}
</style>
