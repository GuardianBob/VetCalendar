<template>
  <div >
    <i class="material-icons q-py-xs flat" style="font-size: 1.8em;">{{ icon }} </i>
    <span id="date_picker_button" style="font-size: 1.2em; margin-left: 10px;">{{ text }}</span>
  </div>
  <!-- <div> -->
    <!-- <q-btn color="primary" round :size="button_size" id="enable_date" @click="enable_date = !enable_date"
            icon="event">X</q-btn> -->
    
    <!-- <i class="fa-regular fa-calendar" size="mx-1">{{ icon }}</i> -->
  <!-- </div> -->
</template>

<script>
export default {
  props: ['icon', 'text'],
}
</script>