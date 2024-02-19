<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md justify-end">
      <div class="col-10 ">
        <q-btn color="accent" dense class="q-px-sm" size="xs" label="Add" icon="add" @click="add_user()"/>
      </div>
    </div>
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_user" :title="pageTitle"/>
    <q-dialog v-model="view_user" transition-show="slide-down" transition-hide="slide-up">
      <ProfileEdit :api_string="api_string" :user_id="user_id" :adminEdit="admin" :parentFunc01="edit_user" @done="user_updated" @close-dialog="view_user = false"/>
    </q-dialog>
    <q-dialog v-model="new_user" transition-show="slide-down" transition-hide="slide-up">  
      <div class="dialog-60">
        <BaseForm :getForm="get_form_api" :submitForm="save_form_api" :closeButton="true" page_title="Add New User" @done="user_created" columns="one"/>
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
import BaseForm from 'src/components/BaseForm.vue'
// import { validators } from "app/services/ValidateService";
const mainStore = useMainStore();
const formStore = useFormFields();


export default defineComponent({
  name: "UserInfo",
  components: {
    DataTable,
    ProfileEdit,
    BaseForm,
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
      get_form_api: ref('/get_formbuilder_form/add_user'),
      save_form_api: ref('/get_formbuilder_form'),
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
    }
  },

  watch: {
    
  },

  methods: {
    async edit_user(userInfo) {
      console.log(userInfo.id)
      this.getForm = "/login/user_profile/" + userInfo.id
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
    console.log(formStore.formFields.columns);
    // console.log(mainStore.getCookie('csrftoken'))
  },
})
</script>