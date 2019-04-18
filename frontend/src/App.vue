<template>
  <div id="app">
    <div>
      <div v-for="o in todos" v-bind:key="o">
        <Todo :todo="o" :parent_container="todos" :master_lock="false"/>
      </div>
    </div>
    <h3 v-if="error">Error backend not available</h3>
    <div v-else @click="add" id="add" class="todo" style="text-align:center">
      <b>+</b>
    </div>
  </div>
</template>

<script>
import Todo from './components/Todo.vue'
const axios = require('axios');
axios.defaults.headers.common['Authorization'] = 'Token 1234';
export default {
  name: 'app',
  components: {
    Todo
  },
  data(){
    return{
      todos:[],
      error:true
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
      this.error = false;
    })
  }
}
</script>

<style>
</style>
