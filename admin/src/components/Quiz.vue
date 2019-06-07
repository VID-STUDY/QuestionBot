<template>
    <section class="quiz-section mb-1">
        <h4>{{ quiz.startDate }} - {{ quiz.endDate }}</h4>
        <div>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                    <v-btn small icon flat color='primary' @click.stop="$emit('openNewTestDialog', quiz)" v-on="on">
                        <v-icon>add</v-icon>
                    </v-btn>
                </template>
                <span>Добавить тест</span>
            </v-tooltip>
            <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                    <v-btn small flat color='red' icon @click.stop="$emit('openDeleteQuizDialog', quiz)" v-on="on">
                        <v-icon>delete</v-icon>
                    </v-btn>
                </template>
                <span>Удалить викторину</span>
            </v-tooltip>
        </div>
        <v-item-group>
            <v-container grid-list-md>
                    <v-layout wrap>
                        <Test v-for="test in quiz.tests"
                            :key="test.id"
                            :test="test"
                            @openDeleteTestDialog="openDeleteTestDialogHandler"
                            @openEditTestDialog="openEditTestDialogHandler"></Test>
                    </v-layout>
            </v-container>
        </v-item-group>
        <v-divider></v-divider>
    </section>
</template>

<script>
import Test from './Test'
export default {
    name: 'Quiz',
    props: ['quiz', 'name'],
    components: {Test},
    methods: {
        openDeleteTestDialogHandler(test) {
            this.$emit('openDeleteTestDialog', test);
        },
        openEditTestDialogHandler(test) {
            this.$emit('openEditTestDialog', test, this.quiz);
        }
    }
}
</script>


