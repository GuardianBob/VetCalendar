<template>
  <q-page class="items-center flex flex-center">
    <div class="row q-mx-md full-width justify-around">
        <div class="col-6 col-xs-10 col-sm-6 col-md-6 col-lg-3 col-xl-2 q-px-lg" style="border: 4px solid #1976d2; border-radius: 10px">
          <FormTest :getForm="get_form_api" :submitForm="save_form_api" :forms="forms" :multiDateSelect="true" :page_title="page_title" @done="submitted" columns="two"/>
        </div>
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
    FormTest,
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
