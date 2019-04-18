<template>
  <div :class="[todo.locked||master_lock ? 'lock' : '','todo']" :id="todo.id">
    <div style="white-space: nowrap;">
      <h1  @input="updateTitle" class="sameline" :contenteditable="todo.locked||master_lock?false:true">{{ todo.title }}</h1>
      <div class="sameline" @click="togglLockstate">
        <img alt="lock" :src="todo.locked||master_lock?'https://image.flaticon.com/icons/svg/26/26053.svg':'https://cdn0.iconfinder.com/data/icons/tools-66/24/unlock-512.png'" width="20" >
      </div>
      <div class="sameline" @click="del">
        <img alt="delete" src="https://cdn4.iconfinder.com/data/icons/email-2-2/32/Trash-Email-Bin-512.png" width="20">
      </div>
    </div>
    <li>
      <ul v-for="o in todo.children" v-bind:key="o"><Todo :todo="o" :parent_container="todo.children" :master_lock="todo.locked"/></ul>
    </li>
    <div class="add todo"  @click="add" style="text-align:center">
        <b>+</b>
    </div>
  </div>
</template>
<script>
const axios = require('axios');

export default {
  name: 'Todo',
  props: {
    todo: {
      type: Object,
      required:true,
      validator:function(value){
        return value["id"] != undefined && value["title"] != undefined && value["locked"] != undefined;
      }
    },
    master_lock: Boolean,
    parent_container: Array
  },
  methods:{
    getRaw(){
      return {"title":this.todo.title,
              "locked":this.todo.locked};
    },
    togglLockstate(){
      if(this.master_lock)return;
      this.todo.locked = ! this.todo.locked;
      
      axios.post("http://localhost:9000/set/"+this.todo.id,this.getRaw()).then(() =>{
        //this.todo = response.data;
      })
      
    },
    del(){
      if(this.todo.locked || this.master_lock)return;
       axios.post("http://localhost:9000/del/"+this.todo.id).then(() =>{
        this.parent_container.splice( this.parent_container.indexOf(this.todo), 1 );
      })
    },
    add(){
      if(this.todo.locked || this.master_lock)return;
      var obj = {"title":"new todo","locked":false,"parent":this.todo.id};
      axios.post("http://localhost:9000/add",obj).then(response =>{
        obj["id"] = response.data;
        this.todo.children.push(obj);
      })
    },
    updateTitle(event){
      axios.post("http://localhost:9000/set/"+this.todo.id,{"title":event.target.textContent}).then(() =>{
        //this.todo = response.data;
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.todo{
  border:2px solid silver;
  margin:10px;
  border-radius:10px;
  padding: 10px;
}

h1, {
    display: inline-block;
}


li {
    list-style-type: none;
}

.lock{
 background-color: gray;
}

.sameline{
  display: inline-block;
  padding-left: 5px;
}

</style>
