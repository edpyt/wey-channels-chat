<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
          <img :src="user.get_avatar" class="mb-6 rounded-full">

          <p><strong>{{ user.name }}</strong></p>
          <p><small>{{ user.email }}</small></p>
          <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
              <RouterLink :to="{'name': 'friends', params: {'id': user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
              <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
          </div>


          <div class="mt-6">
            <div v-if="userStore.user.id !== user.id">
              <button class="inline-block py-4 px-3 bg-purple-600 text-sm text-white rounded-lg"
                      @click="sendFriendShipRequest">
                Send friendship request
              </button>

              <button class="inline-block mt-4 py-4 px-3 bg-purple-600 text-sm text-white rounded-lg"
                      @click="sendDirectMessage">
                Send direct message
              </button>
            </div>

            <div v-else>
              <RouterLink class="inline-block mr-2 py-4 px-3 bg-purple-600 text-sm text-white rounded-lg"
                          :to="{name: 'editprofile'}">
                Edit profile
              </RouterLink>
              <button class="inline-block py-4 px-3 bg-red-600 text-sm text-white rounded-lg"
                      @click="logout">
                Logout
              </button>
            </div>
          </div>
      </div>
    </div>


    <div class="main-center col-span-2 space-y-4">
        <div
            class="bg-white border border-gray-200 rounded-lg"
            v-if="userStore.user.id === user.id">
          <form v-on:submit.prevent="submitForm" method="POST">
            <div class="p-4">
                <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
            <img :src="previewPhoto" class="uploading-image rounded-xl mt-3"
                style="width: 145px">

            </div>

            <div class="p-4 border-t border-gray-100 flex justify-between">
              <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg cursor-pointer">
                <input type="file" @change="uploadImage">
                Attach Image
              </label>
              <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
            </div>
          </form>
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

<style>
input[type=file]{
  display: none;
}
</style>

<script>
import axios from "axios";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";
import FeedItem from "@/components/FeedItem.vue";

export default {
  name: 'FeedView',

  setup() {
    const userStore = useUserStore()
    const toastStore = useToastStore()

    return {
      userStore,
      toastStore
    }
  },
  components: {
    FeedItem,
    PeopleYouMayKnow,
    Trends,
  },

  data() {
    return {
      posts: [],
      user: {
        id: null
      },
      body: '',
      image: null,
      previewPhoto: null
    }
  },

  mounted() {
    this.getFeed()
  },

  watch: {
    '$route.params.id': {
      handler: function () {
        this.getFeed()
      },
      deep:true,
      immediate:true
    }
  },

  methods: {
    uploadImage(e){
      this.image = e.target.files[0];

      const reader = new FileReader();
      reader.readAsDataURL(this.image);

      reader.onload = e => {
        this.previewPhoto = e.target.result;
      }
    },
    sendDirectMessage() {
      console.log('sendDirectMessage')

      axios
          .get(`/api/chat/get-or-create/${this.$route.params.id}/`)
          .then(response => {
            console.log(response.data)

            this.$router.push('/chat')
          })
          .catch(err => {
            console.log(err)
          })
    },

    sendFriendShipRequest() {
      axios
          .post(`/api/friends/${this.$route.params.id}/request/`)
          .then(response => {
            console.log(response.data)

            if (response.data.message === 'request already sent') {
              this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
            } else {
              this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
            }
          })
          .catch(err => {
            console.log(err)
          })
    },
    getFeed() {
      axios.get(`/api/posts/profile/${this.$route.params.id}/`)
          .then(response => {
            this.posts = response.data.posts
            this.user = response.data.user
          })
          .catch(err => {
            console.log('error', err)
          })
    },

    submitForm() {
      console.log('submitForm', this.body, this.image)

      let formData = new FormData()
      formData.append('image', this.image)
      formData.append('body', this.body)

      axios.
          post('api/posts/create/', formData,{
            headers: {
              "Content-Type": "multipart/form-data"
            }
      })
          .then(response => {
            this.posts.unshift(response.data)
            this.body = ''
            this.image = null
            this.previewPhoto = null
            this.user.posts_count += 1
          })
          .catch(error => {
            console.log('error', error)
          })
    },

    logout() {
      console.log('Log out')

      this.userStore.removeToken()

      this.$router.push('/login')
    }
  }

}
</script>