<template>
  <q-page class="items-center flex-center q-my-xl">
    <DataTable :rowData="users" :columns="columns" :parentFunc01="edit_users" :title="pageTitle"/>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import DataTable from "components/DataTable.vue"
import dummyData from "components/dummyData.json"
// import { validators } from "app/services/ValidateService";

const api = APIService 

export default defineComponent({
  name: "UserInfo",
  components: {
    DataTable
  },
  setup() {
    return {
      columns: ref(dummyData.columns),
      users: ref(dummyData.users),
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
    edit_users(user_id) {
      Notify.create({
        message: `Open User Edit Window for ${user_id}`,
        color: "positive",
        position: "center",
        timeout: 2000
      })
    }
  },
  mounted() {
  },
})
</script>