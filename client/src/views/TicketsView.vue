<template>
  <div class="tickets-container">
    <h1>Support Tickets </h1>

    <!-- loading state-->
     <p v-if="isLoading">Loading tickets...</p>

     <!-- tickets list-->
      <div v-else>
        <div
            v-for ="ticket in tickets"
            :key="ticket.id"
            class="ticket-card">
            <h3>Ticket #{{ ticket.id }}</h3>
            <p>Status: {{ ticket.status }}</p>
            <p>Sentiment: {{ ticket.sentiment }}</p>
            <p>Intent: {{ ticket.intent }}</p>
            <p>Message: {{ ticket.query }}</p>
        </div>
      </div>
  </div>
</template>

<script setup>
import {ref, onMounted } from 'vue'
import axios from 'axios'

const tickets = ref ([])
const isLoading = ref(false)

const fetchTickets = async () => {
    isLoading.value = true
    try{
        const response = await axios.get('http://localhost:3000/api/tickets')
        tickets.value = response.data
    } catch (error) {
        console.error('Could not fetch tickets', error)
    } finally {
        isLoading.value= false
    }
}

//onMounted runs fetchTicjkets when page loads
onMounted(() => {
    fetchTickets()
})

</script>

<style scoped>
.tickets-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.ticket-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.ticket-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.ticket-card p {
  color: #666;
  margin: 0.25rem 0;
}
</style>


<style scoped>
.tickets-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}
</style>