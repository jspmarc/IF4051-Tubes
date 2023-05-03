<script setup lang="ts">
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
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[450px] px-8 py-3 bg-[#f4f4f4] rounded-3xl"
  >
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
