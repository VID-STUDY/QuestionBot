<template>
    <v-flex xs12 md4>
        <v-item>
            <v-card>
                <v-card-title>
                    <p class="question mb-0">{{ test.question }}</p>
                </v-card-title>
                <v-divider/>
                <v-card-text>
                    <v-list subheader>
                        <v-subheader>Вариаты ответов</v-subheader>
                        <v-list-tile v-for="option in test.options" :key="option.id" class="option-item" avatar>
                            <v-list-tile-avatar>
                                <v-checkbox color="primary" :disabled="!option.isAnswer" @change="checkboxChange" v-model="option.isAnswer"/>
                            </v-list-tile-avatar>
                            <v-list-tile-content>
                                <v-list-tile-title class="option-item-title">
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

<style scoped lang="scss">
    p.question {
        font-size: 1rem;
        font-weight: bold;
    }
    .option-item {
        height: 24px;
        &-title {
            height: 12px;
            line-height: 12px;
        }
    }
</style>