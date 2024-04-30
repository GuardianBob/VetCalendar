<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md justify-end">
      <div class="col-10 ">
        <q-btn color="accent" dense class="q-px-sm" size="xs" label="Add" icon="add" @click="add_user()"/>
      </div>
    </div>
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_user" :parentFunc02="reset_password" :title="pageTitle"/>
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
          okButtonName="Update"
          :page_title="form_title" 
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
        :item_id="user_id"
        :okButtonName="okBtnName"
        :page_title="form_title" 
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
      form_title: ref(""),
      okBtnName: ref("Add"),
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
      this.forms = ["user_basic_info", "user_address", "user_city", "user_occupation", "user_level"]
      this.linked_forms = true
      this.user_id = userInfo.id
      this.admin = "true"
      this.form_title = "User Details"
      this.view_user = true
    },

    add_user() {
      this.forms = ["add_user"]
      this.linked_forms = false
      this.user_id = null
      this.form_title = "Add New User"
      this.okBtnName = "Add"
      this.new_user = true
    },

    reset_password(userInfo) {
      this.forms = ["password_reset"]
      this.linked_forms = false
      this.admin = true
      this.user_id = userInfo.id
      this.form_title = "Reset User Password"
      this.okBtnName = "Reset"
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