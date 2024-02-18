<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <FormTest :getForm="get_form_api" :multiDateSelect="true" :submitForm="save_form_api" :closeButton="true" page_title="Build Form" @done="submitted" columns="one"/>
      <!-- </q-dialog> -->
    </div>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import FormTest from 'components/FormTest.vue'
import APIService from "../../services/api";

export default defineComponent({
  name: "FormsPage",
  components: {
    // vue linter no use error bypass

    // Forms,
    FormTest,
  },
  data() {
    return {
    }
  },
  setup() {    
    return {
      show: ref(true),
      get_form_api: ref("/get_formbuilder_form/add_shift"),
      save_form_api: ref("/get_formbuilder_form"),
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
    // APIService.get_formbuilder_form().then((response) => {
    //   console.log(response);
    // });
  },

})
</script>
