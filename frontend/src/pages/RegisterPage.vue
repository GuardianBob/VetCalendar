<template>
  <q-page class="items-center flex flex-center">
    <div class="row justify-center">
      <BaseForm getForm="/login/account_request" submitForm="/login/account_request" page_title="Request Access (Broken)" @done="user_created" columns="one"/>
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
