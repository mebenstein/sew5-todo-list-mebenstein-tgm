<template>
  <div id="app">
    <div>
      <div v-for="o in todos" v-bind:key="o">
        <Todo :todo="o" :parent_container="todos" :master_lock="false"/>
      </div>
    </div>
    <div @click="add" class="todo" style="text-align:center">
      <b>+</b>
    </div>
  </div>
</template>

<script>
import Todo from './components/Todo.vue'
const axios = require('axios');

export default {
  name: 'app',
  components: {
    Todo
  },
  data(){
    return{
      todos:[]
    }
  },
  methods:{
    add(){
      var obj = {"title":"new todo","locked":false};
      axios.post("http://localhost:9000/add",obj).then(response =>{
        obj["id"] = response.data;
        this.todos.push(obj);
      })
    }
  },
  mounted(){
    axios.get("http://localhost:9000/get").then(response => {
      this.todos = response.data;
    })
  }
}
</script>

<style>
</style>
