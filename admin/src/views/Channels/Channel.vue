<template>
    <v-container>
        <p class="headline">Канал {{ name }}</p>
        <router-view></router-view>
    </v-container>
</template>

<script>
export default {
    name: 'Channel',
    props: ['name']
}
</script>

