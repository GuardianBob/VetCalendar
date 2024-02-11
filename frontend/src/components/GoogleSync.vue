<template>
  <span>
    <q-item v-if="$q.platform.is.mobile" class="column" >
      <q-btn v-if="!auth_token" class="outline q-mx-xs" size="md" id="authorize_button" v-close-popup @click="handleAuthClick"
        v-show="!auth_token">
        <img width="20" src="~assets/Google_G_Logo.svg" alt="" class="q-mr-xs"> Connect to Google
        <q-tooltip class="bg-accent" anchor="bottom middle">Connect to Google</q-tooltip>
      </q-btn>
      <q-btn v-if="auth_token" class="q-mx-xs" color="accent" size="md" id="fetch_calendars" v-close-popup @click="sync_google">
        <q-icon name="sync" class="q-mr-xs" />
        Sync Google Calendar
        <q-tooltip class="bg-accent" anchor="bottom middle">Sync Google Calendar</q-tooltip>
      </q-btn>
    </q-item>
    <q-btn v-if="$q.platform.is.desktop" class="outline q-pa-none q-mr-xs" round dense id="authorize_button" @click="handleAuthClick"
      v-show="!auth_token">
      <img width="20" src="~assets/Google_G_Logo.svg" alt="">
      <q-tooltip class="bg-accent" anchor="bottom middle">Connect to Google</q-tooltip>
    </q-btn>
    <q-btn v-if="auth_token" class="q-mr-xs" color="accent" size="sm" round id="fetch_calendars"
      @click="sync_google" icon="sync">
      <q-tooltip class="bg-accent" anchor="bottom middle">Sync to Google Calendar</q-tooltip>
    </q-btn>
  </span>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from 'app/services/api';
import GoogleFunctions from 'app/services/GoogleFunctions';

export default {
  name: "GoogleSync",
  props: [ 
    "parentFunction",
    "date",
    "events",
    "user",
  ],
  setup() {
    return {
      keys: {},
      tokenClient: ref(null),
      gapiInited: ref(false),
      gisInited: ref(false),
      auth_token: ref(false),
    }
  },

  watch: {
  },

  methods: {
    initialize_google() {
      APIService.get_api_keys(["GOOGLE_API_KEY", "DISCOVERY_DOC", "GOOGLE_CLIENT_ID", "SCOPES"])
      .then((response) => {
        this.keys["GOOGLE_API_KEY"] = response.data.GOOGLE_API_KEY
        this.keys["DISCOVERY_DOC"] = response.data.DISCOVERY_DOC
        this.keys["GOOGLE_CLIENT_ID"] = response.data.GOOGLE_CLIENT_ID
        this.keys["SCOPES"] = response.data.SCOPES
        this.gapiLoaded()
        this.gisLoaded()
      })
    },

    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    },

    gapiLoaded() {
      gapi.load('client', this.initializeGapiClient);
    },

    async initializeGapiClient() {
      await gapi.client.init({
        apiKey: this.keys["GOOGLE_API_KEY"],
        discoveryDocs: this.keys["DISCOVERY_DOC"],
      });
      this.gapiInited = true;
    },

    gisLoaded() {
      this.tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: this.keys["GOOGLE_CLIENT_ID"],
        scope: this.keys["SCOPES"],
        callback: '', // defined later
      });
      this.gisInited = true;
      console.log("gisLoaded")
    },

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
        this.tokenClient.requestAccessToken({ prompt: 'consent' });
      } else {
        // Skip display of account chooser and consent dialog for an existing session.
        this.tokenClient.requestAccessToken({ prompt: '' });
      }
    },

    sync_google() {
      console.log("sync_google")
      if (this.user != null) {
        GoogleFunctions.sync_google(this.tokenClient, this.date, this.events, this.user)
      } else {
        Notify.create({
          message: "Please select which user to sync.",
          color: "red",
          position: "center"
        })
      }
    },

  },

  mounted() {
    this.initialize_google()
  }
};
</script>


