<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <div class="col-6">
          <FormTest :getForm="get_form_api" :submitForm="save_form_api" :forms="forms" :multiDateSelect="true" :closeButton="true" page_title="Build Form" @done="submitted" columns="one"/>
        </div>
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
      forms: ref(['user_basic_info', 'user_address', 'user_city', 'user_occupation']),
      // forms: ref(['user_basic_info', 'user_address']),     
      // forms: ref(['add_user']),
      // forms: ref(['add_shift']),
      get_form_api: ref("/handle_forms"),
      save_form_api: ref("/handle_forms"),
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
