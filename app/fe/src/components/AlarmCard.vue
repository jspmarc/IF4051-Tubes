<script setup lang="ts">
import { Ref, ref } from 'vue';
import type Alarm from '../types/Alarms';
import AppMode from '../types/AppMode';
import AlarmModal from './AlarmModal.vue';

const props = defineProps<{
  alarm?: Alarm;
}>();

const showModal: Ref<Boolean> = ref(false);

let alarmDisplay = {
  time: props.alarm?.time.format("HH:mm"),
  info: "+"
}

function setAlarmDisplay() {
  // set info to be displayed
  if (props.alarm?.mode == AppMode.Ai) {
    alarmDisplay.info = "Auto"
  } else {
    switch (props.alarm?.servo_multiple) {
      case 0:
        alarmDisplay.info = "Closed"
        break;
      case 1:
        alarmDisplay.info = "Half Open"
        break;
      case 2:
        alarmDisplay.info = "Open"
        break;
      default:
        alarmDisplay.info = "+"
        break;
    }
  }
}
setAlarmDisplay();
</script>


<template>
  <button 
    type="button"
    class="alarm-card flex flex-col self-center bg-gray-1 p-4 rounded-lg mx-1"
    @click="showModal = true"
    >
    <div class="" v-if="props.alarm != null">
      <p class="text-xl font-normal">{{ alarmDisplay.time }}</p>
      <p class="text-sm font-extralight">{{ alarmDisplay.info }}</p>
    </div>
    <div class="" v-else>
      <p class="text-5xl font-extralight px-2">{{ alarmDisplay.info }}</p>
    </div>
  </button>
  <AlarmModal v-show="showModal" @close-modal="showModal = false" :alarm="props.alarm"/>
</template>