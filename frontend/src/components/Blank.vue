<template>
  <div class="row q-mx-md full-width justify-around ">
    <!-- Blank -->
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "Blank",
  props: [ "parentFunction" ],
  setup() {
    return {
      pageTitle: ref('User Details')
    }
  },

  watch: {
  },

  methods: {
    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    }
  },

  mounted() {
    // this.userData = this.users
  }
};
</script>


