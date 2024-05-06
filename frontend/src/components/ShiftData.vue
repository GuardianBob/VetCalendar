<template>
  <div class="row q-mx-md full-width justify-around ">
    <!-- <div class="text-h6 col-12">Shifts  Total: {{ total_shifts }}</div> -->
    <div class="col-12">
      <div class="text-h4">Total Shifts: {{ total_shifts }}</div>
    </div>
    <div v-if="selectedMonth" class="text-h6 text-secondary col-12 q-my-md">Total for {{ selectedMonth }}: {{ filtered_count }}</div>
    <div v-if="selectedYear && !selectedMonth" class="text-h6 text-secondary col-12 q-my-md">Total for {{ selectedYear }}: {{ filtered_count }}</div>
    <!-- <q-date 
      v-model="filter_date" 
      default-view="Months"
      emit-immediately
      @update:model-value="onUpdateMv"
      minimal 
      mask="MM"
      :key="dpKey"
      size="sm"
    /> -->
    <div class="col-2 col-xs-10 col-sm-2 col-md-2 col-lg-2 q-ma-sm">
      <q-select bg-color="primary" dense dark filled label-color="white" v-model="selectedMonth" :options="months" label="Month" >
      <template v-if="selectedMonth" v-slot:append>
        <q-icon name="cancel" @click.stop.prevent="selectedMonth = null" class="cursor-pointer" />
      </template>
      </q-select>
    </div>
    <div class="col-2 col-xs-10 col-sm-2 col-md-2 col-lg-2 q-ma-sm">
      <q-select bg-color="primary" dense dark filled label-color="white" v-model="selectedYear" :options="years" label="Year" >
      </q-select>
    </div>
    <div class="col-2 col-xs-10 col-sm-2 col-md-2 col-lg-2 q-ma-sm">
      <q-select bg-color="primary" dense dark filled label-color="white" v-model="sort_by" :options="sort_options.map(option => ({label: option.label, value: option.value}))" map-options label="Show Count By" >
        <template v-if="sort_by" v-slot:append>
          <q-icon name="cancel" @click.stop.prevent="sort_by = null" class="cursor-pointer" />
        </template>
      </q-select>
    </div>
    
    <DataTable :columns="columnLabels" :rowData="filtered_shifts"/>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import DataTable from './DataTable.vue'

const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"];
const defaultLabels = [
  { "name": "shift_type__type_label", "align": "left", "label": "Shift Type", "field": "shift_type__type_label", "sortable": true },
  { "name": "shift_name__shift_label", "align": "left", "label": "Shift", "field": "shift_name__shift_label", "sortable": true },
  { "name": "shift_start", "align": "right", "label": "Date", "field": "shift_date", "sortable": true },
]

const typeLabels = [
  { "name": "type", "align": "left", "label": "Shift Type", "field": "type", "sortable": true },
  { "name": "count", "align": "left", "label": "Type Total", "field": "count", "sortable": true },
]

export default {
  name: "ShiftData",
  components: {
    DataTable
  },
  props: [ 
    "parentFunction", 
    "shifts",
  ],
  setup() {
    return {
      pageTitle: ref(''),
      // filter_date: ref(new Date()),
      months,
      columnLabels: ref(defaultLabels),
      years: ref([]),
      shifts_month: ref([]),
      shifts_year: ref([]),
      total_shifts: ref(),
      filtered_shifts: ref([]),
      filtered_count: ref(0),
      selectedMonth: ref(''),
      selectedYear: ref(new Date().getFullYear()),
      dataTable_columns: ref([]),
      sort_options: ref([{value: 'shift_type__shift_type', label:'Shift Type'}, {value: 'shift_name__shift_name', label:'Shift Name'}]),
      sort_by: ref(''),
    }
  },

  watch: {
    shifts: {
      immediate: true,
      handler(newValue, oldValue) {
        console.log("watcher triggered")
        this.total_shifts = newValue.length
        this.update_shifts()
      }
    },
    selectedMonth(newValue, oldValue) {
      this.filter_shifts()
    },
    selectedYear(newValue, oldValue) {
      console.log(oldValue)
      if (oldValue != null) {
        this.filter_shifts()
      }
      console.log(this.selectedMonth)
    },
    sort_by(newValue, oldValue) {
      this.filter_shifts()
    }
  },

  methods: {
    shift_count() {
      let year = new Date().getFullYear();
      let date = new Date("01 " + this.selectedMonth + " " + year)
      console.log
      // this.filter_date = `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
      this.shifts_month = []
      console.log(date.getFullYear())
      let new_mon_arr = this.shifts.filter(shift => new Date(shift.shift_start).getMonth() == date.getMonth());
      let new_arr = this.shifts.filter(shift => new Date(shift.shift_start).getFullYear() == date.getFullYear());
      // this.shifts_month = [...this.shifts_month, { type: shift, monthTotal: new_mon_arr.length, yearTotal: new_arr.length }];
      
      let shiftTypeCounts = this.shifts.reduce((acc, shift) => {
        acc[shift.shift_type__type_label] = (acc[shift.shift_type__type_label] || 0) + 1;
        return acc;
      }, {});

      let shiftNameCounts = this.shifts.reduce((acc, shift) => {
        acc[shift.shift_name__shift_label] = (acc[shift.shift_name__shift_label] || 0) + 1;
        return acc;
      }, {});
      
      let shiftTypeByMonth = new_mon_arr.reduce((acc, shift) => {
        acc[shift.shift_type__type_label] = (acc[shift.shift_type__type_label] || 0) + 1;
        return acc;
      }, {});

      console.log(shiftTypeCounts);
      console.log(shiftNameCounts);
      console.log(date.getMonth(), shiftTypeByMonth);
    },

    shift_count_month() {
      let date = new Date("01 " + this.selectedMonth + " " + this.selectedYear)
      console.log(this.filtered_shifts)
    },
    
    shift_count_year() {
      console.log(this.selectedMonth)
      let date = new Date("01 Jan " + this.selectedYear)
      console.log(date)
      this.filtered_shifts = this.shifts.filter(shift => new Date(shift.shift_start).getFullYear() == this.selectedYear);
      if (this.months.includes(this.selectedMonth)) {
        this.shift_count_month()
      }
    },

    filter_date() {
      if (this.months.includes(this.selectedMonth)) {
        let date = new Date("01 " + this.selectedMonth + " " + this.selectedYear)   
        this.filtered_shifts = this.shifts.filter(shift => {
          let shiftDate = new Date(shift.shift_start);
          return shiftDate.getFullYear() == this.selectedYear && shiftDate.getMonth() == date.getMonth();
        });
      } else {
        console.log('filtering by year only')
        this.filtered_shifts = this.shifts.filter(shift => new Date(shift.shift_start).getFullYear() == this.selectedYear);
      }
      this.filtered_count = this.filtered_shifts.length
    },

    filter_shifts() {
      console.log(this.sort_by)
      // group shifts objects by filter and show count
      // sample shift object: {"id": 17, "shift_name__shift_label": "Day", "shift_type__type_label": "Holiday", "shift_start": "2024-02-25 15:00:00"}
      let shiftCounts = []
      this.filter_date()
      console.log(this.filtered_shifts)
      if (this.sort_by){
        console.log(this.sort_by.value)
        if (this.sort_by.value == 'shift_type__shift_type') {
          shiftCounts = this.filtered_shifts.reduce((acc, shift) => {
            acc[shift.shift_type__type_label] = (acc[shift.shift_type__type_label] || 0) + 1;
            return acc;
          }, {});
        } else if (this.sort_by.value == 'shift_name__shift_name') {
          shiftCounts = this.filtered_shifts.reduce((acc, shift) => {
            acc[shift.shift_name__shift_label] = (acc[shift.shift_name__shift_label] || 0) + 1;
            return acc;
          }, {});
        }
        this.filtered_shifts = Object.entries(shiftCounts).map(([type, count]) => ({ type, count }));
        this.columnLabels = typeLabels
      }
      //   this.filtered_shifts = this.shifts.reduce((acc, shift) => {
      //     acc[shift.shift_type__type_label] = (acc[shift.shift_type__type_label] || 0) + 1;
      //     return acc;
      //   }, {});
      // } else {
      //   this.filtered_shifts = this.shifts.reduce((acc, shift) => {
      //     acc[shift.shift_name__shift_label] = (acc[shift.shift_name__shift_label] || 0) + 1;
      //     return acc;
      //   }, {});
      else {
        this.filtered_count = this.filtered_shifts.length
        this.columnLabels = defaultLabels
      }
      // console.log(shiftCounts)
    },

    update_shifts() {
      let date = new Date()
      this.years = Array.from({length: 10}, (v, k) => date.getFullYear() - k)
      this.columnLabels = defaultLabels
      this.filtered_shifts = this.shifts
      this.filtered_count = this.shifts.length
      this.selectedYear = new Date().getFullYear()
      this.shift_count_year()
      console.log(this.shifts, this.total_shifts)
    },
    
    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    }

    
  },

  mounted() {
    // this.userData = this.users
    // this.update_shifts()
  }
};
</script>


