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
        />

        <q-toolbar-title>
          Shift Management
        </q-toolbar-title>

        <div class="text-secondary">v: {{ version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      bordered
      overlay
    >
      <q-list>
        <q-item-label
          header
        >
          <q-icon v-if="$q.platform.is.mobile" name="menu" size="md" color="secondary" @click="drawer = !drawer" ></q-icon>
          Menu
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
        <q-item
          clickable
          @click="logout"
        >
          <q-item-section
              avatar
            >
              <q-icon name="logout" color="negative "/>
            </q-item-section>
            <q-item-section>
              Logout</q-item-section>
          </q-item>
      </q-list>
    </q-drawer>

    <q-page-container >
      <router-view @click="drawer = false"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
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
  {
    title: 'Login',
    caption: '',
    icon: 'lock',
    link: '/login',
    sublinks : [
      {
        title: 'Login',
        caption: '',
        icon: 'lock',
        link: '/login'
      },
      {
        title: 'Register',
        caption: '',
        icon: 'lock',
        link: '/register'
      },
    ]
  },
  {
    title: 'Admin',
    caption: '',
    icon: 'admin_panel_settings',
    sublinks : [
      {
        title: 'Schedule Import',
        caption: '',
        icon: 'upload_file',
        link: '/schedule_import'
      },
      {
        title: 'Manage Users',
        caption: '',
        icon: 'people',
        link: '/users'
      },
      {
        title: 'Manage Schedule',
        caption: '',
        icon: 'calendar_month',
        link: '/schedule'
      },
    ]
  },
  {
    title: 'Testing',
    caption: '',
    icon: 'construction',
    sublinks : [
      {
        title: 'BlankTest',
        caption: '',
        icon: 'upload_file',
        link: '/blank'
      },
      {
        title: 'FormTest',
        caption: '',
        icon: 'feed',
        link: '/form'
      },
    ]
  },
  // {
  //   title: 'Discord Chat Channel',
  //   caption: 'chat.quasar.dev',
  //   icon: 'chat',
  //   link: 'https://chat.quasar.dev'
  // },
  // {
  //   title: 'Forum',
  //   caption: 'forum.quasar.dev',
  //   icon: 'record_voice_over',
  //   link: 'https://forum.quasar.dev'
  // },
  // {
  //   title: 'Twitter',
  //   caption: '@quasarframework',
  //   icon: 'rss_feed',
  //   link: 'https://twitter.quasar.dev'
  // },
  // {
  //   title: 'Facebook',
  //   caption: '@QuasarFramework',
  //   icon: 'public',
  //   link: 'https://facebook.quasar.dev'
  // },
  // {
  //   title: 'Quasar Awesome',
  //   caption: 'Community Quasar projects',
  //   icon: 'favorite',
  //   link: 'https://awesome.quasar.dev'
  // }
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
    return {
      drawer: ref(false),
      essentialLinks: linksList,
      // toggleLeftDrawer () {
      //   leftDrawerOpen.value = !leftDrawerOpen.value
      // }
    }
  },
  methods: {
    logout() {
      // router.push({ name: 'login' });
      APIService.logout();
    }
  }
})
</script>
