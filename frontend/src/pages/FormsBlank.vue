<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <BaseForm getForm="/quick_add" submitForm="/quick_add" :isSingle="true" :closeButton="true" page_title="Quick-Schedule" @done="user_created"/>
      <!-- </q-dialog> -->
    </div>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import BaseForm from 'components/BaseForm.vue'

export default defineComponent({
  name: "FormsPage",
  components: {
    // vue linter no use error bypass

    // Forms,
    BaseForm,
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
