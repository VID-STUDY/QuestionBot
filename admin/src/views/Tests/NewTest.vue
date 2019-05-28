<template>
    <v-container>
        <v-layout wrap>
            <v-flex xs12>
                <v-form ref="form">
                    <v-card>
                        <v-card-title>
                            <h3 class="headline mb-0">Создать новый тест</h3>
                        </v-card-title>
                        <v-card-text>
                            <v-text-field
                                prepend-icon="help_outline"
                                v-model="newTest.question"
                                :rules="testRules"
                                label="Вопрос"></v-text-field>
                            <v-divider/>
                            <v-list subheader>
                                <v-subheader>Варианты ответов</v-subheader>
                                <test-option v-for="option in newTest.options"
                                             :option="option"
                                             :key="option.id"
                                             @delete="removeOption"
                                             @answerChange="changeAnswer"/>
                            </v-list>
                            <h3 class="headline mb-0">Добавить вариант ответа</h3>
                            <v-form ref="newOptionForm">
                                <v-layout row>
                                    <v-flex sm12>
                                        <v-text-field
                                                v-model="newOption.value"
                                                :rules="newOptionRules"
                                                label="Содержание варианта"></v-text-field>
                                    </v-flex>
                                    <v-flex sm12>
                                        <v-btn flat color="accent" @click="addOption">
                                            <v-icon>add</v-icon> Добавить
                                        </v-btn>
                                    </v-flex>
                                </v-layout>
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn flat @click="back">
                                <v-icon left>arrow_back</v-icon> Назад
                            </v-btn>
                            <v-btn @click="saveAndContinue" flat color="accent"> Сохранить и продолжить
                            </v-btn>
                            <v-btn @click="saveAndBack" flat color="primary"> Сохранить
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-form>
            </v-flex>
        </v-layout>
        <v-snackbar v-model="snackbar"
                    bottom
                    :color="snackbarColor">
            {{ snackbarText }}
            <v-btn
                   flat
                   @click="snackbar = false"><v-icon left>close</v-icon>Закрыть</v-btn>
        </v-snackbar>
    </v-container>
</template>

<script>
    import TestOption from '../../components/Option'
    import axios from 'axios'
    import apis from '../../apiEndpoints'
    export default {
        name: "NewTest",
        data: () => ({
            newTest: {
                question: '',
                options: [],
            },
            newOption: {
                value: '',
            },
            lastId: 0,
            snackbar: false,
            snackbarColor: 'info',
            snackbarText: ''
        }),
        props: ['name'],
        computed: {
            testRules() {
                const rules = [];
                const require = value => {
                    return value.length > 0 || 'Напишите вопрос'
                };
                const questionMark = value => {
                    return value.slice(-1) === '?' || 'Вопрос должен заканчиваться восклицательным знаком'
                };
                rules.push(require);
                // rules.push(questionMark);
                return rules;
            },
            newOptionRules() {
                const rules = [];
                const require = value => {
                    return value.length > 0 || 'Укажите значение варианта ответа'
                };
                rules.push(require);
                return rules;
            }
        },
        methods: {
            addOption() {
                if (!this.$refs.newOptionForm.validate()){
                    return;
                }
                let currentId = this.lastId + 1;
                let newOption = {
                    id: currentId,
                    value: this.newOption.value,
                    isAnswer: false
                };
                this.newTest.options.push(newOption);
                this.lastId = currentId;
                this.newOption.value = '';
            },
            removeOption(optionId) {
                let index = this.newTest.options.findIndex(option => option.id === optionId);
                this.newTest.options.splice(index, 1);
            },
            changeAnswer(optionId, value) {
                if (value) {
                    let option = this.newTest.options.find(option => option.isAnswer === true && option.id !== optionId);
                    if (option) {
                        option.isAnswer = false;
                    }
                }
            },
            error(msg) {
                this.snackbarText = msg;
                this.snackbarColor = 'danger';
                this.snackbar = true;
            },
            success(msg) {
                this.snackbarText = msg;
                this.snackbarColor = 'success';
                this.snackbar = true;
            },
            checkIfAnswerExists() {
                let option = this.newTest.options.find(option => option.isAnswer === true);
                return !!option;
            },
            saveAndContinue() {
                if (!this.checkIfAnswerExists()) {
                    this.error('Вы не указали правильный вариант ответа');
                    return;
                }
                axios.post(apis.channelTests.replace('channelName', this.name), this.newTest)
                    .then(() => {
                        this.newTest.question = '';
                        this.newTest.options.splice(1, this.newTest.options.length - 1);
                        this.success('Тест успешно добавлен');
                    })
                    .catch(error => {
                        if (error.response) {
                            let errorMsgs = error.response.data;
                            let errorString = '';
                            errorMsgs.forEach(error => {
                                errorString += error + '\n';
                            });
                            this.error(errorString);
                        }
                    });
            },
            saveAndBack() {
                if (!this.checkIfAnswerExists()) {
                    this.error('Вы не указали правильный вариант ответа');
                    return;
                }
                axios.post(apis.channelTests.replace('channelName', this.name), this.newTest)
                    .then(() => {
                        this.success('Тест успешно добавлен');
                        this.back();
                    })
                    .catch(error => {
                        if (error.response) {
                            let errorMsgs = error.response.data;
                            let errorString = '';
                            errorMsgs.forEach(error => {
                                errorString += error + '\n';
                            });
                            this.error(errorString);
                        }
                    });
            },
            back() {
                this.$router.push({name: 'channelTests', params: {name: this.name}});
            },
            save() {

            }
        },
        components: {TestOption}
    }
</script>

<style scoped>

</style>