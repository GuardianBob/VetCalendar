<template>
  <q-page class="q-pt-xl" >
    <!-- <div class="col-10 col-sm-5 col-md-5 col-lg-5"> -->
    <q-form           
      @submit="upload_shifts_v2">
      <div class="row align-start justify-center q-mx-sm items-center">
        <!-- <q-input filled v-model="gmail" required type="email" label="Gmail"></q-input> -->
          <div class="col-4 q-ml-sm">
            
            <q-btn class="q-mr-xs" color="primary" round size="sm" id="enable_file" @click="enable_file = !enable_file">
              <q-icon name="attach_file" />
              <q-tooltip class="bg-accent" anchor="bottom middle">Upload File</q-tooltip>
            </q-btn>
            
            <q-btn class="outline q-pa-none q-mr-xs" round dense id="authorize_button" @click="handleAuthClick" v-show="!auth_token">
              <img width="20" src="~assets/Google_G_Logo.svg" alt="">
              <q-tooltip class="bg-accent" anchor="bottom middle">Connect to Google</q-tooltip>
            </q-btn>
            <q-btn v-if="auth_token" class="q-mr-xs" color="accent" size="sm" round id="fetch_calendars" @click="sync_google" icon="sync">
              <q-tooltip class="bg-accent" anchor="bottom middle">Sync to Google Calendar</q-tooltip>
            </q-btn>
            <q-btn class="" color="primary" round size="sm" id="enable_file" @click="info = true">
              <q-icon name="question_mark" />
              <q-tooltip class="bg-accent" anchor="bottom middle">Help</q-tooltip>
            </q-btn>
            <!-- <q-input filled v-model="date" label="Select Date" class="q-my-sm" v-show="enable_date"></q-input> -->
          </div>
          <div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"></div>
          <div class="col-1 text-right q-mr-sm">
            <q-btn color="primary" round size="sm" id="enable_date" @click="enable_date = !enable_date" icon="event">
              <!-- <q-icon name="event" /> -->
              <q-tooltip class="bg-accent" anchor="bottom middle">Select Date</q-tooltip>
              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                <q-date v-model="date" mask="MMM YYYY">
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="accent" flat />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-btn>
          </div>
          <div class="col-xs-3 col-lg-2 col-md-2 col-sm-2 q-mr-sm">          
            <q-select class="q-mx-none" v-model="user" :options="users" dense options-dense @update:model-value="filterShifts()">
              <template v-slot:prepend>
                <q-icon name="filter_alt" round color="primary"/>
              </template>
              <template v-slot:append>
                <q-btn v-if="user !== null" class="q-ml-md q-px-sm" color="negative" size="md" flat rounded id="clear_filters_button" @click.stop.prevent="clearFilters" icon="cancel"/>
                <!-- <q-icon name="close" @click.stop.prevent="clearFilters" class="cursor-pointer" v-if="user !== null" /> -->
              </template>
              <q-tooltip class="bg-accent" anchor="center start">Filter Schedule</q-tooltip>
            </q-select>
          </div>
      </div>
      <div class="row justify-center q-mx-lg items-center" v-show="enable_file">
        <div class="col-lg-6 col-md-6 col-sm-6 col-xs-9 text-center">
        <q-file
        v-model="file"        
        label="Select File"
        accept=".docx, .doc"
        class="q-my-sm"
        counter
        >
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
        <q-btn class="q-mx-sm" size="sm" color="primary" round id="upload_button" @click="file_upload" v-show="file">
          <q-icon name="upload"></q-icon>
          <q-tooltip class="bg-accent">Upload File</q-tooltip>
        </q-btn>
        </div>
      </div>
          <q-btn
            v-if="auth_token"
            :loading="disabled"
            v-show="submit_button"
            color="primary"
            label="Add to Google Calendar"
            type="submit"
            class="q-px-lg q-mt-sm"
            :disabled="disabled"
          />
          <br>
          <q-spinner
          v-show="loading"
          color="primary"
          size="3em"
          :thickness="3"
          />
        <!-- </div> -->
    </q-form>
      <!-- </div> -->
      <!-- <q-tab-panels
      v-model="panel"
      animated
      infinite    
    >
    <q-tab-panel animated :name="panel"  > -->
      <div class="row align-start justify-center" v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe">
        <div class="col-10 col-md-10 col-sm-8 col-lg-6 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;">
          <FullCalendar 
            id="fullCalendar" 
            ref="fullCalendar" 
            
            :custom-buttons="customButtons" 
            :options='calendarOptions'/>
            
        </div>
      </div>
    <!-- </q-tab-panel>
    <q-tab-panel name="snail"> -->
      <!-- <div class="row align-start justify-center">
        <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe" class="col-10 col-md-10 col-sm-8 col-lg-6 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;">
          <FullCalendar 
            id="fullCalendar" 
            ref="fullCalendar" 
            :custom-buttons="customButtons" 
            :options='calendarOptions'/>
        </div>
      </div> -->
    <!-- </q-tab-panel>
  </q-tab-panels> -->
    <q-dialog v-model="info" transition-show="slide-down" transition-hide="slide-up">
      <ButtonDefinitions />
    </q-dialog>
    <!-- Place scroller at bottom -->
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import ButtonDefinitions from 'components/ButtonDefinitions.vue'

const quasar = useQuasar()
const CLIENT_ID = process.env.GOOGLE_CLIENT_ID
const API_KEY = process.env.GOOGLE_API_KEY
// Discovery doc URL for APIs used by the quickstart
const DISCOVERY_DOC = process.env.DISCOVERY_DOC;
// Authorization scopes required by the API; multiple scopes can be
// included, separated by spaces.
const SCOPES = process.env.SCOPES;

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default defineComponent({
  name: "FileUpload",
  components: {
    FullCalendar, // make the <FullCalendar> tag available
    ButtonDefinitions
  },

  data() {
    return {
      calendarOptions: ref({
        customButtons: ref({
          prev: {
            text: "PREV",
            click: () => {
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.prev();
              // console.log("eventPrev", calendarApi.getDate());
              this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
          next: { // this overrides the next button
            text: "NEXT",
            click: () => {
                // console.log("eventNext");
                let calendarApi = this.$refs.fullCalendar.getApi();
                calendarApi.next();
                this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
          today: { // this overrides the next button
            text: "Today",
            click: () => {
                // console.log("eventNext");
                let calendarApi = this.$refs.fullCalendar.getApi();
                calendarApi.today();
                this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
        }),
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        weekends: true,
        initialDate: new Date(),
        height: "auto",
        eventDisplay: 'block',
        eventColor: 'white',
        eventTextColor: "black",
        events: [
          { }
        ]
      }),
    }
  },
  setup() {
    
    const progress = ref(false)
    
    return {
      // label: "Select File",
      file: ref(null),
      date: ref(new Date().toLocaleString('en-US', { month: 'short', year: 'numeric' })),
      calendar_button: ref(false),
      tokenClient: null,
      gapiInited: false,
      gisInited: false,
      gmail: ref(''),
      auth_token: ref(false),
      users: ref([]),
      user: ref(null),
      show_users: ref(false),
      user_shifts: ref([]),
      submit_button: ref(false),
      disabled: ref(true),
      loading: ref(false),
      shifts: ref([]),
      shift_data: ref([]),     
      calendar_id: ref([]),
      show_add2Cal: ref(false),
      enable_file: ref(false),
      enable_date: ref(false),
      info: ref(false),
      slide: ref(1),
      panel: ref(1),
      savedTheme: 'light_theme',
      // onFileSelected(file) {
      //   this.file = file
      //   console.log(file)
      //   this.label = file.name
      // },
      // onFileRemoved(file) {
      //   this.file = null
      //   this.label = "Select File"
      // },
    };
  },
  watch: {
    file(newValue, oldValue) {
      if (newValue != null) {
        console.log("triggered")
        let new_month = ""
        let new_year = parseInt(this.date.slice(-4))
        let file_name = newValue["name"].toLowerCase()
        console.log(file_name)
        month_abbrev.forEach((month) => {
          if (file_name.includes(month.toLowerCase())) {
            console.log(month)
            new_month = month
          }        
        })      
        if (file_name.includes(new_year + 1)) {
          new_year = (new_year + 1).toString()
        }
        this.date = new_month + " " + new_year.toString()
        console.log(new_year)
        // this.user = null
        // this.get_users()      
      }
    },
    date(newValue, oldValue) {
      // console.log(newValue.slice(4, 8), oldValue.slice(4, 8))
      this.handleMonthChange()
      // if (newValue.slice(4, 8) != oldValue.slice(4, 8)){

      // }
    },
  },
  computed: {
      
  },
  methods: {
    splitDate(date) {
      let shift_date = new Date(date)
      let month = shift_date.toLocaleString('default', {month:'short'})
      let day = shift_date.toLocaleString('default', {weekday:'short'})
      let day_date = date.slice(8, 10)
      let date_string = `${day} - ${month} ${day_date} ${date.slice(0,4)} - ${date.slice(11, 16)}`
      return date_string
    },

    async handleRightSwipe() {      
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.prev();
      let new_date =  calendarApi.getDate().toString()
      // console.log("eventPrev", calendarApi.getDate());
      this.handleCalendarChange(new_date, -1)
      // this.panel = this.panel - 1

    },

    async handleLeftSwipe() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.next();
      let new_date =  calendarApi.getDate().toString()
      this.handleCalendarChange(new_date, 1)
      .then(() => {
        // this.panel = this.panel + 1
      })
    },

    async handleMonthChange(){
      let new_date = new Date('01 ' + this.date)
      let calendarApi = this.$refs.fullCalendar.getApi()
      calendarApi.gotoDate(new_date.toISOString())
      await this.getShifts()
      if (this.user) {
        this.filterShifts()
      }
      // console.log(this.calendarOptions.events.length)
    },

    async handleCalendarChange(cal_date, direction = null){
      let new_date = cal_date.slice(4, 7) + " " + cal_date.slice(11, 15)
      // console.log(new_date)
      this.date = new_date
      // let calendarApi = this.$refs.fullCalendar.getApi()
      // calendarApi.gotoDate(new Date('01 ' + new_date).toISOString())
      // if (direction != null) {
      //   if (direction > 0){
      //     calendarApi.next();
      //   } else {
      //     calendarApi.prev();
      //   }
      // //   this.panel = this.panel + direction
      // //   console.log(direction, this.panel)
      // }
      // let body = {}
      // body["date"] = this.date      
      // APIService.return_shifts(this.date)
      return
    },

    async file_upload(){
      console.log("and for ALL the marbles...!")
      if (this.file) {
        this.user_shifts = []
        localStorage.setItem("gmail", this.gmail)
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
        this.getShifts()
        this.clearFile()
        this.clearFilters()
      }
    },

    async getShifts() {
      let calendarApi = this.$refs.fullCalendar.getApi()
      let start = calendarApi.view.activeStart
      let end = calendarApi.view.activeEnd
      await APIService.return_shifts({"start": start, "end": end})
      .then(res => {
        // console.log(res.data)
        if (res.data != "No Shifts"){
          this.calendarOptions.events = []
          this.shifts = []
          // console.log(events)
          this.users = res.data.users
          res.data.shifts.map(event => { 
            // console.log(event)
            this.calendarOptions.events.push({
              // Add event to displayed calendar
              "title": event["user"],
              "start": event["start"],
              // "end": shift["end"]["dateTime"],
            })
            this.shifts.push({
              // Add event to displayed calendar
              "title": event["user"],
              "start": event["start"],
              // "end": shift["end"]["dateTime"],
            })
          })
          // 
        }
      })
      // console.log(this.shifts)
      calendarApi.updateSize()
    },

    async filterShifts() {
      console.log(this.user)
      this.calendarOptions.events = []
      this.shifts.map(shift => {
        if (shift["title"] == this.user){
          // console.log("matches")
          this.calendarOptions.events.push(shift)
          localStorage.setItem("filtered_user", this.user)
        }
      })
    },

    async clearFilters() {
      this.calendarOptions.events = this.shifts
      // console.log(this.shifts.length)
      this.user = null
      localStorage.removeItem("filtered_user")
    },

    async clearFile() {
      this.file = null
      this.enable_file = false
    },

    async timeMin() {
      let tz_offset =  (new Date()).getTimezoneOffset() * 60000
      let date_start = new Date(`01 ${this.date}`)
      let start = new Date(date_start - tz_offset).toISOString().slice(0,-5) + "Z"
      return start
    },

    async timeMax() {
      let tz_offset =  (new Date()).getTimezoneOffset() * 60000
      let date_start = new Date(`01 ${this.date}`)
      let date_end = new Date(date_start.getFullYear(), date_start.getMonth()+1, 0, 23, 59)
      let end = new Date(date_end - tz_offset).toISOString().slice(0,-5) + "Z"
      return end
    },

    async getShifts2() {
      // const request = gapi.client.calendar.events.insert({
      //   'calendarId': 'primary',
      //   'resource': event
      // });
      if (this.file) {
        this.user_shifts = []
        localStorage.setItem("gmail", this.gmail)
        let formData = new FormData()
        let file = this.file
        await formData.append("file", file)
        await formData.append("date", this.date)
        APIService.upload_file(formData)
        .then(res => {          
          this.calendarOptions.events = res.data ? [] : null
          console.log(res.data)
          Object.entries(res.data).forEach(
            ([key, shift]) => {
              this.calendarOptions.events.push({
                "title": shift["summary"],
                "start": shift["start"]["dateTime"],
              })
            }
          );
        })
        .catch(err => {
          Notify.create({
            message: "Something went wrong",
            color: "red",
          })
        })
      }
    },

    async get_users() {
      let calendarApi = this.$refs.fullCalendar.getApi()
      console.log("triggered")
      if (this.file) {
        this.loading = true
        localStorage.setItem("gmail", this.gmail)
        let formData = new FormData()
        let file = this.file
        await formData.append("file", file)
        await formData.append("date", this.date)
        // await formData.append("gmail", this.gmail)
        console.log(file)
        console.log("formData: ", formData)
        APIService.get_user_list(formData)
        .then(res => {
          console.log(res.data)
          console.log(this.date, res.data["month"])
          if (res.data["month"] != "false"){
            if (!this.date.includes(res.data["month"])){
              this.date = res.data["month"] + this.date.slice(3)
              let new_date = new Date('01 ' + res.data["month"] + this.date.slice(3))
              console.log(new_date.toISOString())
              calendarApi.gotoDate(new_date.toISOString())
              calendarApi.setOption('contentHeight', 'auto')
              calendarApi.updateSize()
            }
          }
          this.users = res.data["users"]
          this.show_users = true
          this.loading = false
          this.getShifts()
        })
      }
    },

    async sync_google() {
      if (this.user != null) {
        await this.verify_calendar().then(() => {
          console.log("syncing...")
          this.sync_shifts()
        })
        
      } else {
          Notify.create({
            message: "Please select which user to sync.",
            color: "red",
            position: "center"
          })
        }
    },

    async list_calendars() {
      return new Promise(resolve => {
        const get_calendars = gapi.client.calendar.calendarList.list()
        console.log(get_calendars)
        let exists = false
        get_calendars.execute((cal) => {
          let calendar = cal.items.find(o => o.summary.includes('AMCS Schedule'))
          if (calendar != undefined) {
            this.calendar_id = calendar.id
            exists = true
          }
          resolve(exists)
        })
      })
    },

    async list_calendars_v1() {
      return new Promise(async (resolve, reject) => {
        const get_calendars = gapi.client.calendar.calendarList.list()
        console.log(get_calendars)
        let exists = false
        await get_calendars.execute((cal) => {
          console.log(cal)
          cal.items.forEach((item) => {
            if (item.summary.includes("AMCS Schedule")) {
              this.calendar_id = item.id
              console.log(`calendar id: ${this.calendar_id}`)
              exists = true
            }
          })
          resolve(exists)
          reject("Error!")
        })
      })
    },

    async list_calendars_OLD() {
      return new Promise(async (resolve, reject) => {
        const get_calendars = gapi.client.calendar.calendarList.list()
        console.log(get_calendars)
        let calendars = {}
        await get_calendars.execute((cal) => {
          console.log(cal)
          cal.items.forEach((item) => {
            console.log(item)
            calendars[item.id] = item.summary
            console.log(item.summary)
          })
          console.log(calendars)
          if (Object.keys(calendars).length > 0) {
            resolve(calendars)
          } else {
            reject("Error!!!")
          }
        })
      })
    },

    async add_calendar() {
      return new Promise(async (resolve, reject) => {
        const insert_calendar = gapi.client.calendar.calendars.insert({
          summary: 'AMCS Schedule'
        });
        // console.log(insert_calendar)
        await insert_calendar.execute((res) => {
          // console.log(res, res.id, res.summary)
          this.calendar_id = res.id
          if (!res.error) {
            resolve(true)
            Notify.create({
              message: "Successfully created calendar!",
              color: "green",
            })
          } else {
            reject(false)
          }
        })
      })
    },

    async verify_calendar() {
      console.log(this.calendar_id)
      await this.list_calendars().then((response) => {
        console.log(response)
        if (response !== true) {
          this.add_calendar().then((res) => {
            return
          })
        } 
        return
      })      
    },

    async verify_calendar_OLD() {
      this.list_calendars().then((res) => { 
        console.log(res[0]) 
        // if (res.includes("AMCS")) {
        //   console.log("It WORKED!!!!!")
        Object.entries(res).forEach(([key, value]) => {
          console.log(key , value); // key ,value
          if (value.includes("AMCS Schedule")) {
            this.calendar_id = key
            console.log(`calendar id: ${this.calendar_id}`)
          } // else {
          //   console.log("NERP! Calendar doesn't exist")
          //   
          // }
        });
        if (this.calendar_id.length > 0){
          console.log("we found a calendar!")
          this.show_add2Cal = true;
        } else {
          console.log("no calendar!")
          let new_calendar = {
            // id: 'amcsschedule@group.calendar.google.com', // Trying to create the ID causes 400 error
            summary: 'AMCS Schedule'
          }
          this.add_calendar(new_calendar).then((res) => {
            console.log("res: ", res)
            // this.verify_calendar();
            this.show_add2Cal = true;
              Notify.create({
                message: "Successfully created calendar!",
                color: "green",
              })
          })
        }
        console.log(`calendar id: ${this.calendar_id}`)
        // res.map((cal) => { 
        //   console.log(cal)
        // })
      })
    },

    async get_google_events() {
      return new Promise(async resolve => {
        if (!this.calendar_id.length > 0) {
          // Need to fix so function waits for this to finish before trying to continue
          this.verify_calendar()
        } else {
          let params = {
            'calendarId': this.calendar_id,  
            'timeMin': await this.timeMin(),
            'timeMax': await this.timeMax(),
          }
          const get_events = gapi.client.calendar.events.list(params)
          // console.log(get_events)
          await get_events.execute((events) => {
            // console.log(events.items)
            resolve(events.items)
          })
        }
      })
    },

    async get_google_events_old() {
      return new Promise(async (resolve, reject) => {
        if (!this.calendar_id.length > 0) {
          // Need to fix so function waits for this to finish before trying to continue
          await this.verify_calendar()
        }
        console.log(this.date)
        let date_start = new Date(`01 ${this.date}`)
        let date_end = new Date(date_start.getFullYear(), date_start.getMonth()+1, 0, 23, 59)
        let tz_offset =  (new Date()).getTimezoneOffset() * 60000
        date_start = new Date(date_start - tz_offset).toISOString().slice(0,-5) + "Z"
        date_end = new Date(date_end - tz_offset).toISOString().slice(0,-5) + "Z"
        // date_start = date_start.toISOString().slice(0,-5) + "Z"
        // date_end = date_end.toISOString().slice(0,-5) + "Z"
        console.log(date_start)
        console.log(date_end)
        let params = {
          'calendarId': this.calendar_id,  
          'timeMin': date_start,
          'timeMax': date_end,
        }
        const get_events = gapi.client.calendar.events.list(params)
        console.log(get_events)
        let events = []
        await get_events.execute((event) => {
          // console.log(cal)
          event.items.forEach((item) => {
            // console.log(item)
            // events.push(item.id)
            events.push(item.id)
            // console.log(item.summary)
          })
          console.log(events)
          if (events.length > 0) {
            resolve(events)
          } else {
            reject("Error!!!")
          }
        })
      })
    },

    async clear_google_events() {
      this.get_google_events().then((res) => {
        // console.log(res)
        if (res.length > 0) {
          var batch = gapi.client.newBatch();
          res.forEach((event) => {
            batch.add(gapi.client.calendar.events.delete({
              'calendarId': this.calendar_id,
              'eventId': event.id
            }));
          })
          batch.then(() => {
            console.log('all jobs done!!!')
            Notify.create({
              message: "Schedule successfully cleared",
              color: "green",
            })
          })
        }
      });
    },

    async clear_google_events_old() {
      this.get_google_events().then((res) => {
        console.log(res)
        if (res.length > 0) {
          var batch = gapi.client.newBatch();
          res.forEach((event) => {
            batch.add(gapi.client.calendar.events.delete({
              'calendarId': this.calendar_id,
              'eventId': event
            }));
          })
          batch.then(() => {
            console.log('all jobs done!!!')
            Notify.create({
              message: "Schedule successfully cleared",
              color: "green",
            })
          })
        }
      });
    },

    async sync_shifts() {
      if (this.calendar_id.length > 0) {
        if (this.user != null) {
          await this.clear_google_events();
          var batch = gapi.client.newBatch();
          this.disabled = true
          console.log(this.user)
          this.calendarOptions.events.forEach((event) => {
            let shift_start = event.start.replace(/ /g, 'T')
            console.log(event.title, shift_start)
            let shift = {
              "summary": event.title,
              "start": {
                "dateTime": shift_start,
                "timeZone": "UTC"
              },
              "end": {
                "dateTime": shift_start,
                "timeZone": "UTC"
              },
              "reminders": {
                "useDefault": false,
              },
              "source.title" : "VetScheduler"
            }
            batch.add(gapi.client.calendar.events.insert({
              'calendarId': this.calendar_id,
              'resource': shift
            }));
          })
            // ====== NOTE: this loads the schedule to Google Calendar ============= 
          // console.log(batch)
          batch.then(() => {
            this.loading = false
            this.submit_button = false
            this.clearFilters()
            // this.user_shifts = []
            console.log('all jobs done!!!')
            Notify.create({
                message: "Schedule uploaded successfully",
                color: "green",
              })
          });
        } else {
          Notify.create({
            message: "Please select which user to sync.",
            color: "red",
            position: "center"
          })
        }
        
      }
    },

    async upload_shifts_v2() {
      if (this.calendar_id.length > 0) {
        if (this.user != null) {
          var batch = gapi.client.newBatch();
          this.disabled = true
          console.log(this.user)
          this.calendarOptions.events.forEach((event) => {
            let shift_start = event.start.replace(/ /g, 'T')
            console.log(event.title, shift_start)
            let shift = {
              "summary": event.title,
              "start": {
                "dateTime": shift_start,
                "timeZone": "UTC"
              },
              "end": {
                "dateTime": shift_start,
                "timeZone": "UTC"
              },
            }
            batch.add(gapi.client.calendar.events.insert({
              'calendarId': this.calendar_id,
              'resource': shift
            }));
          })
            // ====== NOTE: this loads the schedule to Google Calendar ============= 
          // console.log(batch)
          batch.then(() => {
            this.loading = false
            this.submit_button = false
            this.user = null
            // this.user_shifts = []
            console.log('all jobs done!!!')
            Notify.create({
                message: "Schedule uploaded successfully",
                color: "green",
              })
          });
        } else {
          Notify.create({
            message: "Please select which user to sync.",
            color: "red",
            position: "center"
          })
        }
        
      }
    },

    async upload_shifts() {
      var batch = gapi.client.newBatch();
      this.disabled = true
      this.user_shifts.forEach((shift) => {
        console.log(shift)
        batch.add(gapi.client.calendar.events.insert({
                'calendarId': 'primary',
                'resource': shift
              }));
        // ====== NOTE: this loads the schedule to Google Calendar ============= 
      })
      batch.then(() => {
        this.loading = false
        this.submit_button = false
        this.user = null
        this.user_shifts = []
        console.log('all jobs done!!!')
        Notify.create({
            message: "Schedule uploaded successfully",
            color: "green",
          })
      });
    },

    async upload_shifts_old() {
      var batch = gapi.client.newBatch();
      this.disabled = true
      this.user_shifts.forEach((shift) => {
        console.log(shift)
        batch.add(gapi.client.calendar.events.insert({
                'calendarId': 'primary',
                'resource': shift
              }));
        // ====== NOTE: this loads the schedule to Google Calendar ============= 
      })
      batch.then(() => {
        this.loading = false
        this.submit_button = false
        this.user = null
        this.user_shifts = []
        console.log('all jobs done!!!')
        Notify.create({
            message: "Schedule uploaded successfully",
            color: "green",
          })
      });
      // this.submit_button = false
    },
    
    async test_backend() {
      APIService.test_calendar().then(res => {
        console.log("res: ", res.data)
        Notify.create({
          message: "Calendar test successful",
          color: "green",
        })
      })
    },

    async test_event() {
      APIService.test_event().then(res => {
        console.log("res: ", res.data)
        Notify.create({
          message: "Event test successful",
          color: "green",
        })
      })
    },

    async test_API() {
      // var requestOptions = {
        //   method: 'POST',
        //   redirect: 'follow'
        // };
        
        // fetch("https://www.googleapis.com/calendar/v3/calendars/primary/events/quickAdd?calendarId=primary&text=Day Shift on June 21 7am-7pm", requestOptions)
        //   .then(response => response.text())
        //   .then(result => console.log(result))
        //   .catch(error => console.log('error', error));
        let event = {
          "summary": "Day Shift on June 21 7am-7pm",
          "location": "World Wide Web",
          "description": "Testing",
          "start": {
            "dateTime": "2023-06-21T07:00:00-07:00",
            "timeZone": "America/Los_Angeles"
          },
          "end": {
            "dateTime": "2023-06-21T19:00:00-07:00",
            "timeZone": "America/Los_Angeles"
          },
        }

        const request = gapi.client.calendar.events.insert({
          'calendarId': 'primary',
          'resource': event
        });
  
        request.execute(function(event) {
          appendPre('Event created: ' + event.htmlLink);
        });
    },

    gapiLoaded() {
        gapi.load('client', this.initializeGapiClient);
    },

    /**
       * Callback after the API client is loaded. Loads the
       * discovery doc to initialize the API.
       */
    async initializeGapiClient() {
      await gapi.client.init({
        apiKey: API_KEY,
        discoveryDocs: [DISCOVERY_DOC],
      });
      this.gapiInited = true;
      this.maybeEnableButtons();

    },

      /**
       * Callback after Google Identity Services are loaded.
       */
    gisLoaded() {
      this.tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: SCOPES,
        callback: '', // defined later
      });
      this.gisInited = true;
      this.maybeEnableButtons();
    },

      /**
       * Enables user interaction after all libraries are loaded.
       */
    maybeEnableButtons() {
      // if (this.gapiInited && this.gisInited) {
      //   // document.getElementById('authorize_button').style.visibility = 'visible';
      // }
    },

      /**
       *  Sign in the user upon button click.
       */
    handleAuthClick() {
      console.log("handleAuthClick")
      this.tokenClient.callback = async (resp) => {
        if (resp.error !== undefined) {
          throw (resp);
        }
        this.auth_token = true;
      };

      if (gapi.client.getToken() === null) {
        // Prompt the user to select a Google Account and ask for consent to share their data
        // when establishing a new session.
        this.tokenClient.requestAccessToken({prompt: 'consent'});
      } else {
        // Skip display of account chooser and consent dialog for an existing session.
        this.tokenClient.requestAccessToken({prompt: ''});
      }
    },

      /**
       *  Sign out the user upon button click.
       */
    handleSignoutClick() {
      const token = gapi.client.getToken();
      if (token !== null) {
        google.accounts.oauth2.revoke(token.access_token);
        gapi.client.setToken('');
        this.auth_token = false;
      }
    },

      /**
       * Print the summary and start datetime/date of the next ten events in
       * the authorized user's calendar. If no events are found an
       * appropriate message is printed.
       */
    async listUpcomingEvents() {
      let response;
      try {
        const request = {
          'calendarId': 'primary',
          'timeMin': (new Date()).toISOString(),
          'showDeleted': false,
          'singleEvents': true,
          'maxResults': 10,
          'orderBy': 'startTime',
        };
        response = await gapi.client.calendar.events.list(request);
      } catch (err) {
        document.getElementById('content').innerText = err.message;
        return;
      }

      const events = response.result.items;
      if (!events || events.length == 0) {
        document.getElementById('content').innerText = 'No events found.';
        return;
      }
      // Flatten to string to display
      const output = events.reduce(
          (str, event) => `${str}${event.summary} (${event.start.dateTime || event.start.date})\n`,
          'Events:\n');
      document.getElementById('content').innerText = output;
    },

    async get_stored_gmail() {
      if (localStorage.getItem('gmail')) {
        this.gmail = localStorage.getItem('gmail')
      }    
    },
  },

  created() {
    if (localStorage.getItem("filtered_user")) {
      this.user = localStorage.getItem("filtered_user")
    }    
  },
  
  mounted() {
    gapi.load('client', this.initializeGapiClient);
    this.tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: CLIENT_ID,
      scope: SCOPES,
      callback: '', // defined later
    });
    this.gisInited = true;
    this.maybeEnableButtons();
    this.get_stored_gmail();
    this.gapiLoaded()
    this.gisLoaded()
    this.getShifts().then(() => {
      if (this.user) {
        this.filterShifts()
      }
    })
  },
  
})
</script>
