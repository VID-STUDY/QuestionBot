<template>
  <v-container>
    <v-dialog v-model="testDialog" max-width="600px">
      <NewEditTest ref="newEditTests" @cancel="testDialog = false" @created="testCreatedHandler" @updated="testUpdatedHandler" @error="testErrorHandler"/>
    </v-dialog>
    <v-dialog v-model="deleteDialog" max-width="400px">
      <DeleteTest ref="deleteTest" @cancel='deleteDialog = false' @deleted="testDeletedHandler" @error="testErrorHandler"></DeleteTest>
    </v-dialog>
    <v-dialog v-model="deleteQuizDialog" max-width="400px">
      <DeleteQuiz ref="deleteQuiz" @cancel='deleteQuizDialog = false' @deleted="quizDeletedHandler" @error="testErrorHandler"/>
    </v-dialog>
    <div class="vld-parent">
      <loading :active.sync="isLoading"></loading>
    </div>
    <template v-if="hasError">
      <v-layout wrap>
        <v-flex xs-12>
          <div class="d-flex justify-center align-center">
            <p class="text-xs-center font-weight-bold">{{ errorMessage }}</p>
          </div>
        </v-flex>
      </v-layout>
    </template>
    <template v-else>
      <v-layout wrap>
        <v-flex xs-12>
          <Quiz
            v-for="quiz in quizzes"
            :key="quiz.id"
            :quiz="quiz"
            :name="name"
            @openNewTestDialog="openNewTestDialog"
            @openDeleteTestDialog="openDeleteTestDialog"
            @openEditTestDialog="openEditTestDialog"
            @openDeleteQuizDialog="openDeleteQuizDialog"
          ></Quiz>
        </v-flex>
      </v-layout>
      <v-fab-transition>
        <v-btn
          color="primary"
          dark
          fab
          fixed
          right
          bottom
          :to="{name: 'newQuiz', params: {name: name}}"
        >
          <v-icon>add</v-icon>
        </v-btn>
      </v-fab-transition>
    </template>
    <v-snackbar v-model="snackbar" bottom :color="snackColor">
      {{ snackText }}
      <v-btn flat icon @click="snackbar = false">
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import Axios from "axios";
import apis from "../../apiEndpoints";
import Loading from "vue-loading-overlay";
import Quiz from "../../components/Quiz";
import NewEditTest from '../../components/NewEditTest'
import DeleteTest from '../../components/DeleteTest'
import DeleteQuiz from '../../components/DeleteQuiz'
import "vue-loading-overlay/dist/vue-loading.css";
export default {
  name: "QuizzesList",
  props: ["name"],
  title () {
    return `Викторины - ${this.name}`
  },
  data: () => ({
    quizzes: [],
    hasError: false,
    errorMessage: "",
    isLoading: false,
    testDialog: false,
    deleteDialog: false,
    deleteQuizDialog: false,
    snackbar: false,
    snackColor: 'info',
    snackText: ''
  }),
  components: { Quiz, NewEditTest, Loading, DeleteTest, DeleteQuiz },
  methods: {
    openNewTestDialog(quiz) {
      this.$refs.newEditTests.newTest(quiz.id, quiz.startDate, quiz.endDate);
      this.testDialog = true;
    },
    openDeleteTestDialog(test) {
      this.$refs.deleteTest.deleteTest(test);
      this.deleteDialog = true;
    },
    openEditTestDialog(test, quiz) {
      this.$refs.newEditTests.editTest(test, quiz.startDate, quiz.endDate);
      this.testDialog = true;
    },
    openDeleteQuizDialog(quiz) {
      this.$refs.deleteQuiz.prepare(quiz);
      this.deleteQuizDialog = true;
    },
    getQuizzes() {
        this.quizzes = [];
      let apiUrl = apis.channelQuizzes.replace("channelName", this.name);
      Axios.get(apiUrl)
        .then(({ data }) => {
          data.forEach(quiz => {
            this.quizzes.push(quiz);
          });
        })
        .catch(error => {
          this.hasError = true;
          if (error.response) {
            error.response.data.erorrs.forEach(e => {
              this.errorMessage += e;
            });
          } else {
            this.errorMessage = "Что-то пошло не так...";
          }
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    showError(error) {
      this.snackColor = 'error';
      this.snackText = error;
      this.snackbar = true;
    },
    success(msg) {
      this.snackColor = 'success';
      this.snackText = msg;
      this.snackbar = true;
    },
    testCreatedHandler(test) {
      let quiz = this.quizzes.find((quiz) => quiz.id === test.quizId);
      quiz.tests.push(test);
      this.success('Тест добавлен!');
      this.testDialog = false;
    },
    testUpdatedHandler(updatedTest) {
      let quiz = this.quizzes.find((quiz) => quiz.id === updatedTest.quizId);
      let test = quiz.tests.find((test) => test.id === updatedTest.id);
      test.question = updatedTest.question;
      test.publishDate = updatedTest.publishDate;
      test.options = [];
      updatedTest.options.forEach(option => {
        test.options.push(option);
      });
      test.file = updatedTest.file;
      this.success('Тест обновлён!');
      this.testDialog = false;
    },
    testErrorHandler(error) {
      this.showError(error);
    },
    testDeletedHandler(testId, quizId) {
      let quiz = this.quizzes.find((quiz) => quiz.id === quizId);
      let testIndex = quiz.tests.findIndex((test) => test.id === testId);
      quiz.tests.splice(testIndex, 1);
      this.deleteDialog = false;
      this.success('Тест удалён!');
    },
    quizDeletedHandler(quizId) {
      let index = this.quizzes.findIndex(quiz => quiz.id === quizId);
      this.quizzes.splice(index, 1);
      this.deleteQuizDialog = false;
      this.success('Викторина удалена!');
    }
  },
  mounted() {
    this.getQuizzes();
  },
  watch: {
    '$route'() {
      this.getQuizzes();
    }
  }
};
</script>

