<template>
    <v-layout>
        <template v-if="error">
            <v-flex xs12>
                <p class="font-weight text-xs-center display-1">{{ errorMessage }}</p>
                <v-layout justify-center>
                  <v-btn color="primary" @click="getQuizzes" :loading="loading" :disabled="loading">
                      <template v-slot:loader>
                          <span class="custom-loader">
                              <v-icon light>cached</v-icon>
                          </span>
                      </template>
                    <v-icon left>cached</v-icon>
                    Обновить
                  </v-btn>
                </v-layout>
            </v-flex>
        </template>
        <template v-else>
            <v-flex xs12>
                <v-subheader>Рейтинги канала</v-subheader>
                <v-card v-for="quiz in quizzes" :key="quiz.id" class="mt-2">
                    <v-card-title class="font-weight-bold">
                        Викторина
                        <v-subheader>{{ quiz.startDate }} - {{ quiz.endDate }}</v-subheader>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-list two-line subheader>
                            <v-subheader>Рейтинг тестов по количеству ответов</v-subheader>
                            <v-list-tile v-for="test in quiz.tests" :key="test.id">
                                <v-list-tile-content>
                                    <v-list-tile-title>{{ test.question }}</v-list-tile-title>
                                    <v-list-tile-sub-title>Дата публикации: {{ test.publishDate }}</v-list-tile-sub-title>
                                    <v-list-tile-sub-title>Количество ответов: {{ test.answersCount }}</v-list-tile-sub-title>
                                </v-list-tile-content>
                            </v-list-tile>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-flex>
        </template>
    </v-layout>
</template>

<script>
    import apiEndpoints from '../../apiEndpoints'
    import axios from 'axios'
    export default {
        name: "ChannelRating",
        props: ['name'],
        data: () => ({
            quizzes: [],
            error: false,
            errorMessage: '',
            loading: false
        }),
        methods: {
            getQuizzes() {
                let apiUrl = apiEndpoints.channelRatings.replace('channelName', this.name);
                this.loading = true;
                axios.get(apiUrl).then(({data}) => {
                    this.error = false;
                    this.quizzes = [];
                    data.forEach(quiz => {
                        this.quizzes.push(quiz);
                    })
                }).catch(error => {
                    this.error = true;
                    if (error.response) {
                        let errorStr = '';
                        error.response.data.errors.forEach(errorMsg => {
                            errorStr += errorMsg;
                        });
                        this.errorMessage = errorStr;
                    } else {
                        this.errorMessage = 'Что-то пошло не так...';
                    }
                }).finally(() => {
                    this.loading = false;
                });
            }
        },
        watch: {
            '$route'() {
                this.getQuizzes();
            }
        },
        created() {
            this.getQuizzes();
        },
    }
</script>