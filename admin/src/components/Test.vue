<template>
    <v-flex xs12 md4>
        <v-item>
            <v-card>
                <v-card-title>
                    <p class="headline mb-0">{{ test.question }}</p>
                </v-card-title>
                <v-divider/>
                <v-card-text>
                    <v-list subheader>
                        <v-subheader>Вариаты ответов</v-subheader>
                        <v-list-tile v-for="option in test.options" :key="option.id">
                            <v-list-tile-content>
                                <v-list-tile-title class="option-item">
                                    <v-icon v-if="option.isAnswer" color="primary">done</v-icon>
                                    {{ option.value }}
                                </v-list-tile-title>
                            </v-list-tile-content>
                        </v-list-tile>
                    </v-list>
                </v-card-text>
                <v-card-actions>
                    <v-spacer/>
                    <v-btn flat color="primary" icon>
                        <v-icon medium>edit</v-icon>
                    </v-btn>
                    <v-btn flat color="red" icon>
                        <v-icon medium>delete</v-icon>
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-item>
    </v-flex>
</template>

<script>
    export default {
        name: "Test",
        props: ['test'],

    }
</script>

<style scoped>
    p.headline {
        font-size: 0.9rem;
    }
</style>