<template>
  <q-page class="q-pt-xl">
    
        <q-card class="">
          <q-card-section>
            <div class="text-h6">Button Definitions</div>
          </q-card-section>
          <q-card-section>
            <div class="row items-center justify-around">
              <div class="col-1">
                <q-btn class="" size="sm" color="primary" round >
                  <q-icon name="file_upload" />
                </q-btn>
              </div>
              <div class="col-10">
                Click to enable file selection and upload.  Use this to upload a new schedule.
              </div>
            </div>
            <div class="row items-center justify-around">
              <div class="col-1">
                <q-btn class="outline q-pa-none" round dense id="authorize_button">
                  <img width="20" src="~assets/Google_G_Logo.svg" alt="">
                </q-btn>
              </div>
              <div class="col-10">
                  Click to connect the schedule app to your Google account to allow you to sync the schedule to your Google calendar.  
              </div>
            </div>
            <div class="row items-center justify-around">
              <div class="col-1">
                <q-btn class="q-ma-xs" color="accent" round size="sm">
                  <q-icon name="sync" />
                </q-btn>
              </div>
              <div class="col-10">
                  Click to sync the schedule to your Google calendar.
              </div>
            </div>
            <div class="row items-center justify-around">
              <div class="col-1">
                <q-btn class="q-ma-xs" color="primary" round size="sm">
                  <q-icon name="event" />
                </q-btn>
              </div>
              <div class="col-10">
                  Click to sync the schedule to your Google calendar.
              </div>
            </div>
            <div class="row items-center justify-around">
              <div class="col-1">
                <q-btn class="q-ma-xs" color="primary" round size="sm" id="authorize_button">
                  <q-icon name="filter_alt" />
                </q-btn>
              </div>
              <div class="col-10">
                Click to filter the calendar to display only the selected user.
              </div>
            </div>
          </q-card-section>
          <q-card-section> 
            <div class="text-right">
              <q-btn class="q-ma-xs" color="negative" round size="sm"  @click="info = false">
                <q-icon name="close"></q-icon>
              </q-btn>
            </div>
          </q-card-section>
        </q-card>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "ButtonDefinitions",

  setup() {
    return {
      info: ref(false),
      savedTheme: 'light_theme',
    }
  }
};
</script>


