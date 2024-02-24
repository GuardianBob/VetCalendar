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
        <!-- <ProfileEdit :api_string="api_string" :user_id="user_id" :adminEdit="admin" :parentFunc01="edit_user" @done="user_updated" @close-dialog="view_user = false"/> -->
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
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import DataTable from "components/DataTable.vue"
import dummyData from "components/dummyData.json"
import { useMainStore } from "stores/main-store.js"
import { useFormFields } from "stores/form-fields.js"
import ProfileEdit from "components/ProfileEdit.vue"
import FormTest from 'src/components/FormTest.vue'
import BaseForm from 'src/components/BaseForm.vue'
// import { validators } from "app/services/ValidateService";
const mainStore = useMainStore();
const formStore = useFormFields();


export default defineComponent({
  name: "UserInfo",
  components: {
    DataTable,
    ProfileEdit,
    // FormTest,
  },
  setup() {
    return {
      // Update column headers with code from SchedSettings.vue
      columns: ref(formStore.formFields.columns),
      users: ref(dummyData.users),
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
      // columns: ref([
      //   // Replace with database columns
      //   { name: 'name', align: 'left', label: 'Name', field: 'name', sortable: true },
      //   { name: 'email', align: 'center', label: 'Email', field: 'email', sortable: true },
      //   { name: 'userGroup', align: 'center', label: 'User Group', field: 'userGroup', sortable: true },
      //   { name: 'userLevel', align: 'center', label: 'User Level', field: 'userLevel', sortable: true },
      //   { name: 'actions', label: 'Actions', field: 'actions', sortable: true },
      // ]),
      // users: ref([
      //   { id: '13', name: 'Jesse Meyer', email: 'mail@mail.com', userGroup: 'Staff', userLevel: 'Admin'}
      // ]),
      // pageTitle: ref('User Details'),
    }
  },
  data() {
    return {
      // rules: ValidateService.validators,
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
      // this.getForm = "/login/user_profile/" + userInfo.id
      // this.get_form_api = "/handle_forms"
      // this.save_form_api = "/login/user_profile"
      this.forms = ["user_basic_info", "user_address", "user_city", "user_occupation"]
      this.linked_forms = true
      this.user_id = userInfo.id
      await this.get_user_profile(userInfo.id)
      this.userInfo = userInfo
      console.log(this.api_data)
      this.view_user = true
      // Notify.create({
      //   message: `Open User Edit Window for ${user_id}`,
      //   color: "positive",
      //   position: "center",
      //   timeout: 2000
      // })
    },

    add_user() {
      // this.userInfo = []
      // this.get_form_api = "/handle_forms"
      // this.save_form_api = "/handle_forms"
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

    async get_user_profile(id) {
      this.api_string = "/login/get_user_profile"
      this.user_id = id
      this.admin = "true"
      // let req = { "id": id, "admin": "true" }
      // await APIService.get_user_profile(req).then((res) => {
      //   console.log(res.data);
      //   this.python_form = res.data
      // })
      return
    }
  },
  created() {
  },
  
  mounted() {
    // console.log(this.getCookie('d_csrfToken'))
    // mainStore.get_csrf()
    // console.log("refresh token: ", localStorage.getItem("refresh_token"))
    this.get_user_list()
    APIService.create_user().then((res) => {
      console.log(res.data)
      this.createForm = res.data.forms
      this.formOptions = res.data.options
    });
    // Update column headers with code from SchedSettings.vue
    // console.log(formStore.formFields.columns);
    const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components[componentName];
    // console.log(mainStore.getCookie('csrftoken'))
  },
})
</script>