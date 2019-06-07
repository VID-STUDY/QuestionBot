<template>
    <v-container>
        <v-layout wrap row>
            <v-flex xs12>
                <p class="headline ml-3">Канал {{ name }}</p>
            </v-flex>
        </v-layout>
        <router-view></router-view>
    </v-container>
</template>

<script>
export default {
    name: 'Channel',
    props: ['name']
}
</script>

