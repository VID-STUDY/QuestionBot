import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
  iconfont: 'md',
  theme: {
    primary: '#1E9AC2',
    secondary: '#424242',
    accent: colors.red.darken1,
    info: '#2196f3',
    success: '#4caf50',
    warning: '#ffc107'
  }
});
