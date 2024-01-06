<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md justify-end">
      <div class="col-10 ">
        <q-btn color="accent" dense class="q-px-sm" size="xs" label="Add" icon="add" @click="add_user()"/>
      </div>
    </div>
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_user" :title="pageTitle"/>
    <q-dialog v-model="view_user" transition-show="slide-down" transition-hide="slide-up">
      <ProfileView :userInfo="userInfo" :parentFunc01="update_user" editButton="Edit User" page_title="User Details"/>
    </q-dialog>
    <q-dialog v-model="new_user" transition-show="slide-down" transition-hide="slide-up">
      <ProfileView :userInfo="userInfo" :parentFunc01="add_user" editButton="Add User" page_title="Add User" />
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
import ProfileView from "components/ProfileView.vue"
// import { validators } from "app/services/ValidateService";
const mainStore = useMainStore();
const api = APIService 
const formStore = useFormFields();

export default defineComponent({
  name: "UserInfo",
  components: {
    DataTable,
    ProfileView
  },
  setup() {
    return {
      columns: ref(formStore.formFields.columns),
      users: ref(dummyData.users),
      view_user: ref(false),
      new_user: ref(false),
      user_list: ref([]),
      user_id: ref(),
      userInfo: ref(),
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
      pageTitle: ref('User Details'),
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
      await this.get_user_profile(userInfo.id)
      // this.userInfo = userInfo
      this.view_user = true
      // Notify.create({
      //   message: `Open User Edit Window for ${user_id}`,
      //   color: "positive",
      //   position: "center",
      //   timeout: 2000
      // })
    },

    add_user() {
      this.userInfo = []
      this.new_user = true
    },

    update_user(userInfo) {

    },

    async get_user_list() {
      await APIService.get_user_list().then((res) => {
        console.log(res.data);
        this.users = res.data
      })
    },

    async get_user_profile(id) {
      await APIService.get_user_profile(id).then((res) => {
        console.log(res.data);
        this.userInfo = res.data
      })
      return
    }
  },
  created() {
  },
  
  mounted() {
    // console.log(this.getCookie('d_csrfToken'))
    // mainStore.get_csrf()
    this.get_user_list()
    console.log(formStore.formFields.columns);
    // console.log(mainStore.getCookie('csrftoken'))
  },
})
</script>