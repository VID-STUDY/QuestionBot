<template>
  <v-container>
    <v-layout wrap>
      <v-flex xs12>
        <v-card>
          <v-card-text>
            <v-list two-line subheader>
              <v-subheader>Пользователи, которые принимают участие в опросах</v-subheader>
              <v-list-tile :to="{name: 'channelUser', params: {name: name, userId: user.id}}" v-for="user in users" :key="user.id">
                <v-list-tile-content>
                  <v-list-tile-title>{{ user.firstName }} <span v-if="user.lastName && user.lastName !== ''">{{ user.lastName }}</span></v-list-tile-title>
                  <v-list-tile-sub-title>
                    <span v-if="user.username && user.username !== ''">{{ user.username }}</span>
                    <span v-else>Unknown</span>
                  </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
    import Axios from 'axios'
    import apiEndpoints from "../../apiEndpoints";

    export default {
        title: "Участники",
        name: 'ChannelMembers',
        props: ['name'],
        data: () => ({
            users: []
        }),
        methods: {
            getUsers() {
                let apiUrl = apiEndpoints.channelUsers.replace('channelName', this.name);
                Axios.get(apiUrl).then(({data}) => {
                    this.users = [];
                    data.forEach(user => {
                        this.users.push(user);
                    })
                }).catch(error => {

                })
            }
        },
        watch: {
            '$route'() {
                this.getUsers();
            }
        },
        mounted() {
            this.getUsers();
        }
    }
</script>