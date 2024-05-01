<template>
  <q-layout view="hHh Lpr lff">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="drawer = !drawer"
          color="secondary"
          v-if="loggedIn"
        />

        <q-toolbar-title>
          <q-btn flat size="lg" label="VSS || Vet Scheduling System" to="/" />
        </q-toolbar-title>
        <div>
          <q-btn v-if="!loggedIn" flat label="Login" to="/login" />
          <q-btn-dropdown v-if="loggedIn" color="white" dropdown-icon="account_circle" flat dense >
            <q-list style="min-width: 100px; max-width: 200px;" class="text-center q-py-none">              
              <q-item v-if="loggedIn" clickable v-close-popup @click="onItemClick">
                <q-item-section class="">
                  <q-btn icon="manage_accounts" color="black" flat dense />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Profile</q-item-label>
                </q-item-section>
              </q-item>
              <!-- <q-item v-if="loggedIn" clickable v-close-popup @click="onItemClick">
                <q-item-section class="">
                  <q-btn icon="manage_accounts" color="primary" flat dense />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Videos</q-item-label>
                </q-item-section>
              </q-item> -->
              <q-item v-if="loggedIn" clickable v-close-popup @click="logout">
                <q-item-section class="">
                  <q-btn icon="logout" text-color="black" flat dense />
                </q-item-section>
                <q-item-section>
                  <q-item-label class="text-orange-10">Logout</q-item-label>
                </q-item-section>
              </q-item>
              <q-item v-if="!loggedIn" clickable v-close-popup to="/login">
                <q-item-section>
                  <q-item-label>Login</q-item-label>
                </q-item-section>
              </q-item>
              <!-- <q-item >
                <q-item-section>
                  <div class="text-accent">v: {{ version }}</div>
                </q-item-section>
              </q-item> -->
            </q-list>
          </q-btn-dropdown>
        </div>
        <!-- <div class="text-secondary">v: {{ version }}</div> -->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      bordered
      overlay
      v-if="loggedIn"
    >
      <q-list>
        <!-- <q-item-label
          header
        >
          <q-icon v-if="$q.platform.is.mobile" name="menu" size="md" color="secondary" @click="drawer = !drawer" ></q-icon>
          Menu
        </q-item-label> -->
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
        <q-item>
          <q-item-section avatar>
            <q-icon name="account_tree" color="accent"/>
          </q-item-section>
          <q-item-section>
            <div class="text-accent">v: {{ version }}</div>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-footer v-if="!loggedIn" elevated>
      <div class="text-center">v: {{ version }}</div>
    </q-footer>

    <q-page-container >
      <router-view @click="drawer = false"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, watch } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { version } from '../../package.json'
import { useMainStore } from "stores/main-store.js"
import { useRouter } from 'vue-router';
import APIService from '../../services/api';

const mainStore = useMainStore();

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'home',
    link: '/'
  },
  // {
  //   title: 'Login',
  //   caption: '',
  //   icon: 'lock',
  //   link: '/login'
  // },
  // {
  //   title: 'Login',
  //   caption: '',
  //   icon: 'lock',
  //   link: '/login',
  //   sublinks : [
  //     {
  //       title: 'Login',
  //       caption: '',
  //       icon: 'lock',
  //       link: '/login'
  //     },
  //     {
  //       title: 'Register',
  //       caption: '',
  //       icon: 'lock',
  //       link: '/register'
  //     },
  //   ]
  // },
  // {
  //   title: 'Admin',
  //   caption: '',
  //   icon: 'admin_panel_settings',
  //   sublinks : [
  {
    title: 'Manage Schedule',
    caption: '',
    icon: 'calendar_month',
    link: '/manage_schedule'
  },
  {
    title: 'Manage Users',
    caption: '',
    icon: 'people',
    link: '/users'
  },      
  // {
  //   title: 'Schedule Settings',
  //   caption: '',
  //   icon: 'settings',
  //   link: '/schedule_settings'
  // },
  {
    title: 'Admin Settings',
    caption: '',
    icon: 'settings',
    link: '/master_settings'
  },
      // {
      //   title: 'Schedule Import',
      //   caption: '',
      //   icon: 'upload_file',
      //   link: '/schedule_import'
      // },
    // ]
  // },
  {
    title: 'Testing',
    caption: '',
    icon: 'construction',
    sublinks : [
      {
        title: 'Page Test',
        caption: '',
        icon: 'upload_file',
        link: '/blank'
      },
      // {
      //   title: 'Forms Page Test',
      //   caption: '',
      //   icon: 'upload_file',
      //   link: '/forms_page'
      // },
      {
        title: 'Form Test',
        caption: '',
        icon: 'feed',
        link: '/form'
      },
      // {
      //   title: 'Add JSON Form',
      //   caption: '',
      //   icon: 'feed',
      //   link: '/add_json_form'
      // },
    ]
  },
]

export default defineComponent({
  name: 'MainLayout',
  
  components: {
    EssentialLink
  },
  data() {
    return {
      version: version,
    }
  },
  setup () {
    const router = useRouter();
    const loggedIn = ref(false)
    // const mainStore = useMainStore();
    watch(() => mainStore.loggedIn, () => {
      // check_login()
      // console.log(`Logging in...`)
      if (localStorage.getItem('access_token')) {
        // console.log('Logged in')
        loggedIn.value = true;
      } else {
        // console.log('Not logged in')
        loggedIn.value = false;
      }
    })

    return {
      drawer: ref(false),
      essentialLinks: linksList,
      profile_icon: ref('no_accounts'),
      loggedIn,
      // toggleLeftDrawer () {
      //   leftDrawerOpen.value = !leftDrawerOpen.value
      // }
    }
  },

  watch: {
    // mainStore: {
    //   immediate: true,
    //   handler() {
    //     this.verify_login()
    //   }
    // },
  },
  methods: {
    verify_login() {
      console.log(`Logging in...`)
      if (localStorage.getItem('access_token')) {
        console.log('Logged in')
        this.loggedIn = true;
        mainStore.setLoggedIn(true)
      }
      // } else {
      //   console.log('Not logged in')
      //   // this.loggedIn = false;
      // }
    },
    logout() {
      // router.push({ name: 'login' });
      APIService.logout();
      mainStore.setLoggedIn(false)
    }
  },
  mounted() {
    this.verify_login()
  }
})
</script>
