<template>
  <div class="row q-mx-md full-width justify-around ">
    <div class="col-12 text-center text-body1 text-weight-medium" style="font-size:20px">{{ title }}</div>
    <q-table
      :rows="rowData"
      :columns="columns"
      row-key="name"
      class="col-10"
      flat
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
  props: [
    "columns",
    "rowData",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
    "parentFunc04",
    "parentFunc05",
    "title"],
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
    }
  },

  mounted() {
    // this.userData = this.rowData
    this.pageTitle = this.title
  }
};
</script>


