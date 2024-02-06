<template>
  <q-page class="q-pt-xl">
      <!-- <div class="row align-start justify-end q-mx-sm items-center">
        <div class="col-xs-8 col-lg-10 col-md-10 col-sm-10 q-mr-xl">
          
        </div>
      </div>
      <br> -->
      <!-- <q-spinner v-show="loading" color="primary" size="3em" :thickness="3" /> -->
        <Calendar />
    <!-- <Forms :form_data="form_data" :option_data="option_data" /> -->
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import Calendar from 'components/Calendar.vue'
import Forms from 'components/Forms.vue'
import MainFunctions from '../../services/MainFunctions'

export default defineComponent({
  name: "IndexPage",
  components: {
    // eslint-disable-next-line vue/no-unused-components
    Calendar,
    // eslint-disable-next-line vue/no-unused-components
    Forms
  },
  data() {
    return {
    }
  },
  setup() {
    
    return {
    };
  },
  watch: {
    
  },
  computed: {

  },
  methods: {
    
  },
  
  mounted() {
    
  },

})
</script>
