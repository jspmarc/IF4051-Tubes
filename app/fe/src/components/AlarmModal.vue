<script setup lang="ts">
import { reactive } from 'vue';
import type Alarm from '../types/Alarms';
import AppMode from '../types/AppMode';
import dayjs from 'dayjs';

const props = defineProps<{
  alarm?: Alarm;
}>();

let alarm = reactive<Alarm>({
  is_active: true,
  time: dayjs(),
  mode: AppMode.Ai,
  servo_multiple: 0
})

if (props.alarm != null) {
  alarm = props.alarm;
}

</script>


<template>
  <section class="alarm-modal">
    <div class="modal-overlay flex justify-center">
      <div class="modal p-20 rounded-3xl bg-primary-bg text-center">
        <p class="my-2 text-xl">{{ alarm.label ?? "Alarm" }}</p>
        <p class="my-2 text-base">{{ alarm.time }}</p>
        <button class="m-1 bg-gray-1" @click="$emit('close-modal')">Close</button>
        <button class="m-1 bg-active-button text-active-text">Set</button>
      </div>
    </div>
  </section>
</template>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #0000005d;
}

.modal {
  height: fit-content;
  width: fit-content;
  margin-top: 10%;
}
</style>