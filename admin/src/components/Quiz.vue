<template>
    <section class="quiz-section mb-1">
        <h4>{{ quiz.startDate }} - {{ quiz.endDate }}</h4>
        <div>
            <v-spacer></v-spacer>
            <v-btn small icon flat color='primary' @click.stop="$emit('openNewTestDialog', quiz)">
                <v-icon>add</v-icon>
            </v-btn>
            <v-btn small flat color='red' icon @click.stop="$emit('openDeleteQuizDialog', quiz)">
                <v-icon>delete</v-icon>
            </v-btn>
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


