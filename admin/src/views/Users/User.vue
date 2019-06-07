<template>
  <v-layout>
    <v-flex xs12 v-if="error">
      <p class="font-weight text-xs-center display-1">{{ errorMessage }}</p>
      <v-layout justify-center>
        <v-btn color="primary" @click="getUser">
          <v-icon left>cached</v-icon>
          Обновить
        </v-btn>
      </v-layout>
    </v-flex>
    <v-flex v-else>

      <v-card>
        <v-card-title>
          {{ user.firstName }} <span v-if="user.lastName && user.lastName !== ''">{{ user.lastName }}</span>
          <v-subheader><span v-if="user.username && user.username !== ''">{{ user.username }}</span><span v-else>Unknown username</span></v-subheader>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-subheader>Сортировать по дате</v-subheader>
          <v-layout align-content-space-between>
            <v-menu ref="startMenu" v-model="startMenu" :close-on-content-click="false" :nudge-right="40" lazy transition="scale-transition" offset-y full-width min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field v-model="startDateFormatted" label="От" prepend-icon="event" @blur="startDate = parseDate(startDateFormatted)" readonly v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="startDate" @input="startMenu = false" no-title scrollable first-day-of-week="1"
              >
              </v-date-picker>
            </v-menu>
            <v-menu ref="endMenu" v-model="endMenu" :close-on-content-click="false" :nudge-right="40" lazy transition="scale-transition" offset-y full-width min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field v-model="endDateFormatted" label="До" prepend-icon="event" @blur="endDate = parseDate(endDateFormatted)" readonly v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="endDate" @input="endMenu = false" no-title scrollable first-day-of-week="1"
              >
              </v-date-picker>
            </v-menu>
          </v-layout>
          <v-divider></v-divider>
          <v-list subheader two-line>
            <v-subheader>Очки, заработанные пользователем. Всего {{ this.pointsSum }}</v-subheader>
            <v-list-tile v-for="answer in answersToShow" :key="answer.id">
              <v-list-tile-content>
                <v-list-tile-title>Очки: {{ answer.points }}</v-list-tile-title>
                <v-list-tile-sub-title>Дата: {{ answer.createdAt }}</v-list-tile-sub-title>
              </v-list-tile-content>

            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
    import apiEndpoints from "../../apiEndpoints";
    import Axios from 'axios'

    export default {
        name: "User",
        props: ["name", "userId"],
        data: () => ({
            user: {},
            error: false,
            errorMessage: '',
            answersToShow: [],
            pointsSum: 0,
            startMenu: false,
            startDate: '',
            startDateFormatted: '',
            endMenu: false,
            endDate: '',
            endDateFormatted: ''
        }),
        watch: {
          startDate(val) {
            this.startDateFormatted = this.formatDate(this.startDate);
            this.sortAnswers();
          },
          endDate(val) {
            this.endDateFormatted = this.formatDate(this.endDate);
            this.sortAnswers();
          }
        },
        methods: {
            sortAnswers() {
                this.answersToShow = [];
                this.answersToShow = this.user.answers.filter(answer => {
                    let answerDate = new Date(this.parseDate(answer.createdAt));
                    if (this.startDate !== '' && this.endDate !== '') {
                         console.log('both Date');
                        let startDate = new Date(this.startDate);
                        let endDate = new Date(this.endDate);
                        return answerDate >= startDate && answerDate <= endDate;
                    } else if (this.startDate !== '') {
                        console.log('start Date');
                        let startDate = new Date(this.startDate);
                        return answerDate >= startDate;
                    } else if (this.endDate !== '') {
                        console.log('end Date');
                        let endDate = new Date(this.endDate);
                        return answerDate <= endDate;
                    } else {
                        return true;
                    }
                });
                this.countPointsSum();
            },
            formatDate(date) {
              if (!date) return null;
              const [year, month, day] = date.split("-");
              return `${day}.${month}.${year}`;
            },
            parseDate(date) {
              if (!date) return null;
              const [day, month, year] = date.split(".");
              return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
            },
            countPointsSum() {
              let sum = 0;
              this.answersToShow.forEach(answer => {
                  sum += answer.points;
              });
              this.pointsSum = sum;
            },
            getUser() {
                let apiUrl = apiEndpoints.channelUser.replace('channelName', this.name).replace('userId', this.userId);
                Axios.get(apiUrl).then(({data}) => {
                    this.error = false;
                    this.user = data;
                    this.answersToShow = data.answers;
                    this.countPointsSum();
                    document.title = `${user.firstName} | QuestionBot`;
                }).catch(error => {
                    this.error = true;
                    if (error.response) {
                        let errorStr = "";
                        error.response.data.errors.forEach(errorData => {
                            errorStr += errorData;
                        });
                        this.errorMessage = errorStr;
                    } else {
                        console.error(error);
                        this.errorMessage = "Что-то пошло не так..."
                    }
                })
            }
        },
        created() {
            this.getUser();
        }
    }
</script>

<style scoped>

</style>