<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
import type { Ref } from "vue";

export default defineComponent({
  props: {
    title: {
      type: String as PropType<string>,
      required: true,
    },
    body: {
      type: String as PropType<string>,
      required: true,
    },
    isRecommending: {
      type: Boolean as PropType<boolean>,
      required: true,
    },
  },
  setup(props) {
    return {
      title: props.title,
      body: props.body,
      isRecommending: props.isRecommending,
      isDismissed: isDismissed,
    };
  },
});

const isDismissed: Ref<boolean> = ref(false);
</script>

<template>
  <div
    v-if="isRecommending && !isDismissed"
    class="flex flex-col lg:w-2/6 md:w-3/6 sm:w-4/6 w-full mx-auto min-w-[450px] px-8 py-3 bg-primary-bg rounded-3xl mb-6 items-start"
  >
    <p class="font-semibold text-xl">{{ title }}</p>
    <p class="text-base">{{ body }}</p>

    <div class="flex ml-auto gap-[10px]">
      <button
        class="bg-secondary-button text-primary-text"
        @click="() => (isDismissed = true)"
      >
        Dismiss
      </button>
      <button class="bg-active-button text-active-text">Read more</button>
    </div>
  </div>
</template>

<style scoped>
button {
  padding: 8px 24px;
  height: 32px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 14px;
  line-height: 14px;
}
</style>
