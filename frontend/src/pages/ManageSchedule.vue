<template>
  <q-page class="q-pt-xl" >
    <div class="row align-start justify-center q-mx-sm ">
      <div class="col-4 q-pl-sm">
        <DataTable :users="users" :columns="columnLabels" :shiftCount="shiftCount" title="Schedule Shifts" :rowData="filtered_shifts"/>
      </div>
      <div class="col-8 q-pr-sm">
        <div class="column justify-start">
            <div class="col-2">
              <q-btn color="accent" id="add_shifts" :size="button_size" @click="quick_add" icon="more_time" label="Quick Add"></q-btn>
            </div>
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

export default defineComponent({
  name: "ScheduleShifts",
  components: {
    Calendar,
    DataTable,
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
      let year = date_filter.slice(0, 4)
      console.log(date_filter, year)
      console.log(this.shifts)
      this.user_shifts = []
      this.filtered_shifts = []
      for (let user of this.users) {
        let new_mon_arr = this.shifts.filter(shift => shift.start.includes(date_filter) && shift.title.includes(user));
        let new_arr = this.shifts.filter(shift => shift.start.includes(year) && shift.title.includes(user));
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
