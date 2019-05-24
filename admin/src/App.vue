<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <v-app id="inspire">
    <v-navigation-drawer
      :clipped="drawer.clipped"
      :fixed="drawer.fixed"
      v-model="drawer.open"
      app
    >
      <vue-perfect-scrollbar class="drawer-menu&#45;&#45;scroll" :settings="scrollSettings">
          <v-list dense expand subheader>
              <v-subheader>Каналы</v-subheader>
                <v-list-group
                        v-for="channel in channels"
                        :key="channel.id">
                    <template v-slot:activator>
                        <v-list-tile>
                            <v-list-tile-action>
                                <v-icon>chat_bubble_outline</v-icon>
                            </v-list-tile-action>
                            <v-list-tile-content>
                                <v-list-tile-title class="font-weight-bold">{{ channel.channelTitle }}</v-list-tile-title>
                            </v-list-tile-content>
                        </v-list-tile>
                    </template>
                    <v-list-tile :to="{ name: 'channelUsers', params: { name: channel.channelName } }">
                        <v-list-tile-action>
                            <v-icon>people_outline</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Пользователи</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile :to="{ name: 'channelTests', params: { name: channel.channelName } }">
                        <v-list-tile-action>
                            <v-icon>assignment</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Тесты/опросы</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile :to="{ name: 'channelRating', params: { name: channel.channelName } }">
                        <v-list-tile-action>
                            <v-icon>assessment</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Рейтинг</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list-group>
              <v-divider></v-divider>
                <v-list-tile :to="{name: 'newChannel'}">
                    <v-list-tile-action>
                        <v-icon>add</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Добавить канал</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
      </vue-perfect-scrollbar>
    </v-navigation-drawer>

    <v-toolbar
      app
      dark
      color="primary"
      :fixed="toolbar.fixed"
      :clipped-left="toolbar.clippedLeft"
    >
      <v-toolbar-side-icon
        @click.stop="toggleDrawer"
      ></v-toolbar-side-icon>
      <v-toolbar-title>Question Bot Administration</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-md-and-down">
            <div class="user-email d-flex align-center justify-center font-weight-bold">
                <v-icon>account_circle</v-icon>
                <p class="ml-2">dmitriyl1899@gmail.com</p>
            </div>
            <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on"><v-icon>exit_to_app</v-icon></v-btn>
                </template>
                <span>Выйти</span>
            </v-tooltip>
        </v-toolbar-items>
    </v-toolbar>
        <v-content>
            <HelloWorld/>
        </v-content>
  </v-app>
</template>

<style lang="scss">
    @media only screen and (min-width: 960px) {
        .v-toolbar__title:not(:first-child) {
            margin-left: 0
        }
    }
    .user-email p{
        margin: 0 auto;
    }
</style>

<script>
import HelloWorld from './components/HelloWorld'
import VuePerfectScrollbar from 'vue-perfect-scrollbar';
import apiEndpoints from './apiEndpoints'
import axios from 'axios'

export default {
  name: 'App',
  components: {
      HelloWorld,
      VuePerfectScrollbar
  },
  data: () => ({
      drawer: {
      // sets the open status of the drawer
        open: false,
        // sets if the drawer is shown above (false) or below (true) the toolbar
        clipped: true,
        // sets if the drawer is CSS positioned as 'fixed'
        fixed: true,
    },
      toolbar: {
        fixed: true,
        clippedLeft: true
    },
      scrollSettings: {
          maxScrollbarLength: 160
      },
      channels: [
          {
              id: 1,
              channelName: 'questions',
              channelTitle: 'Вопросы'
          },
          {
              id: 2,
              channelName: 'tests',
              channelTitle: 'Тесты'
          }
      ]
  }),
    methods: {
      getAllChannels() {
          axios.get(apiEndpoints.channels).then(({data}) => {
             data.forEach(channel => {
                 this.channels.push(channel)
             })
          });
      },
        toggleDrawer() {
          if (this.drawer.permanent) {
            this.drawer.permanent = !this.drawer.permanent;
            this.drawer.clipped = true;
            this.toolbar.clippedLeft = true;
          } else {
            // normal drawer
            this.drawer.open = !this.drawer.open;
      }
        }
    },
    created() {
      // this.getAllChannels();
    },
}
</script>
