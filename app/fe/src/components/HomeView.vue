<script setup lang="ts">
import dayjs from "dayjs";
import Selection from "../components/Selection.vue";
import type AppState from "../types/AppState";

/**
 * HomeView component properties
 * @interface HomeViewProps
 * @member {string} [url] url to send request to, if not set: do nothing
 * @member {WebSocket} [wsConnection] websocket connection to listen to, if not set: do nothing
 */
interface HomeViewProps {
  url?: string;
  wsConnection?: WebSocket;
  appState: AppState;
}

const props = defineProps<HomeViewProps>();
</script>

<template>
  <div class="flex flex-col lg:w-3/6 md:w-4/6 sm:w-5/6 w-full mx-auto text-primary-text bg-white rounded-lg px-20 py-5">
    <!-- Mode -->
    <Selection
      class="py-2"
      label="Mode"
      :options-display="['Auto', 'Override']"
      :options="['Ai', 'Override']"
      :url="`${props.url}/mode`"
      property-name="current_mode"
      :app-state="appState"
    />
    <!-- Door - Servo -->
    <Selection
      class="py-2"
      label="Door"
      :options-display="['Open', 'Close']"
      :options="['2', '0']"
      :url="`${props.url}/servo`"
      property-name="servo_multiple"
      :app-state="appState"
    />
    <!-- Window - Servo -->
    <Selection
      class="py-2"
      label="Window"
      :options-display="['Open', 'Close']"
      :options="['2', '0']"
      :url="`${props.url}/servo`"
      property-name="servo_multiple"
      :app-state="appState"
    />
  </div>
</template>

<style scoped></style>
