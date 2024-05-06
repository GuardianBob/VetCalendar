<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md justify-end">
      <div class="col-10 ">
        <q-btn v-if="addUserPriv" color="accent" dense class="q-px-sm" size="xs" label="Add" icon="add" @click="add_user()"/>
      </div>
    </div>
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_user" :parentFunc02="reset_password_show" :title="pageTitle" :managerPriv="editUserPriv"/>
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
    <q-dialog v-model="reset_pass_form" transition-show="slide-down" transition-hide="slide-up" @hide="reset_pass_form = false, verify_reset = false">
      <div class="dialog-60">
        <div class="row justify-center  q-mb-lg">
          <div class="col-12 text-center">
            <h3 class="text-primary">Reset Password</h3>
          </div>
          <div class="col-12 text-center ">
            <span class="text-h5">Are you sure you want to reset the password for {{ reset_pass_email }}?</span>
            <q-toggle
              v-model="verify_reset"
              color="red"
              checked-icon="check"
              unchecked-icon="clear"
            />
            <span v-if="!verify_reset" class="text-red-10 text-h6">Please confirm password reset</span>
            <span v-if="verify_reset" class="text-red-10 text-h6">Reset confirmed</span>
          </div>
          <q-btn :disable="!verify_reset" color="red" label="Reset Password" @click="reset_password" />
        </div>
      </div>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import APIService from "../../services/api"
import DataTable from "components/DataTable.vue"
import { useFormFields } from "stores/form-fields.js"
import FormTest from 'src/components/FormTest.vue'
import BaseForm from 'src/components/BaseForm.vue'
import { useMainStore } from 'src/stores/main-store'
import { Notify } from 'quasar'
const formStore = useFormFields();
const mainStore = useMainStore();

export default defineComponent({
  name: "UserInfo",
  props: [
  ],
  components: {
    DataTable,
    // FormTest,
  },
  setup() {

    // ===================== Watch for permissions update in Pinia store =====================
    // This allows the page permissions to be updated if the user reloads the page
    // This won't work if the user navigates away from teh page then back to the page
    const managerPriv = ref(mainStore.checkPermissions(["Edit User", "Add User", "Delete User"]))
    const addUserPriv = ref(mainStore.checkPermissions(["Add User"]))
    const editUserPriv = ref(mainStore.checkPermissions(["Edit User"]))
  
    // watch(() => mainStore.permissions, () => {
    //   managerPriv.value = mainStore.checkPermissions(["Edit User", "Add User", "Delete User"])
    //   addUserPriv.value = mainStore.checkPermissions(["Add User"])
    //   editUserPriv.value = mainStore.checkPermissions(["Edit User"])
    // })
    // ========================================================================================

    return {
      // Update column headers with code from SchedSettings.vue
      columns: ref(formStore.formFields.columns),
      users: ref(),
      view_user: ref(false),
      new_user: ref(false),
      user_list: ref([]),
      user_id: ref(),
      managerPriv,
      addUserPriv,
      editUserPriv,
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
      reset_pass_form: ref(false),
      reset_pass_email: ref(""),
      verify_reset: ref(false),
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
      // this.admin = "true"
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

    reset_password_show(userInfo) {
      console.log(userInfo.email)
      this.reset_pass_email = userInfo.email
      this.reset_pass_form = true
      // this.forms = ["password_reset"]
      // this.linked_forms = false
      // // this.admin = true
      // this.user_id = userInfo.id
      // this.form_title = "Reset User Password"
      // this.okBtnName = "Reset"
      // this.new_user = true
    },

    reset_password() {
      console.log("Resetting password \n", this.reset_pass_email)
      APIService.reset_password({"email": this.reset_pass_email}).then((res) => {
        console.log(res)
        Notify.create({
          message: "Password reset successfully",
          color: "green",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
        this.reset_pass_form = false
        this.verify_reset = false
      })
      .catch(error => {
        console.log(error)
        Notify.create({
          message: error.response.data.message,
          color: "red",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
      })
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
    // ================= Update permissions for the page =================
    // This is needed to update the permissions for the page when the user navigates to the page
    // This will not work on a page reload. 
    // this.managerPriv = mainStore.checkAccess("Manager")
    // this.addUserPriv = mainStore.checkPermissions(["Add User"])
    // this.editUserPriv = mainStore.checkPermissions(["Edit User"])
    // ==================================================================
    this.get_user_list()
    const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components[componentName];
  },
    
})
</script>