<template>
  <v-container>
    <v-layout row justify-center>
      <v-card>
        <v-toolbar color="primary" dark flat dense cad>
          <v-toolbar-title class="subheading">Создать викторину</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-divider></v-divider>
        <v-card-text class>
          <v-form v-model="isValid" ref="form">
            <v-layout row wrap>
              <v-flex xs12 md6>
                <v-menu
                  ref="startMenu"
                  v-model="startMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="startDate"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="startDateFormatted"
                      label="Дата начала"
                      :rules="startDateRules"
                      prepend-icon="event"
                      @blur="startDate = parseDate(startDateFormatted)"
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="startDate"
                    no-title
                    scrollable
                    :allowed-dates="allowedStartDates"
                    first-day-of-week="1"
                  >
                    <v-spacer></v-spacer>
                    <v-btn flat color="primary" @click="startMenu = false">Отмена</v-btn>
                    <v-btn flat color="primary" @click="$refs.startMenu.save(startDate)">Ок</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs12 md6>
                <v-menu
                  ref="endMenu"
                  v-model="endMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="endDate"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="endDateFormatted"
                      label="Дата окончания"
                      prepend-icon="event"
                      readonly
                      :rules="endDateRules"
                      @blur="endDate = parseDate(endDateFormatted)"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="endDate"
                    no-title
                    scrollable
                    :allowed-dates="allowedEndDates"
                    first-day-of-week="1"
                  >
                    <v-spacer></v-spacer>
                    <v-btn flat color="primary" @click="endMenu = false">Отмена</v-btn>
                    <v-btn flat color="primary" @click="$refs.endMenu.save(endDate)">Ок</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="topCount"
                  :rules="topCountRules"
                  label="Количество топ игроков"
                  prepend-icon="filter_1"
                />
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" flat @click="goBack">
            <v-icon left>arrow_back</v-icon>Назад
          </v-btn>
          <v-btn color="primary" flat @click="save" :disabled="isLoading" :loading="isLoading">
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon light>cached</v-icon>
              </span>
            </template>
            <v-icon left>save</v-icon>Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
    <v-snackbar v-model="snackbar" bottom color="error">
      {{ snackbarText }}
      <v-btn flat @click="snackbar = false">
        <v-icon left>close</v-icon>Закрыть
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import Axios from "axios";
import apiEndpoints from "../../apiEndpoints";
export default {
  name: "NewQuiz",
  props: ["name"],
  data: () => ({
    isValid: true,
    startMenu: false,
    endMenu: false,
    startDate: "",
    endDate: "",
    startDateFormatted: "",
    endDateFormatted: "",
    topCount: 10,
    isLoading: false,
    snackbar: false,
    snackbarText: ""
  }),
  computed: {
    computedStartDateFormatted() {
      return this.formatDate(this.startDate);
    },
    computedEndDateFormatted() {
      return this.formatDate(this.endDate);
    },
    startDateRules() {
      const rules = [];
      const requiredRule = value => {
        return value !== "" || "Укажите дату начала викторины"
      };
      const lessThenEndDateRule = value => {
        if (this.endDate !== "" && value !== "") {
          let dateValue = new Date(this.parseDate(value));
          let endDateValue = new Date(this.endDate);
          return dateValue < endDateValue || "Дата начала должна быть раньше, чем дата конца";
        }
        return true;
      };
      rules.push(requiredRule);
      rules.push(lessThenEndDateRule);
      return rules;
    },
    endDateRules() {
      const rules = [];
      const requiredRule = value => {
        return value !== "" || "Укажите дату окончания викторины"
      };
      const moreThanStartDateRule = value => {
        if (this.startDate !== "" && value !== "") {
          let dateValue = new Date(this.parseDate(value));
          let startDateValue = new Date(this.startDate);
          return dateValue > startDateValue || "Дата окончания должна быть позже, чем дата начала";
        }
        return true;
      };
      rules.push(requiredRule);
      rules.push(moreThanStartDateRule);
      return rules;
    },
    topCountRules() {
      const rules = [];
      const requiredRule = value => {
        return value !== "" || "Укажите количество топ игроков"
      };
      rules.push(requiredRule);
      return rules;
    }
  },
  watch: {
    startDate(val) {
      this.startDateFormatted = this.formatDate(this.startDate);
    },
    endDate(val) {
      this.endDateFormatted = this.formatDate(this.endDate);
    }
  },
  methods: {
    goBack() {
      this.$router.push({
        name: "channelQuizzes",
        params: { name: this.name }
      });
    },
    save() {
      if (!this.$refs.form.validate()) {
        return;
      }
      this.isLoading = true;
      let apiUrl = apiEndpoints.channelQuizzes.replace(
        "channelName",
        this.name
      );
      let data = {
        startDate: this.startDateFormatted,
        endDate: this.endDateFormatted,
        topCount: this.topCount
      };
      Axios.post(apiUrl, data)
        .then(({ data }) => {
          this.goBack();
        })
        .catch(error => {
          if (error.response) {
            let error_str = "";
            error.response.data.errors.forEach(error => {
              error_str += error + "\n";
            });
            this.snackbarText = error_str;
            this.snackbar = true;
          }
        })
        .finally(() => {
          this.isLoading = false;
        })
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
    allowedStartDates: val => {
      let dateVal = new Date(val);
      let nowDate = new Date();
      return dateVal > nowDate;
    },
    allowedEndDates(val) {
      let dateVal = new Date(val);
      let nowDate = new Date();
      return dateVal > nowDate;
    }
  }
};
</script>

<style lang="scss">
.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}
@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
