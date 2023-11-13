<template>
  <div class="row q-mx-md full-width justify-around ">
    <q-table
      title="Users"
      :rows="users"
      :columns="columns"
      row-key="name"
      class="col-10"
      flat
    >
      <!-- Remove "Actions" column from "columns" in setup to hide "Actions" column -->
      <template v-slot:header-cell-actions="props" >
        <q-th :props="props">
          Actions
        </q-th>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <div>
            <q-btn color="positive" dense class="q-px-sm" size="xs" label="Edit" icon="edit" @click="editBtn(props.row.id)"/>
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "DataTable",
  props: [ "columns", "users", "parentEdit" ],
  setup() {
    return {
      info: ref(false),
      userData: ref([]),
      pageTitle: ref('User Details')
    }
  },

  watch: {
  },

  methods: {
    editBtn(data) {
      this.parentEdit(data)
    }
  },

  mounted() {
    // this.userData = this.users
  }
};
</script>


