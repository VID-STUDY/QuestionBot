<template>
	<v-card>
		<v-card-title class="headline">
			Подтвердите действие
		</v-card-title>
		<v-card-text>
			<p>Вы действительно хотите безвозвратно удалить викторину <strong>{{ startDate }}</strong> - <strong>{{ endDate }}</strong>? Так же станут недоступны рейтинги по этой викторине.</p>
		</v-card-text>
		<v-card-actions>
			<v-spacer></v-spacer>
			<v-btn flat @click="$emit('cancel')" color="primary">Отмена</v-btn>
			<v-btn flat color="primary" @click="removeQuiz" :loading="loading" :disabled="loading">
				<template v-slot:loader>
          <span class="custom-loader">
            <v-icon light>cached</v-icon>
          </span>
        </template>
				Удалить
			</v-btn>
		</v-card-actions>
	</v-card>
</template>

<script>
	import Axios from 'axios';
	import apiEndpoints from '../apiEndpoints';
	export default {
		name: 'DeleteQuiz',
		data: () => ({
			quizId: 0,
			startDate: '',
			endDate: '',
			loading: false
		}),
		methods: {
			prepare(quiz) {
				this.quizId = quiz.id;
				this.startDate = quiz.startDate;
				this.endDate = quiz.endDate;
			},
			removeQuiz() {
				let apiUrl = apiEndpoints.quizzes.replace('quizId', this.quizId);
				this.loading = true;
				Axios.delete(apiUrl).then(() => {
					this.$emit('deleted', this.quizId)
				}).catch(error => {
					if (error.response) {
         		let errorMsgs = error.response.data;
         		let errorString = "";
         		errorMsgs.forEach(error => {
          		errorString += error + "\n";
         		});
         		this.$emit('error', errorString);
       		} else {
         		this.$emit('error', "Что-то пошло не так...");
       		}
				}).finally(() => {
					this.loading = false;
				})
			}
		}
	}
</script>