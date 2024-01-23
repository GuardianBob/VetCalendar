<template>
  <!-- <q-page class="q-pt-xl"> -->
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <Forms />
      <!-- </q-dialog> -->
    </div>
  <!-- </q-page> -->
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import Forms from 'components/Forms.vue'

export default defineComponent({
  name: "FormsPage",
  components: {
    Forms
  },
  data() {
    return {
    }
  },
  setup() {    
    return {
      show: ref(true),
    };
  },
  watch: {
    
  },
  computed: {

  },
  methods: {
    
  },

  created() {
  },
  
  mounted() {
    
  },

})
</script>
