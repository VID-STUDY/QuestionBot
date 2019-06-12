<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-card>
    <v-card-title class="headline">Создать тест</v-card-title>
    <v-card-text>
      <v-container grid-list-md>
        <v-form ref="testForm">
          <v-layout wrap>
            <v-flex xs12>
              <v-text-field label="Вопрос"
                            v-model="test.question"
                            prepend-icon="help"
                            :rules="questionRules"
                            required></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-menu
                v-model="publishDateMenu"
                ref="dateMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="test.publishDateNF"
                lazy
                transition="scale-transition"
                offset-y
                full-width
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="test.publishDate"
                    label="День публикации"
                    prepend-icon="event"
                    :rules="publishDateRules"
                    @blur="test.publishDateNF = parseDate(test.publishDate)"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="test.publishDateNF" no-title scrollable first-day-of-week="1">
                  <v-spacer></v-spacer>
                  <v-btn flat color="primary" @click="publishDateMenu = false">Отмена</v-btn>
                  <v-btn flat color="primary" @click="$refs.dateMenu.save(test.publishDateNF)">Ок</v-btn>
                </v-date-picker>
              </v-menu>
            </v-flex>
            <v-flex xs12 md6>
              <v-menu
                ref="timeMenu"
                v-model="publishTimeMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="test.publishTime"
                lazy
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="test.publishTime"
                    label="Время публикации"
                    prepend-icon="access_time"
                    :rules="publishTimeRules"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker v-if="publishTimeMenu" v-model="test.publishTime" full-width format="24hr">
                  <v-spacer></v-spacer>
                  <v-btn flat color="primary" @click="publishTimeMenu = false">Отмена</v-btn>
                  <v-btn flat color="primary" @click="$refs.timeMenu.save(test.publishTime)">Ок</v-btn>
                </v-time-picker>
              </v-menu>
            </v-flex>
            <v-flex xs12>
              <upload-btn @file-update="fileUpdateHandler" ref="fileField" title="Файл">
                <template slot="icon">
                  <v-icon>attach_file</v-icon>
                </template>
              </upload-btn>
              <small v-if="test.file && test.file !== ''" class="grey--text">
                Что бы изменить файл, загрузите новый, иначе оставьте это поле пустым
              </small>
            </v-flex>
          </v-layout>
        </v-form>
      </v-container>
      <v-divider></v-divider>
      <v-list subheader>
        <v-subheader>Варианты ответов</v-subheader>
        <test-option
          v-for="option in test.options"
          :option="option"
          :key="option.id"
          @delete="removeOption"
          @answerChange="changeAnswer"
        />
      </v-list>
      <h3 class="headline mb-0">Добавить вариант ответа</h3>
      <v-form ref="newOptionForm">
        <v-layout row>
          <v-flex sm12>
            <v-text-field
              v-model="newOption.value"
              :rules="newOptionRules"
              label="Содержание варианта"
            ></v-text-field>
          </v-flex>
          <v-flex sm12>
            <v-btn flat color="accent" @click="addOption">
              <v-icon>add</v-icon>Добавить
            </v-btn>
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn @click="$emit('cancel')" flat color="primary">Отмена</v-btn>
      <v-btn @click="save" flat color="primary" :disabled="isLoading" :loading="isLoading">
        <template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>cached</v-icon>
          </span>
        </template>
        Сохранить</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import TestOption from "./Option";
import UploadButton from "vuetify-upload-button";
import apiEndpoints from "../apiEndpoints";
import Axios from "axios";
export default {
  name: "NewEditTest",
  components: { TestOption, "upload-btn": UploadButton },
  data: () => ({
    test: {
      id: 0,
      question: "",
      publishDateNF: "",
      publishTime: "",
      filePath: "",
      quizId: 0,
      options: [],
      clear() {
        this.question = "";
        this.publishDate = "";
        this.filePath = "";
        this.quizId = 0;
        this.options = [];
      }
    },
    newOption: {
      value: ""
    },
    lastId: 0,
    publishDateMenu: false,
    publishTimeMenu: false,
    isEditable: false,
    isLoading: false,
    startDate: null,
    endDate: null
  }),
  computed: {
    questionRules() {
      const rules = [];
      const requireRule = value => {
        return value !== "" || "Вы не указали вопрос";
      };
      rules.push(requireRule);
      return rules;
    },
    publishDateRules() {
      const rules = [];
      const requireRule = value => {
        return value !== "" || "Вы не указали дату публикации";
      };
      const betweenStartEndRule = value => {
        let dateVal = new Date(this.parseDate(value));
        return (dateVal >= this.startDate && dateVal <= this.endDate) || "Указанная дата не попадает в период викторины";
      }
      rules.push(requireRule);
      rules.push(betweenStartEndRule);
      return rules;
    },
    publishTimeRules() {
      const rules = [];
      const requireRule = value => {
        return value !== "" || "Вы не указали время публикации";
      };
      rules.push(requireRule);
      return rules;
    },
    newOptionRules() {
      const rules = [];
      const require = value => {
        return value.length > 0 || "Укажите значение варианта ответа";
      };
      rules.push(require);
      return rules;
    },
    computedPublishDateFormatted() {
      return this.formatDate(this.newTest.publishDate);
    }
  },
  watch: {
    'test.publishDateNF'(value) {
      this.test.publishDate = this.formatDate(this.test.publishDateNF);
    }
  },
  methods: {
    fileUpdateHandler(file) {
      this.test.filePath = file;
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
    newTest(quizId, startDate, endDate) {
      this.isEditable = false;
      this.test.clear();
      this.$refs.fileField.clear();
      this.test.quizId = quizId;
      this.startDate = new Date(this.parseDate(startDate));
      this.endDate = new Date(this.parseDate(endDate));
    },
    editTest(test, startDate, endDate) {
      this.isEditable = true;
      this.test.clear();
      this.$refs.fileField.clear();
      this.test.id = test.id;
      this.test.question = test.question;
      let [publishDate, publishTime] = test.publishDate.split(' ');
      this.test.publishDate = publishDate;
      this.test.publishTime = publishTime;
      this.test.publishDateNF = this.parseDate(publishDate);
      this.test.quizId = test.quizId;
      test.options.forEach(option => {
        this.test.options.push(option);
      });
      this.startDate = new Date(this.parseDate(startDate));
      this.endDate = new Date(this.parseDate(endDate));
    },
    addOption() {
      if (!this.$refs.newOptionForm.validate()) {
        return;
      }
      let currentId = this.lastId + 1;
      let newOption = {
        id: currentId,
        value: this.newOption.value,
        isAnswer: false
      };
      this.test.options.push(newOption);
      this.lastId = currentId;
      this.newOption.value = "";
    },
    removeOption(optionId) {
      let index = this.test.options.findIndex(
        option => option.id === optionId
      );
      this.test.options.splice(index, 1);
    },
    changeAnswer(optionId, value) {
      if (value) {
        let option = this.test.options.find(
          option => option.isAnswer === true && option.id !== optionId
        );
        if (option) {
          option.isAnswer = false;
        }
      }
    },
    error(error) {
       if (error.response) {
         let errorMsgs = error.response.data;
         let errorString = "";
         errorMsgs.forEach(error => {
           errorString += error + "\n";
         });
         this.$emit('error', errorString);
       } else {
          console.log(error)
         this.$emit('error', 'Что-то пошло не так...');
       }
    },
    uploadFile(testId) {
      let formData = new FormData();
      formData.append('file', this.test.filePath);
      let apiUrl = apiEndpoints.testsFiles.replace('testId', testId);
      return Axios.post(apiUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    },
    save() {
      if (!this.$refs.testForm.validate()) {
        return;
      }
      if (!this.checkIfAnswerExists()) {
        this.$emit("error", "Вы не указали правильный ответ");
        return;
      }
      this.isLoading = true;
      let apiUrl = apiEndpoints.tests;
      if (!this.isEditable) {
        Axios.post(apiUrl, this.test).then(({ data }) => {
          if (this.test.filePath !== "") {
            console.log(this.test.filePath);
            this.uploadFile(data.id).then(() => {
              this.$emit('created', data);
            }).catch(error => {
              this.error(error);
            }).finally(() => {
              this.isLoading = false;
            });
          } else {
            this.$emit('created', data);
          }
        }).catch(error => {
          this.error(error);
        }).finally(() => {
          this.isLoading = false;
        });
      } else {
        apiUrl += '/' + this.test.id;
        Axios.put(apiUrl, this.test).then(({data}) => {
          if (this.test.filePath !== "") {
            this.uploadFile(data.id).then(() => {
              this.$emit('updated', data);
            }).catch(error => {
              this.error(error);
            }).finally(() => {
              this.isLoading = false;
            });
          } else {
            this.$emit('updated', data);
          }
        }).catch(error => {
          this.error(error)
        }).finally(() => {
          this.isLoading = false;
        })
      }
    },
    checkIfAnswerExists() {
      let option = this.test.options.find(
        option => option.isAnswer === true
      );
      return !!option;
    }
  }
};
</script>

