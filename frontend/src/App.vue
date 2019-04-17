<template>
  <div id="app">
    <div class="row-fluid">
      <div v-for="o in data" v-bind:key="o" class="accordion-toggle" :data-target="'co-'+o.id">
        <Todo :todo="o" :parent_container="data" :master_lock="false"/>
      </div>
    </div>
    <div @click="add" class="todo" style="text-align:center">
      <b>+</b>
    </div>
  </div>
</template>

<script>
import Todo from './components/Todo.vue'

export default {
  name: 'app',
  components: {
    Todo
  },
  data(){
    return{
      data:[{"id":1,"title":"todo1","locked":false,"children":[
            {"id":3,"title":"todo1.1","locked":true},
            {"id":4,"title":"todo1.2","locked":false}]},
            {"id":2,"title":"todo2","locked":true}
      ]
    }
  },
  methods:{
    add(){
      var obj = {"title":"new todo","locked":false};
      this.data.push(obj);
    }
  }
}
</script>

<style>
</style>
