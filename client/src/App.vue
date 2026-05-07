<template>
  <div id ="app">
    <!-- navigation bar with links to chat and tickets pages -->
     <nav>
        <router-link to="/">Chat</router-link> 
        <router-link to="/tickets">Tickets</router-link>
     </nav>
     <!-- page content changes here based on route -->
      <router-view />
    </div>
</template>
 
<script setup> //setup keyword means code runs automatically and ne need to import anything manually and cleaner style
import { RouterLink, RouterView } from "vue-router" //just bring Routerlink and RouterView from vue-router package
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
}

nav {
  background-color: #2c3e50;
  padding: 1rem;
  display: flex;
  gap: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

nav a:hover {
  background-color: #34495e;
}
</style>


