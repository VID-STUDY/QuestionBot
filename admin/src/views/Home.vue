<template>
  <v-container>
    <v-layout row justify-center>
      <section class="mt-4">
        <h1 class="text-xs-center">Добро пожаловать в административную панель Telegram бота QuestionBot!</h1>
        <div class="mt-3">
          <p class="subheading text-xs-center">Данная система позволяет управлять каналами, создавать тесты и опросы, которые публикуются только в то время, которое выберите вы, мониторить пользователей и рейтинги</p>
        </div>
        <v-divider class="my-3"></v-divider>
        <div class="title mb-3 text-xs-center">Для начала работы откройте меню слева в верхнем углу.</div>
      </section>
    </v-layout>
  </v-container>
</template>

<script>

  export default {
    name: "Home",
    title: "QuestionBot Administration"
  }
</script>
