<template>
    <div class="chat-container">
        <h1> Customer Support Chat </h1>

        <!--Ai toggle button -->
        <div class="ai-toggle">
            <button
                :class="{ active: selectedAI === 'openai' }"
                @click="selectedAI = 'openai'">
                Openai
            </button>
            <button
                :class="{ active: selectedAI === 'groq'}"
                @click="selectedAI = 'groq'">
                Groq
            </button>
        </div>

        <!-- messages appear here-->
        <div class="messages-area">
            <div
                v-for="message in messages"
                :key="message.id"
                :class="message.role">
                <p>{{ message.content }}</p>
            </div>

        </div>

        <!-- input form -->
         <div class="input-form">
            <input
                v-model="customerName"
                placeholder="Your name"
                type="text"
            />
            <input
                v-model="customerEmail"
                placeholder="Your email"
                type="email"
            />
            <textarea
                v-model="userMessage"
                placeholder="Type your message..."
            />
            <button @click="sendMessage">
                Send
            </button>

         </div>

    </div>
</template>

<script setup>
import { ref } from 'vue' //ref makes the variable dynamic
import axios from 'axios' //axios allows the http requests

//AI provider selection
const selectedAI = ref('groq') //shows which AI is selected

//form inputs
const customerName = ref('') //input the customer name
const customerEmail = ref('') //inputs the customer email
const userMessage = ref('')  //inputs the text message

//messages array
const messages = ref([]) //empty list for holding the messages

//loading state
const isLoading = ref(false) //true when AI is thinking, false when response received

const sendMessage = async () => {
    if (!customerName.value || !customerEmail.value || !userMessage.value) {
        alert('Please fill in all fields')
        return
    }

    // add user message to screen
    messages.value.push({
        id: Date.now(),
        role: 'user',
        content: userMessage.value
    })

    // AI is loading
    isLoading.value = true
    const message = userMessage.value
    userMessage.value = ''

    try {
        const response = await axios.post('http://localhost:3000/api/chat/process', {
            message: message,
            customer_name: customerName.value,
            customer_email: customerEmail.value,
            provider: selectedAI.value
        })

        messages.value.push({
            id: Date.now(),
            role: 'agent',
            content: response.data.response
        })
    } catch (error) {
        alert('Something went wrong. Please try again.')
    } finally {
        isLoading.value = false
    }
} // ← function closes here

</script>

<style scoped>
   
.chat-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.ai-toggle {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.ai-toggle button {
  padding: 0.5rem 1rem;
  border: 2px solid #2c3e50;
  border-radius: 4px;
  cursor: pointer;
  background: white;
}

.ai-toggle button.active {
  background: #2c3e50;
  color: white;
}

.messages-area {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  background: white;
}

.user {
  text-align: right;
  margin: 0.5rem 0;
}

.agent {
  text-align: left;
  margin: 0.5rem 0;
}

.user p {
  background: #2c3e50;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  display: inline-block;
}

.agent p {
  background: #ecf0f1;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  display: inline-block;
}

.input-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-form input,
.input-form textarea {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.input-form textarea {
  height: 100px;
  resize: none;
}

.input-form button {
  padding: 0.75rem;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.input-form button:hover {
  background: #34495e;
}
</style>



