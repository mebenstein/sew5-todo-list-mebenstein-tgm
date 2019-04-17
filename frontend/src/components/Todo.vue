<template>
  <div :class="[todo.locked||master_lock ? 'lock' : '','todo']" :id="todo.id">
    <h1 :contenteditable="todo.locked||master_lock?false:true">{{ todo.title }}</h1>
    <div @click="togglLockstate">
      <img :src="todo.locked||master_lock?'https://image.flaticon.com/icons/svg/26/26053.svg':'https://cdn0.iconfinder.com/data/icons/tools-66/24/unlock-512.png'" width="20" >
    </div>
    <div @click="del">
      <img src="https://cdn4.iconfinder.com/data/icons/email-2-2/32/Trash-Email-Bin-512.png" width="20">
    </div>
    <li>
      <ul v-for="o in todo.children" v-bind:key="o"><Todo :todo="o" :parent_container="todo.children" :master_lock="todo.locked"/></ul>
    </li>
    <div  @click="add" class="todo" style="text-align:center">
        <b>+</b>
    </div>
  </div>
</template>
<script>

export default {
  name: 'Todo',
  props: {
    todo: Object,
    master_lock: Boolean,
    parent_container: Object
  },
  methods:{
    togglLockstate(){
      if(this.master_lock)return;
      this.todo.locked = ! this.todo.locked;
    },
    del(){
      if(this.todo.locked || this.master_lock)return;
      this.parent_container.splice( this.parent_container.indexOf(this.todo), 1 );
    },
    add(){
      if(this.todo.locked || this.master_lock)return;
      var obj = {"title":"new todo","locked":false};
      this.todo.children.push(obj);
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

</style>
