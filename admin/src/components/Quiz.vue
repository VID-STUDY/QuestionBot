<template>
    <section class="quiz-section mb-1">
        <h4>{{ quiz.startDate }} - {{ quiz.endDate }}</h4>
        <div class="d-flex justify-end align-center">
            <v-btn :to="{ name: 'editQuiz', params: {name: name, id: quiz.id} }" flat color='primary'>
                <v-icon>edit</v-icon>
            </v-btn>
            <v-btn flat color='danger'>
                <v-icon>delete</v-icon>
            </v-btn>
        </div>
        <v-carousel hide-delimiters>
            <v-carousel-item v-for="test in quiz.tests" :key="test.id">
                <Test :test='test'></Test>
            </v-carousel-item>
        </v-carousel>
        <v-divide></v-divide>
    </section>
</template>

<script>
import Test from './Test'
export default {
    name: 'Quiz',
    props: ['quiz', 'name'],
    components: {Test}
}
</script>


