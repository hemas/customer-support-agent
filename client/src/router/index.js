//creates the router for the whole app
import { createRouter, createWebHistory } from "vue-router";

import ChatView from '../views/ChatView.vue' //loads chat view page from views folder
import TicketsView from '../views/TicketsView.vue' //loads tickets view page from views folder

const routes = [
    {
        path: '/',              //localhost:5173 url
        component: ChatView     
    },
    {
        path: '/tickets',       //localhost:5173/tickets
        component: TicketsView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router //this can be used by other pages