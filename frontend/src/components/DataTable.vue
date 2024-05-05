<template>
  <div class="row q-mx-md full-width justify-around ">
    <div class="col-12 text-center text-body1 text-weight-medium" style="font-size:20px">{{ title }}</div>
    <q-table
      :rows="rowData"
      :columns="columns"
      row-key="name"
      class="col-10"
      flat
      :separator="separator"
      :rows-per-page-options="[10,20,50,0]"
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
            <q-btn v-if="managerPriv" color="positive" dense class="q-px-sm q-mx-xs" size="xs" label="" icon="edit" @click="editBtn(props.row)">
              <q-tooltip class="bg-accent" anchor="bottom middle">Edit User Info</q-tooltip>
            </q-btn>
            <q-btn v-if="managerPriv" color="warning" dense class="q-px-sm q-mx-xs" size="xs" label="" icon="lock_reset" @click="reset_button(props.row)">
              <q-tooltip class="bg-accent" anchor="bottom middle">Reset User Password</q-tooltip>
            </q-btn>
          </div>
          <div>
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
  props: [
    "columns",
    "rowData",
    "separator",
    "managerPriv",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
    "parentFunc04",
    "parentFunc05",
    "title"
  ],
  setup() {
    return {
      info: ref(false),
      userData: ref([]),
      pageTitle: ref(''),   
    }
  },

  watch: {
  },

  methods: {
    editBtn(data) {
      this.parentFunc01(data)
    },
    reset_button(data) {
      console.log(data)
      this.parentFunc02(data)
    },    
  },

  mounted() {
    // this.userData = this.rowData
    this.pageTitle = this.title
  }
};
</script>


