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

const props = defineProps<SelectionProps>()
const state = reactive({ selectedIdx: 0 })

onMounted(async () => {
  // do some props validation
  if (props.url != null && props.label == null && props.propertyName == null) {
    console.warn('url is set but no propertyName or label set')
  }
  if (props.optionsDisplay != null && props.optionsDisplay.length != props.options.length) {
    console.error('optionsDisplay and options are not the same length')
  }

  // get current state from backend
  if (props.url != null) {
    let propertyName = props.propertyName ?? slugify(props.label!)
    const response = await fetch(props.url!, {
      method: 'GET'
    })
    response.json().then((data: any) => {
      setSelectedIdx({ option: data[propertyName].toString(), options: props.options })
    })
  }
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
  setSelectedIdx({ index: selectedIdx })
  let value = props.options[selectedIdx]
  let propertyName = props.propertyName ?? slugify(props.label!) // use slugified label if propertyName is not set
  fetch(props.url!, { 
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify({ [propertyName]: value })
  })
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
