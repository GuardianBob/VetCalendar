<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <BaseForm :getForm="get_form_api" :submitForm="save_form_api" :closeButton="true" page_title="Add New Form" @done="submitted" columns="one"/>
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
      get_form_api: ref("/add_edit_form"),
      save_form_api: ref("/add_edit_form"),
    };
  },
  watch: {
    
  },
  computed: {

  },
  methods: {
    submitted(){
    },
  },

  created() {
  },
  
  mounted() {
    
  },

})
</script>
