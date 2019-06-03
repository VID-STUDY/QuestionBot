<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <v-container>
        <v-layout wrap>
            <v-flex xs12>
                <v-form ref="form">
                    <v-card>
                        <v-card-title primary-title>
                            <h3 class="headline mb-0">Добавить новый канал</h3>
                            <span class="grey--text">Перед заполнением поля, сделайте канал публичным, задайте ему ссылку, добавьте туда бота и сделайте его администратором.</span>
                        </v-card-title>
                        <v-card-text>
                            <v-text-field
                                :error-messages="newChannel.errorMessages"
                                prepend-icon="link"
                                v-model="newChannel.url"
                                :rules="rules"
                                label="Ссылка на канал или юзернэйм"></v-text-field>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn flat @click="save" сolor="primary"
                                    :disabled="loading"
                                    :loading="loading">
                                <template v-slot:loader>
                                    <span class="custom-loader">
                                        <v-icon light>cached</v-icon>
                                    </span>
                                </template>
                                <v-icon left>save</v-icon>
                                Добавить
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
    import axios from 'axios/index'
    import apis from '../apiEndpoints'
    export default {
        name: "AddChannel",
        data: () => ({
            newChannel: {
                url: '',
                hasError: false,
                errorMessages: []
            },
            valid: true,
            snackbar: false,
            snackbarText: '',
            snackbarColor: 'info',
            loading: false
        }),
        computed: {
            rules() {
                const rules = [];
                const url_rule = value => {
                    let url_re = /https?:\/\/(t(elegram)?\.me|telegram\.org)\/([a-z0-9\_]){5,32}/gi;
                    let tg_username_re = /@[a-z0-9\_]/gi;
                    return url_re.test(value) || tg_username_re.test(value) || 'Введите Telegram-ссылку на ваш канал'
                };
                rules.push(url_rule);
                return rules;
            }
        },
        methods: {
            save () {
                if (!this.$refs.form.validate()) {
                    return;
                }
                this.loading = true;
                axios.post(apis.channels, {channelName: this.newChannel.url}).then(({data}) => {
                    if (data.errors) {
                        let error_str = '';
                        error.errors.forEach(error => {
                           error_str += error + '\n';
                        });
                        this.snackbarText = error_str;
                        this.snackbarColor = 'error';
                        this.snackbar = true;
                    }
                    this.$root.$emit('newChannelAdded', data);
                    this.newChannel.url = '';
                    this.snackbarText = `Добавлен канал ${data.channelTitle}`;
                    this.snackbarColor = 'success';
                    this.snackbar = true;
                }).catch((error) => {
                    if (error.response) {
                        let error_str = '';
                        error.response.data.errors.forEach(error => {
                           error_str += error + '\n';
                        });
                        this.snackbarText = error_str;
                        this.snackbarColor = 'error';
                        this.snackbar = true;
                    }
                }).finally(() => {
                    this.loading = false;
                });
            }
        }
    }
</script>

<style scoped>

</style>