<script setup lang="ts">
import { onMounted, reactive, watch } from "vue";
import slugify from "slugify";
import type AppState from "../types/AppState";
/**
 * Selection component properties
 * @type SelectionProps
 * @member {string[]} options options to store/send value
 * @member {string[]} [optionsDisplay] options to display, if not set: use options
 * @member {string} [label] label to display, if not set: only display options
 * @member {string} [url] url to send request to, if not set: do nothing
 * @member {WebSocket} [wsConnection] websocket connection to listen to, if not set: do nothing
 * @member {string} [propertyName] property name to send to server, if not set: use slugified label
 * @example
 * <Selection label="Mode"
 *            :optionsDisplay="['Auto', 'Override']"
 *            :options="['ai', 'override']"
 *            :url="`http://localhost:8080/mode`"
 *            :wsConnection="`WebSocket()`"
 *            propertyName="current_mode" />
 */
interface SelectionProps {
  options: string[];
  optionsDisplay?: string[];
  label?: string;
  url?: string;
  wsConnection?: WebSocket;
  propertyName: "current_mode" | "servo_multiple";
  appState: AppState;
}

const props = defineProps<SelectionProps>();
const state = reactive({
  selectedIdx: 0,
  protocol: "",
});

watch(
  () => props.appState,
  function (newState) {
    const propertyName = props.propertyName ?? slugify(props.label!);
    setSelectedIdx({
      option: newState[propertyName].toString(),
      options: props.options,
    });
  }
);

onMounted(async () => {
  // do some props validation
  if (props.url != null && props.label == null && props.propertyName == null) {
    console.warn("url is set but no propertyName or label set");
  }
  if (
    props.optionsDisplay != null &&
    props.optionsDisplay.length != props.options.length
  ) {
    console.error("optionsDisplay and options are not the same length");
  }
});

/**
 * set `state.selectedIdx` based on option or index; the index takes precedence
 * @param option option to set as selected
 * @param index index of option to set as selected
 * @returns void
 */
function setSelectedIdx({
  index,
  option,
  options,
}: {
  index?: number;
  option?: string;
  options?: string[];
}) {
  // guards
  if (index != null && option != null) {
    console.warn("both index and option are set, index takes precedence");
  }
  if (index != null && options != null) {
    console.warn("index is set and options is set, index will be used");
  }
  if (index == null && option == null) {
    console.error("neither index nor option is set");
    return;
  }
  if (option != null && options == null) {
    console.error("option is set but options is not set");
    return;
  }

  // main logic
  if (index != null) {
    state.selectedIdx = index;
    return;
  }

  if (option != null && options != null) {
    state.selectedIdx = options.indexOf(option);
    return;
  }
}

/**
 * Sending data to server: only via REST for now
 */
async function sendData(selectedIdx: number) {
  if (props.url != null) {
    const propertyName = props.propertyName ?? slugify(props.label!); // use slugified label if propertyName is not set
    const value = props.options[selectedIdx];
    const response = await fetch(props.url!, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ [propertyName]: value }),
    });
    if (!response.ok) {
      console.error(
        "Can't update state to server, response:",
        response.statusText
      );
    }
    setSelectedIdx({ index: selectedIdx });
  } else {
    console.debug("wsUrl and url are not set, will not send data");
  }
}
</script>

<template>
  <div class="selection flex flex-row justify-between items-center">
    <div class="label" v-if="label != null">
      {{ label }}
    </div>
     <div class="selection bg-gray-1 rounded-full p-2 gap-3 flex">
      <button
        type="button"
        class="rounded-full py-1"
        v-for="(option, index) in optionsDisplay"
        :class="{ 'bg-blue text-active-text': state.selectedIdx === index }"
        @click="sendData(index)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.label {
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 24px;
}
</style>
