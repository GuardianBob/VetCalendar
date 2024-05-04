import { boot } from 'quasar/wrappers'
import { watch } from 'vue'
import { useMainStore } from 'src/stores/main-store';

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async (/* { app, router, ... } */) => {
  // something to do
  const mainStore = useMainStore();

  watch(
    () => mainStore.user,
    (newUser, oldUser) => {
      console.log('User changed:', newUser);
      if (newUser) {
        console.log('updating permissions at boot...')
        mainStore.updatePermissions();
        mainStore.setLoggedIn(true);
      }
    },
    { immediate: true }
  );
  // watch(
  //   // pinia.state,
  //   // (state) => {
  //   //   console.log('updating permissions at boot...')
  //   //   mainStore.updatePermissions();
  //   // },
  //   // { deep: true }
  //   () => mainStore.user,
  //   (newUser, oldUser) => {
  //     console.log('updating permissions at boot...')
  //     mainStore.updatePermissions();
  //   },
  //   { deep: true }
  // );
})
