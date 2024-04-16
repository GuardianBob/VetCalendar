<template>
  <div class="q-pa-md" style="max-width: 600px">
    <q-card flat>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
      >
        <q-tab name="totals" label="Shift Totals" />
        <q-tab name="schedule" label="Scheduling Tools" />
        <q-tab name="admin" label="Admin Tools" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="totals" class="q-pa-none">
          <DataTable :columns="columns" title="Schedule Shifts" :rowData="rowData"/>
        </q-tab-panel>

        <q-tab-panel name="schedule">
          <div class="text-h6">Scheduling Tools</div>
          <div class="col-12 q-my-sm">
            <q-btn class="q-mx-xs" color="accent" id="add_shifts" :size="button_size" @click="quick_add" icon="more_time" label="Quick Add"></q-btn>
            <q-btn class="q-mx-xs" color="secondary" id="upload" :size="button_size" @click="upload_file = true" icon="upload_file" label="Upload"></q-btn>
          </div>
        </q-tab-panel>

        <q-tab-panel name="admin">
          <div class="text-h6">Admin Tools</div>
          <div class="col-4 q-my-sm">
            <q-btn class="q-mx-xs" color="negative" id="clear_shifts" :size="button_size" @click="confirm = true" icon="cancel" label="Clear Month"></q-btn>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
    <q-dialog v-model="add_shifts" position="left" @hide="resetEventId">
      <q-card style="width: 90%" class="dialog-25">
        <component 
        :is="dynamicComponent"
        :getForm="get_form_api" 
        :submitForm="save_form_api" 
        :forms="forms"
        :item_id="event_id"
        :isSingle="true" 
        :closeButton="true" 
        page_title="Quick-Schedule" 
        @done="form_complete" 
        :form_data="editEvent" 
        :delete_button="event_edit"
        :delete_api="delete_event"
        columns="one" 
        :multiDateSelect="multiDateSelect" 
        :add_to_date="add_to_date"/>
      </q-card>
    </q-dialog>
    <q-dialog v-model="upload_file" @hide="upload_file = false">
      <div class="row justify-center items-center bg-white text-black dialog-60-nb">
        <div class="col-lg-10 col-md-10 col-sm-10 col-xs-9">
          <q-file v-model="file" label="Select File" accept=".docx, .doc" class="q-my-sm" counter>
            <!-- <q-btn class="q-ml-md q-px-sm" color="primary" size="md" flat rounded id="clear_filters_button" @click="clearFile" icon="cancel"/> -->
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
            <template v-slot:append>
              <q-icon name="cancel" color="negative" v-if="file !== null" @click="file = null" class="cursor-pointer" />
            </template>
          </q-file>
        </div>
        <div class="col-1 text-center">
          <q-btn class="q-mx-sm" size="md" color="primary" round id="upload_button" @click="file_upload" v-show="file">
            <q-icon name="upload"></q-icon>
            <q-tooltip class="bg-accent">Upload File</q-tooltip>
          </q-btn>
        </div>
      </div>
    </q-dialog>
    <q-dialog v-model="confirm" persistent>
      <ConfirmDialog 
        :doubleVerify="true"
        @confirmed="confirm_choice"
      />
    </q-dialog>
  </div>
</template>

<script>
import { ref } from 'vue'
import DataTable from 'components/DataTable.vue'
import ConfirmDialog from "components/ConfirmDialog.vue"
import ScheduleTools from 'components/ScheduleTools.vue';
import FormTest from './FormTest.vue';
import BaseForm from './BaseForm.vue';

export default {
  name: 'ScheduleTools',
  components: {
    DataTable,
    ConfirmDialog,
  },
  props: [
    "columns",
    "rowData",
    "separator",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
    "parentFunc04",
    "parentFunc05",
    "title",
  ],

  data() {
    return {
      dynamicComponent: null,
      components: {
        FormTest,
        BaseForm
      }
    }
  },

  setup () {
    return {
      tab: ref('totals'),
      splitterModel: ref(20),
      add_shifts: ref(false),
      button_size: ref('sm'),
      columnLabels: ref([]),
      updated_events: ref([]),
      editEvent: ref({}),
      event_edit: ref(false),
      event_id: ref(),
      forms: ref(['add_shift']),
      get_form_api: ref("/handle_forms"),
      save_form_api: ref("/handle_forms"),
      multiDateSelect: ref(true),
      add_to_date: ref(null),
      delete_event: ref('/delete_event'),
      upload_file: ref(false),
      file: ref(null),
      confirm: ref(false),
    }
  },

  methods: {
    quick_add() {
      this.multiDateSelect = true
      this.add_shifts = true
    },
  
  },

  created() {
    if (this.$q.platform.is.mobile) {
      this.button_size = 'md'
    }
  },

  mounted() {
    const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components[componentName];
  },
  
}
</script>