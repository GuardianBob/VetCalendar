<template>
  <div class="row q-mx-md full-width justify-around ">
    <!-- Blank -->
    <div class="col-10">
      <q-splitter
        v-model="splitterModel"
      >
        <template v-slot:before>
          <div class="row">
            <div class="col-5"></div>
            <div class="col-7 q-pa-md">
              <q-date
                v-model="date"
                event-color="orange"
                :events="events"
                @click="get_availability"
              />
            </div>
          </div>
          <div class="row justify-center">
            <div class="col-5 q-pa-md"></div>
            <div class="col-7 q-mt-lg q-px-md text-center">
              <q-btn color="negative" @click="clearAll()" label="Reset" class="q-mx-xs"/>
              <q-btn color="primary" @click="saveClicked()" label="Save" class="q-mx-xs"/>
            </div>
          </div>
        </template>

        <template v-slot:after>
          <q-tab-panels
            v-model="date"
          >
            <q-tab-panel :name="date">
              <!-- <q-card style="width: 90%" flat> -->
                <!-- <q-card-section> -->
                  <div class="row">
                    <!-- <div class="col-12"></div> -->
                    <div rounded class="col-5 text-center q-px-sm">
                      <div class="col-12 text-center bg-primary text-white rounded-borders">
                          {{ date }}
                      </div>
                      <span v-for="(time, index) in avilableTimes" :key="index">
                        <q-btn :label="time" :color="clicked[index]" @click="timeClicked(index)" class="q-mx-sm q-my-xs q-px-lg"/>
                      </span>
                    </div>                    
                    <div class="col-3 text-center">
                      <div v-for="(times, event_date) in selectedTimes" :key="event_date">
                        <div v-if="times && times.length > 0">
                          <!-- <div class="bg-primary text-white rounded-borders">{{ event_date }}</div> -->
                          <q-btn size="12px" dense padding="0px lg" color="primary" @click="jump_to_date(event_date)">{{ event_date }}</q-btn>
                          <div v-for="(time, timeIndex) in times" :key="`time-${timeIndex}`">
                            <q-chip color="primary" text-color="white" :label="time" removable @remove="removeTime(event_date, time)"/>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-5 q-my-sm text-center">
                      <!-- <q-btn class="q-mx-xs" label="Close" color="primary" @click="showTime = false"/> -->
                      <q-btn class="q-mx-xs q-px-lg" label="Clear" color="negative" @click="clearClicked()"/>
                    </div>
                  </div>
                  
                <!-- </q-card-section> -->
                <!-- <q-card-actions class="row justify-right"> -->
                  <!-- <div class="row">
                    <div class="col-5 q-my-sm text-center">
                      <q-btn class="q-mx-xs" label="Close" color="primary" @click="showTime = false"/>
                      <q-btn class="q-mx-xs q-px-lg" label="Clear" color="negative" @click="clearClicked()"/>
                    </div>
                  </div>   -->
                <!-- </q-card-actions> -->
              <!-- </q-card> -->
            </q-tab-panel>
          </q-tab-panels> 
        </template>
      </q-splitter>
    </div>

    <!-- <div class="col-6 q-mt-lg">
      <q-date
        v-model="date"
        today-btn
        no-unset
        landscape
        @click="get_availability"
        />
    </div>    
    <div class="col-2">
      <div v-for="(times, date) in selectedTimes" :key="date">
        <div v-if="times && times.length > 0">
          <div>{{ date }}</div>
          <div v-for="(time, timeIndex) in times" :key="`time-${timeIndex}`">
            <q-chip :label="time" removable @remove="removeTime(date, time)"/>
          </div>
        </div>
      </div>
    </div>
    
    <q-dialog v-model="showTime" >
      <q-card style="width: 90%">
        <q-card-section>
        </q-card-section>
        <q-card-section>
          <div class="row justify-center">
            <div class="col-5">
              <span v-for="(time, index) in avilableTimes" :key="index">
                <q-btn :label="time" :color="clicked[index]" @click="timeClicked(index)" class="q-mx-sm q-my-xs"/>
              </span>
            </div>
          </div>
        </q-card-section>
        <q-card-section>
          
        </q-card-section>
        <q-card-actions class="row justify-right">
          <div class="col text-right">
            <q-btn class="q-mx-xs" label="Close" color="primary" @click="showTime = false"/>
            <q-btn class="q-mx-xs" label="Clear" color="negative" @click="clearClicked()"/>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog> -->
    
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "ScheduleAvailability",
  props: [ "parentFunction" ],
  setup() {
    return {
      pageTitle: ref('Schedule Availability'),
      date: ref(new Date().toISOString()),
      splitterModel: ref(50),
      events: ref([]),      
      options: ref([ '2024/04/01', '2024/04/05', '2024/04/06', '2024/04/09', '2024/04/23' ]),
      avilableTimes: ref(),
      selectedTimes: ref({}),
      showTime: ref(false),
      clicked: ref([]),
      optionsFn (date) {
        // let start, end = this.getDateOptions()
        // console.log('start', start, 'end', end, 'date', date)
        return date >= start && date <= end
      },
    }
  },

  watch: {
    // date: {
    //   handler: function (newVal, oldVal) {
    //     if (newVal === null) {
    //       this.date = oldVal;
    //     } else {
    //       console.log(newVal);
    //       // this.get_availability();
    //     }
    //   },
    //   deep: true
    // }
  },

  methods: {
    getToday() {
      let date = new Date();
      this.date = date.getFullYear() + '/' + ('0' + (date.getMonth() + 1)).slice(-2) + '/' + ('0' + date.getDate()).slice(-2);
    },

    jump_to_date(date) {
      this.date = date;
      this.get_availability()
    },

    get_availability() {
      if (this.date != null){
        // console.log('triggerd', this.date)
        let start_time = 8
        let times = []
        for (let i = 0; i < 9; i++) {
          let time = start_time + i;
          let new_time = time.toString().padStart(2, '0') + ':00';
          times.push(new_time);
          new_time = time.toString().padStart(2, '0') + ':30';
          times.push(new_time);
        }
        if (this.selectedTimes.hasOwnProperty(this.date)) {
          // console.log('selected times found')
          this.clicked = new Array(times.length).fill('primary');
          this.selectedTimes[this.date].forEach(time => {
            let index = times.indexOf(time);
            this.clicked[index] = 'accent';
          });
        } else {
          this.clicked = new Array(times.length).fill('primary');
        }
        // this.clicked = new Array(times.length).fill('primary');
        this.avilableTimes = times;
        // this.showTime = true;
      }
    },

    timeClicked(index) {
      this.clicked[index] == "primary" ? this.clicked[index] = 'accent' : this.clicked[index] = 'primary';
      // console.log('clicked', this.avilableTimes[index])
      if (this.date in this.selectedTimes) {
        if (this.selectedTimes[this.date].includes(this.avilableTimes[index])) {
          this.selectedTimes[this.date] = this.selectedTimes[this.date].filter(time => time !== this.avilableTimes[index])
        } else {
          this.selectedTimes[this.date].push(this.avilableTimes[index])
          if (!this.events.includes(this.date)) {
            this.events.push(this.date)
          }
        }
        // this.selectedTimes[this.date].push(this.avilableTimes[index])
      } else {
        this.selectedTimes[this.date] = [this.avilableTimes[index]]
        this.events.push(this.date)
      }
      let selectedTimes = new Map(
        Object.entries(this.selectedTimes)
          .sort(([a], [b]) => new Date(a) - new Date(b))
      );
      this.selectedTimes = Object.fromEntries(selectedTimes);
      this.checkEvents()
    },

    checkEvents() {
      for (let key in this.selectedTimes) {
        if (this.selectedTimes.hasOwnProperty(key)) {
          let array = this.selectedTimes[key];
          if (array.length === 0) {
            console.log(`Array at key ${key} is empty`);
            this.events = this.events.filter(event => event !== key)
            delete this.selectedTimes[key]
          }
        }
      }
    },

    removeTime(date, time) {
      this.selectedTimes[date] = this.selectedTimes[date].filter(t => t !== time)
      this.checkEvents()
    },

    saveClicked() {      
      console.log('selected Times: ', this.selectedTimes)
      this.showTime = false;
    },

    clearClicked() {
      if (this.date in this.selectedTimes) {
        this.selectedTimes[this.date] = []
      }
      this.clicked = new Array(this.avilableTimes.length).fill('primary');
      this.showTime = false;
      this.checkEvents();
    },

    clearAll() {
      this.selectedTimes = {}
      this.events = []
      this.clicked = new Array(this.avilableTimes.length).fill('primary');
    },

    getDateOptions() {
      // NOTE WORKING
      let date = new Date(this.date); 
      // let startDate = date.getFullYear() + '/' + ('0' + (date.getMonth() + 1)).slice(-2) + '/' + ('0' + date.getDate()).slice(-2);
      let firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
      // firstDay = date ? date > firstDay : firstDay;
      let lastDay = new Date(date.getFullYear(), date.getMonth()+1, 0);
      first = firstDay.getFullYear() + '/' + ('0' + (firstDay.getMonth() + 1)).slice(-2) + '/' + ('0' + firstDay.getDate()).slice(-2);
      last = lastDay.getFullYear() + '/' + ('0' + (lastDay.getMonth() + 1)).slice(-2) + '/' + ('0' + lastDay.getDate()).slice(-2);
      return [first, last]
    },
  },

  mounted() {
    // this.userData = this.users
    this.getToday()
    this.get_availability()
  }
};
</script>


