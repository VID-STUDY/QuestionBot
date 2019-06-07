<template>
    <v-list-tile avatar>
        <v-list-tile-avatar>
            <v-checkbox color="primary" @change="checkboxChange" v-model="option.isAnswer"/>
        </v-list-tile-avatar>
        <v-list-tile-content>
            <v-list-tile-title>{{ option.value }}</v-list-tile-title>
        </v-list-tile-content>
        <v-list-tile-action>
            <v-tooltip>
                <template v-slot:activator="on">
                    <v-btn flat icon color="red" @click="deleteClick" v-on="on">
                        <v-icon>delete</v-icon>
                    </v-btn>
                </template>
                <span>Удалить</span>
            </v-tooltip>
        </v-list-tile-action>
    </v-list-tile>
</template>

<script>
    export default {
        name: "TestOption",
        props: ['option'],
        methods: {
            deleteClick() {
                this.$emit('delete', this.option.id);
            },
            checkboxChange() {
                this.$emit('answerChange', this.option.id, this.option.isAnswer);
            }
        }
    }
</script>

<style scoped>

</style>