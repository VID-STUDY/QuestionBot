<template>
    <v-container>
        <v-layout wrap>
            <v-flex xs12>
                <v-card>
                    <v-toolbar color="primary" dark flat dense cad>
                      <v-toolbar-title class="subheading">Настройки</v-toolbar-title>
                      <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-form ref="form">
                            <v-text-field v-model="rightAnswerPoints"
                                          label="Очки за правильный ответ"
                                           :rules="rightAnswerPointsRules"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn flat color="primary" ripple @click="setSettings" :loading="loading" :disabled="loading">
                            <v-icon left>save</v-icon>
                            Сохранить
                            <template v-slot:loader>
                              <span class="custom-loader">
                                <v-icon light>cached</v-icon>
                              </span>
                            </template>
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
        <v-snackbar color="success" v-model="snackbar">
            Настройки сохранены
        </v-snackbar>
    </v-container>
</template>

<script>
    import apiEndpoints from "../apiEndpoints";
    import axios from 'axios'
    export default {
        title: "Настройки",

        name: "Settings",
        data: () => ({
            rightAnswerPoints: 0,
            snackbar: false,
            loading: false
        }),
        methods: {
            getSettings() {
                let apiUrl = apiEndpoints.settings;
                axios.get(apiUrl).then(({data}) => {
                    this.rightAnswerPoints = data.rightAnswerPoints;
                });
            },
            setSettings() {
                if (!this.$refs.form.validate()) {
                    return;
                }
                this.loading = true;
                let data = {
                    rightAnswerPoints: this.rightAnswerPoints
                };
                let apiUrl = apiEndpoints.settings;
                axios.post(apiUrl, data).then(() => {
                    this.snackbar = true;
                }).finally(() => {
                    this.loading = false;
                })
            }
        },
        computed: {
            rightAnswerPointsRules() {
                const rules = [];
                const requiredRule = value => {
                    return value !== '' || "Укажите количество баллов за правильный ответ";
                };
                const isNumberRule = value => {
                    return !isNaN(value) || "Количество баллов должно быть числом"
                };
                const moreThanZero = value => {
                    if (value !== '' && !isNaN(value)) {
                        return +value > 0 || "Количество баллов должно быть больше нуля";
                    }
                };
                rules.push(requiredRule);
                rules.push(isNumberRule);
                rules.push(moreThanZero);
                return rules;
            }
        },
        created() {
            this.getSettings();
        }
    }
</script>

<style scoped>

</style>