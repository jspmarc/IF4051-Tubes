<script setup lang="ts">
import dayjs from "dayjs";
import Selection from "../components/Selection.vue";
import type AppState from "../types/AppState";
import AlarmCard from "./AlarmCard.vue";
import AppMode from "../types/AppMode";
import Alarm from "../types/Alarms";

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
const dummyAlarms: Alarm[] = [
  {
    time: dayjs(),
    is_active: true,
    mode: AppMode.Ai,
    servo_multiple: 0,
    label: "Anjay",
  },
  {
    time: dayjs().hour(12).minute(30),
    is_active: true,
    mode: AppMode.Ai,
    servo_multiple: 2,
    label: "Anjay",
  },
];
</script>

<template>
  <div
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[450px] text-primary-text bg-primary-bg rounded-3xl px-8 py-3"
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
    <section name="alarm-section" class="flex flex-col">
      <p class="flex self-start label py-5">Alarm(s)</p>
      <section class="flex flex-row pb-2 overflow-scroll">
        <AlarmCard v-for="alarm in dummyAlarms" :alarm="alarm" />
        <AlarmCard />
      </section>
    </section>
  </div>
</template>

<style scoped></style>
