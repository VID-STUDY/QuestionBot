<template>
    <v-flex xs12 md4>
        <v-item>
            <div class="test-item">
                <v-card >
                    <v-card-title>
                        <p class="question mb-0">{{ test.question }}</p>
                    </v-card-title>
                    <v-divider/>
                    <v-card-text>
                        <p><span class="font-weight-bold">Дата пубикации: </span>{{ test.publishDate }} <span v-if="test.published"><v-icon right color='success'>check</v-icon></span> </p>
                        <v-list subheader>
                            <v-subheader>Варианты ответов</v-subheader>
                            <v-list-tile v-for="option in test.options" :key="option.id" class="option-item" avatar>
                                <v-list-tile-avatar>
                                    <v-checkbox color="primary" :disabled="true" v-model="option.isAnswer"/>
                                </v-list-tile-avatar>
                                <v-list-tile-content>
                                    <v-list-tile-title class="option-item-title">
                                        {{ option.value }}
                                    </v-list-tile-title>
                                </v-list-tile-content>
                            </v-list-tile>
                        </v-list>
                        <p class="mt-3"><span class="font-weight-bold">Всего ответов: </span>{{ test.answersCount }}</p>
                        <p v-if="test.file && test.file !== ''">
                            <span class="font-weight-bold">Файл: </span>
                            {{ test.file }}
                        </p>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer/>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn flat color="primary" icon @click.stop="$emit('openEditTestDialog', test)" v-on="on">
                                    <v-icon medium>edit</v-icon>
                                </v-btn>
                            </template>
                            <span>Редактировать</span>
                        </v-tooltip>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                                <v-btn flat color="red" icon @click.stop="$emit('openDeleteTestDialog', test)" v-on="on">
                                    <v-icon medium>delete</v-icon>
                                </v-btn>
                            </template>
                            <span>Удалить</span>
                        </v-tooltip>

                    </v-card-actions>
                </v-card>
            </div>
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
            line-height: 18px;
        }
    }
</style>