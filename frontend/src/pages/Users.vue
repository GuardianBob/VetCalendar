<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md justify-end">
      <div class="col-10 ">
        <q-btn color="accent" dense class="q-px-sm" size="xs" label="Add" icon="add" @click="add_user()"/>
      </div>
    </div>
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_user" :title="pageTitle"/>
    <q-dialog v-model="view_user" transition-show="slide-down" transition-hide="slide-up">
      <div class="dialog-60">
        <component 
          :is="dynamicComponent" 
          :getForm="get_form_api" 
          :submitForm="save_form_api"
          delete_api="/login/delete_user"
          :forms="forms" 
          :linked_forms="linked_forms"
          :item_id="user_id"
          :closeButton="true" 
          :delete_button="true"
          :cancel_button="true"
          :doubleVerify="true"
          page_title="User Details" 
          @done="user_updated" 
          columns="two"
        />
      </div>
    </q-dialog>
    <q-dialog v-model="new_user" transition-show="slide-down" transition-hide="slide-up">  
      <div class="dialog-60">
        <component 
        :is="dynamicComponent" 
        :getForm="get_form_api" 
        :submitForm="save_form_api" 
        :forms="forms" 
        :closeButton="true" 
        page_title="Add New User" 
        @done="user_created" 
        columns="one"
      />
      </div>    
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import APIService from "../../services/api"
import DataTable from "components/DataTable.vue"
import { useFormFields } from "stores/form-fields.js"
import FormTest from 'src/components/FormTest.vue'
import BaseForm from 'src/components/BaseForm.vue'
const formStore = useFormFields();


export default defineComponent({
  name: "UserInfo",
  components: {
    DataTable,
    // FormTest,
  },
  setup() {
    return {
      // Update column headers with code from SchedSettings.vue
      columns: ref(formStore.formFields.columns),
      users: ref(),
      view_user: ref(false),
      new_user: ref(false),
      user_list: ref([]),
      user_id: ref(),
      admin: ref(),
      userInfo: ref(),
      python_form: ref(),
      api_string: ref(""),
      api_data: ref({}),
      createForm: ref({}),
      formOptions: ref({}),
      forms: ref(['add_user']),
      get_form_api: ref('/handle_forms'),
      save_form_api: ref('/handle_forms'),
      linked_forms: ref(false),
    }
  },
  data() {
    return {
      loading: false,
      dynamicComponent: null,
      components: {
        FormTest,
        BaseForm
      }
    }
  },

  watch: {
    
  },

  methods: {
    async edit_user(userInfo) {
      console.log(userInfo.id)
      this.forms = ["user_basic_info", "user_address", "user_city", "user_occupation"]
      this.linked_forms = true
      this.user_id = userInfo.id
      this.admin = "true"
      this.view_user = true
    },

    add_user() {
      this.forms = ["add_user"]
      this.linked_forms = false
      this.new_user = true
    },

    user_created() {
      this.new_user = false
      this.get_user_list()
    },

    user_updated() {
      this.view_user = false
      this.get_user_list()
    },

    async get_user_list() {
      await APIService.get_user_list().then((res) => {
        console.log(res.data);
        this.users = res.data
      })
    },
    
  },
  created() {
  },
  
  mounted() {
    this.get_user_list()
    const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components[componentName];
  },
})
</script>