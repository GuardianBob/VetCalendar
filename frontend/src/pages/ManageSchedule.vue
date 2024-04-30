<template>
  <q-page class="q-pt-xl" >
    <div class="row align-start justify-center q-mx-sm ">
      <div class="col-4 col-xs-11 col-sm-4 col-md-4 col-lg-4 q-pl-sm">
        <q-card flat>
          <q-tabs
            v-model="tab"
            dense
            outside-arrows
            mobile-arrows
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
            <q-tab-panel name="totals">
              <DataTable :users="users" :columns="columnLabels" :shiftCount="shiftCount" title="Schedule Shifts" :rowData="filtered_shifts"/>
            </q-tab-panel>

            <q-tab-panel name="schedule">
              <div class="text-h6">Scheduling Tools</div>
              <div class="row justify-between">
                <q-btn class="q-ma-xs btn-50" color="accent" id="add_shifts" :size="button_size" @click="quick_add" icon="more_time" label="Quick Add"></q-btn>
                <q-btn class="q-ma-xs btn-50" color="secondary" id="upload" :size="button_size" @click="upload_file = true" icon="upload_file" label="Upload"></q-btn>
              </div>
            </q-tab-panel>

            <q-tab-panel name="admin">
              <div class="text-h6">Admin Tools</div>
              <div class="row justify-between">
                <q-btn class="q-mx-xs btn-50" color="negative" id="clear_shifts" :size="button_size" @click="confirm = true" icon="cancel" label="Clear Month"></q-btn>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>
      <div class="col-8 col-xs-12 col-sm-8 col-md-8 col-lg-8">
        <div class="column justify-start">
          <div class="row align-start justify-center">
            <Calendar 
              @send_date="set_date" 
              @send_filter="set_filter" 
              @send_events="store_updated_events" 
              @edit_event="edit_event" 
              @date_clicked="date_clicked"
              :calEvents="events" 
              :calShifts="shifts" :calUsers="users" 
              :calDate="date" :editCal="true" 
              :dialog_open="add_shifts" />
          </div>
        </div>
      </div>
    </div>
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
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="settings" color="accent"  padding="sm" to="/schedule_settings"/>
    </q-page-sticky>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import Calendar from 'components/Calendar.vue'
import FormTest from 'components/FormTest.vue';
import BaseForm from 'components/BaseForm.vue';
import MainFunctions from '../../services/MainFunctions'
import CalendarFunctions from '../../services/CalendarFunctions'
import { useDummyData } from "stores/dummy-data.js"
import DataTable from "components/DataTable.vue"
import ConfirmDialog from "components/ConfirmDialog.vue"
import ScheduleTools from 'components/ScheduleTools.vue';

export default defineComponent({
  name: "ScheduleShifts",
  components: {
    Calendar,
    DataTable,
    ConfirmDialog, 
    // ScheduleTools,
    // BaseForm,
  },
  data() {
    return {
      calfunc: new CalendarFunctions(),
      dynamicComponent: null,
      components: {
        FormTest,
        BaseForm
      }
    }
  },
  setup() {
    const $q = useQuasar()
    const progress = ref(false)
    const store = useDummyData()
    
    return {
      
      store,
      events: ref([]),
      date: ref(new Date().toLocaleString('en-US', { year: 'numeric' }) + "-" + new Date().toLocaleString('en-US', { month: 'short' })),

      calendar_button: ref(false),
      auth_token: ref(false),
      users: ref([]),
      user: ref(null),
      show_users: ref(false),
      user_shifts: ref([]),
      user_data: ref({}),
      filtered_shifts: ref([]),
      submit_button: ref(false),
      disabled: ref(true),
      loading: ref(false),
      shifts: ref([]),
      shift_data: ref([]),     
      enable_date: ref(false),
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
      tab: ref('totals'),
      splitterModel: ref(20),
    };
  },
  watch: {
    date(newValue, oldValue) {
      // console.log(newValue, oldValue)
      // this.handleMonthChange(newValue, oldValue)
      let oldYear = oldValue.slice(0, 4);
      let newYear = newValue.slice(0, 4);
      // console.log(oldYear, newYear)
      if (newYear !== oldYear) {
        console.log("Year changed")
        this.getShiftsYear().then(() => {
          this.shift_count()
        });
      } else {
        console.log("Month changed")
        this.shift_count()
      }
    },
    add_shifts(newValue, oldValue) {
      if (newValue == false) {
        this.add_to_date = null
        this.event_edit = false
      }
    },
  },
  computed: {
      
  },
  methods: {
    set_date(date){
      console.log(date)
      this.date = date
    },

    async getShiftsYear() {
      const { calendarEvents, shifts, users } = await this.calfunc.getShiftsYear(this.date, this.events, this.shifts, this.users);
      this.events = calendarEvents;
      this.shifts = shifts;
      this.users = users;
    },

    set_filter(filter){
      console.log(filter)
      this.user = filter
      if (filter != null){
        this.filtered_shifts = this.user_shifts.filter(shift => shift.employee.includes(filter))
      } else {
        this.filtered_shifts = this.user_shifts
      }
    },

    resetEventId() {
      this.event_id = null;
      this.get_form = `/handle_forms`
    },

    store_updated_events(event) {
      // ========== Save Dragged Event ==========
      APIService.edit_event(event, true) // This saves events that are dragged and dropped
    },

    quick_add() {
      // this.get_form = '/quick_add'
      // this.submit_form = '/quick_add'
      this.multiDateSelect = true
      this.add_shifts = true
    },

    edit_event(info) {
      console.log(info.id)
      this.event_id = info.id
      this.event_edit = true
      this.get_form = `/handle_forms`
      this.submit_form = '/handle_forms'
      this.multiDateSelect = false
      this.add_shifts = true
    },

    date_clicked(date) {
      console.log(date)
      this.get_form = '/handle_forms'
      this.submit_form = '/handle_forms'
      this.add_shifts = true
      this.add_to_date = date
      console.log(this.form_data)
      this.form_data = {
        "date": date,
      }

    },

    form_complete() {
      this.event_id = null
      this.add_shifts = false;
      this.getShiftsYear().then(() => {
        this.shift_count()
      });
    },

    async shift_count() {
      // calculate on backend with data pull
      // console.log(this.events, this.users)
      let date_filter = MainFunctions.date_to_number(this.date)
      // let year = date_filter.slice(0, 4)
      let temp_filter_date = new Date(this.date + "-01")
      let year = temp_filter_date.getFullYear()
      let month = temp_filter_date.getMonth()
      console.log(temp_filter_date, year, month)
      this.user_shifts = []
      this.filtered_shifts = []      
      console.log(this.shifts, this.events)
      for (let user of this.users) {
        let new_mon_arr = this.shifts.filter(shift => new Date(shift.start).getMonth() == month && shift.title.includes(user));
        let new_arr = this.shifts.filter(shift => new Date(shift.start).getFullYear() == year && shift.title.includes(user));
        console.log(`${user}: month : ${Object.keys(new_mon_arr).length}, array: ${Object.keys(new_arr).length}`)
        // let new_arr = this.shifts.filter((shift) => { return shift.title == user })
        // this.user_shifts.push({ employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length })
        // this.filtered_shifts.push({ employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length })
        this.user_shifts = [...this.user_shifts, { employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length }];
        this.filtered_shifts = [...this.filtered_shifts, { employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length }];
      }
      if (this.user != null){
        this.filtered_shifts = this.filtered_shifts.filter(shift => shift.employee.includes(this.user))
      }
      // console.log(this.user_shifts)
    },

    async file_upload() {
      console.log("and for ALL the marbles...!")
      if (this.file) {
        this.user_shifts = []
        // localStorage.setItem("gmail", this.gmail)
        let formData = new FormData()
        let file = this.file
        await formData.append("file", file)
        await formData.append("date", this.date)
        await APIService.upload_file(formData)
          .then((res) => {
            if (res.status == 200) {
              Notify.create({
                message: "Successfully uploaded shifts!",
                color: "green",
                position: 'center',
                timeout: 300,
              })
            } else {
              Notify.create({
                message: "Something went wrong",
                color: "red",
                position: 'center',
                timeout: 300,
              })
            }
          })
        Notify.create({
          message: "Successfully sent the file!",
          color: "green",
          position: 'center',
          timeout: 300,
        })
        this.clearFile()
        this.getShiftsYear().then(() => {
          this.shift_count()
        });
      }
    },

    async clearFile() {
      this.file = null
      this.upload_file = false
    },

    confirm_choice(choice) {
      this.confirm = false;
      console.log(choice);
      if (choice) {
        this.clear_shifts();
      }
    },

    async clear_shifts() {
      this.user_shifts = []
      this.filtered_shifts = []
      await APIService.clear_shifts(this.date)
      console.log("Cleared shifts")
      this.getShiftsYear().then(() => {
        this.shift_count()
      });
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
    console.log(this.store.dummyData.shiftCountColumns)
    this.columnLabels = this.store.dummyData.shiftCountColumns
    // this.get_user_list();
    this.getShiftsYear().then(() => {
      this.shift_count()
    });
    
  },
  
})
</script>
