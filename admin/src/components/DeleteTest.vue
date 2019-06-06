<template>
	<v-card>
		<v-card-title class="headline">
			Подтвердите действия
		</v-card-title>
		<v-card-text>
			<p>Вы действительно хотите безвосратно удалить тест <strong>"{{ question }}"</strong>?</p>
		</v-card-text>
		<v-card-actions>
			<v-spacer></v-spacer>
			<v-btn color="primary" flat @click="$emit('cancel')">Отмена</v-btn>
			<v-btn color="primary" flat @click="removeTest" :loading="loading" :disabled="loading">
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
	import apiEndpoints from './../apiEndpoints';
	export default {
		name: 'DeleteTest',
		data: () => ({
			question: '',
			testId: 0,
			quizId: 0,
			loading: false
		}),
		methods: {
			deleteTest(test) {
				this.question = test.question;
				this.testId = test.id;
				this.quizId = test.quizId;
			},
			removeTest() {
				let apiUrl = apiEndpoints.test.replace('testId', this.testId);
				this.loading = true;
				Axios.delete(apiUrl).then(() => {
					this.$emit('deleted', this.testId, this.quizId);
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
				});
			}
		}
	}
</script>
