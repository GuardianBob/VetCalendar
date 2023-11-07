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
        />

        <q-toolbar-title>
          Vet Scheduler
        </q-toolbar-title>

        <div>Version: {{ version }}</div>
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
          <q-icon v-if="$q.platform.is.mobile" name="menu" size="md" color="primary" @click="drawer = !drawer" ></q-icon>
          Essential Links
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container >
      <router-view @click="drawer = false" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { version } from '../../package.json'

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'home',
    link: '/'
  },
  {
    title: 'Schedule Import',
    caption: '',
    icon: 'code',
    link: '/schedule_import'
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
    
    return {
      drawer: ref(false),
      essentialLinks: linksList,
      // toggleLeftDrawer () {
      //   leftDrawerOpen.value = !leftDrawerOpen.value
      // }
    }
  }
})
</script>
