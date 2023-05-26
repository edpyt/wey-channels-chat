<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <div class="space-y-4">
          <div class="flex items-center justify-between"
               v-for="conversation in conversations"
               v-bind:key="conversation.id"
               v-on:click="setActiveConversation(conversation.id)"
          >
              <div class="flex items-center space-x-2">

                  <template
                      v-for="user in conversation.users"
                      v-bind:key="user.id">

                    <img v-if="user.id !== userStore.user.id"
                         :src="user.get_avatar" class="w-[40px] rounded-full">


                    <p class="text-xs font-bold"
                       v-if="user.id !== userStore.user.id">
                      {{ user.name }}
                    </p>
                  </template>
              </div>

              <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }} ago</span>
          </div>
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">

      <div class="bg-white border border-gray-200 rounded-lg">
        <div class="flex flex-col flex-grow p-4">

          <template
                    v-for="message in activeConversation.messages"
                    v-bind:key="message.id">
            <div
                class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                v-if="message.created_by.id === userStore.user.id">
              <div>
                  <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                      <p class="text-sm">{{ message.body }}</p>
                  </div>
                  <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }} ago</span>
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
              </div>
            </div>

            <div
                class="flex w-full mt-2 space-x-3 max-w-md"
                v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
              </div>
              <div>
                  <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                      <p class="text-sm">{{ message.body }}</p>
                  </div>
                  <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }} ago</span>
              </div>
           </div>
          </template>

<span data-v-01536f9a=""><div data-v-62f48a11="" data-v-01536f9a="" class="seventv-emote-box emote-token"><img data-v-62f48a11="" class="seventv-chat-emote" srcset="https://cdn.7tv.app/emote/613937fcf7977b64f644c0d2/1x.webp 1x, https://cdn.7tv.app/emote/613937fcf7977b64f644c0d2/2x.webp 2x" alt="xdd" loading="lazy" decoding="async"><!----></div><span data-v-01536f9a=""></span></span>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg">
        <form v-on:submit.prevent="submitForm">
          <div class="p-4">
              <textarea minlength="1" v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What do you want to say?"></textarea>
          </div>

          <div class="bg-red-500 text-white rounded-lg p-4 mt-2"
              v-for="error in errors">
            {{ error }}
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
              Send
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

import {useUserStore} from "@/stores/user";

export default {
  name: 'chat',

  setup() {
    const userStore = useUserStore()


    return {
      userStore
    }
  },

  data() {
    return{
      conversations: [],
      activeConversation: {},
      body: '',
      socket: null,
      errors: []
    }
  },

  mounted() {
    this.getConversations()
  },

  methods: {
    setActiveConversation(id) {
      console.log('SetAcs', id)

      this.activeConversation = id
      this.getMessages()
    },
    async getConversations(){
      console.log('getConversations')

      await axios
          .get('/api/chat/')
          .then(response => {

            this.conversations = response.data
            console.log('conversations', this.conversations)
            if (this.conversations.length) {
              this.activeConversation = this.conversations[0].id
              this.getMessages()
            }
          })
          .catch(err => {
            console.log(err)
          })
    },

    getMessages(){
      const result = axios.defaults.baseURL.replace(/(^\w+:|^)\/\//, '')

      this.socket = new WebSocket(`ws://${result}/ws/${this.activeConversation}/`);

      let self = this

      this.socket.onmessage = function (event) {
        try {
          const resp = JSON.parse(event.data)
          self.activeConversation.messages.push(resp)
        } catch (e) {
          console.log('Error', e.message)
        }

      }


      axios.get(`/api/chat/${this.activeConversation}`)
          .then(response => {

            this.activeConversation = response.data
          })
          .catch(err => {
            console.log(err)
          })
    },

    submitForm() {
      if (this.body.length >= 1) {
        this.socket.send(JSON.stringify([this.userStore.user.id, this.activeConversation.id,
          this.body]))
        this.body = ''
      } else {
        this.errors.push('You need to fill it!')

        this.errors = this.errors.slice(0, 2)
      }

      // axios.post(`/api/chat/${this.activeConversation.id}/send/`, {
      //   body: this.body
      // })
      //     .then(response => {
      //
      //       this.activeConversation.messages.push(response.data)
      //
      //       this.body = ''
      //     })
      //     .catch(err => {
      //       console.log(err)
      //     })
    }
  }
}
</script>