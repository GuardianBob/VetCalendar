<template>
  <div >
    <i class="material-icons q-py-xs flat" style="font-size: 1.8em;">{{ icon }} </i>
    <span id="date_picker_button" style="font-size: 1.2em; margin-left: 10px;">{{ text }}</span>
  </div>
</template>

<script>
export default {
  props: ['icon', 'text'],
}
</script>