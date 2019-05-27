<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <v-container>
        <div class="vld-parent">
            <loading :active.sync="isLoading"> </loading>
        </div>
        <template v-if="hasError">
            <v-layout wrap>
                <v-flex xs12>
                    <div class="d-flex justify-center align-center">
                        <p class="text-xs-center font-weight-bold">{{ errorMessage }}</p>
                    </div>
                </v-flex>
            </v-layout>
        </template>
        <template v-else>
            <template v-if="tests.length > 0">
                <v-item-group>
                    <v-container grid-list-md>
                        <v-layout wrap>
                            <Test v-for="test in tests"
                                :key="test.id"
                                :test="test"></Test>
                        </v-layout>
                    </v-container>
                </v-item-group>
            </template>
            <template v-else>
                <v-layout wrap>
                    <v-flex xs12>
                        <div class="d-flex justify-center align-center">
                            <p class="text-xs-center font-weight-bold">Для этого канала тесты или опросы ещё не созданы. Для этого нажмите на кнопку справа снизу.</p>
                        </div>
                    </v-flex>
                </v-layout>
            </template>
            <v-speed-dial
                bottom
                right
                fixed
                direction="top"
                transition="slide-y-transition">
                <template v-slot:activator>
                    <v-btn
                        fab
                        dark
                        color="primary">
                        <v-icon>add</v-icon>
                        <v-icon>close</v-icon>
                    </v-btn>
                </template>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn
                            fab
                            dark
                            small
                            color="accent">
                            <v-icon>assignment</v-icon>
                        </v-btn>
                    </template>
                    <span>Создать тест</span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                        <v-btn
                            fab
                            dark
                            small
                            color="accent">
                            <v-icon>chat_bubble_outline</v-icon>
                        </v-btn>
                    </template>
                    <span>Создать опрос</span>
                </v-tooltip>
            </v-speed-dial>
        </template>
    </v-container>
</template>

<script>
    import axios from 'axios/index'
    import apis from '../../apiEndpoints'
    import Test from './Test'
    import Loading from 'vue-loading-overlay'
    import 'vue-loading-overlay/dist/vue-loading.css'
    export default {
        name: "ChannelTests",
        props: ['name'],
        data: () => ({
           tests: [],
            hasError: false,
            errorMessage: '',
            isLoading: false
        }),
        methods: {
            getChannelTests() {
                this.isLoading = true;
                axios.get(apis.channelTests.replace('channelName', this.name))
                    .then(({data}) => {
                        this.tests.length = 0;
                        data.forEach(test => {
                           this.tests.push(test);
                        });
                    })
                    .catch(error => {
                        if (error.response) {
                            this.hasError = true;
                            error.response.data.errors.forEach(e => {
                                this.errorMessage += e;
                            });
                        }
                    })
                    .finally(() => {
                        this.isLoading = false;
                    });
            }
        },
        mounted() {
            this.getChannelTests();
        },
        components: {Loading, Test},
        watch: {
            '$route' (to, from) {
                this.getChannelTests();
            }
        }
    }
</script>

<style scoped>
    .v-item-group > * {
        cursor: default;
    }
</style>