<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <div class="col-6">
          <component 
            :is="dynamicComponent" 
            :getForm="get_form_api" 
            :submitForm="save_form_api" 
            :item_id="item_id"
            :forms="forms" 
            :linked_forms="linked_forms"
            :multiDateSelect="true" 
            :closeButton="true" 
            :doubleVerify="true"
            :page_title="page_title" 
            :cancel_button="true"
            :delete_button="true"
            okButtonName="Send"
            @done="submitted" 
            columns="one"/>
        </div>
      <!-- </q-dialog> -->
    </div>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import APIService from "../../services/api";
import FormTest from 'components/FormTest.vue';
import BaseForm from 'components/BaseForm.vue';

export default defineComponent({
  name: "FormsPage",
  props: [
    'api_route',
    'page_title',
    'forms',
    'get_form_api',
    'save_form_api',
  ],
  components: {
    // vue linter no use error bypass

    // Forms,
    // FormTest,
  },
  data() {
    return {
      dynamicComponent: null,
      components: {
        FormTest,
        BaseForm
      }
    }
  },
  setup() {    
    return {
      show: ref(true),
      // page_title: ref("Form Test"),
      // item_id: ref(9),
      // forms: ref(['access_settings']),
      // forms: ref(['user_basic_info', 'user_address', 'user_city', 'user_occupation']),
      // forms: ref(['user_basic_info', 'user_address']),     
      // forms: ref(['add_user']),
      // forms: ref(['add_shift']),
      // forms: ref(['user_profile']),
      // get_form_api: ref("/handle_forms"),
      // get_form_api: ref("/login/request_access"),
      // save_form_api: ref("/handle_forms"),
      linked_forms: ref(true),
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
    // const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components['FormTest'];
    // APIService.get_formbuilder_form().then((response) => {
    //   console.log(response);
    // });
  },

})
</script>
