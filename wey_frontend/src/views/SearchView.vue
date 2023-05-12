<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
          <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">
              <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you looking for?">

              <button href="#" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
          </form>
      </div>
      <div
          class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
          v-if="users.length">
        <RouterLink class="p-4 text-center bg-gray-100 rounded-lg"
             v-for="user in users"
             v-bind:key="user.id"
              :to="{'name': 'profile', params:{'id': user.id}}">
            <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

            <p>
              <strong>
                {{ user.name }}
              </strong>
            </p>

            <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                <p class="text-xs text-gray-500">120 posts</p>
            </div>
        </RouterLink>
      </div>
      <div class="p-4 bg-white border border-gray-200 rounded-lg"
             v-for="post in posts"
             v-bind:key="post.id">
        <FeedItem v-bind:post="post"/>
        </div>
    </div>

   <div class="main-right col-span-1 space-y-4">
     <PeopleYouMayKnow/>
     <Trends/>

   </div>
  </div>
</template>

<script>
import axios from "axios";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import FeedItem from "@/components/FeedItem.vue";

export default {
  name: 'SearchView',

  components: {
    FeedItem,
    PeopleYouMayKnow,
    Trends,
  },

  data() {
    return {
      query: '',
      users: [],
      posts: []
    }
  },

  methods: {
    submitForm() {
      console.log('Submit Form', this.query)

      axios
          .post('/api/search/',{
            'query': this.query
          })
          .then(response => {
            console.log(response.data)

            this.users = response.data.users
            this.posts = response.data.posts
          })
          .catch(err => {
            console.log(err)
          })
    }
  }
}
</script>