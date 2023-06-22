<script setup>
import { onMounted } from 'vue';

let url = ref('')
let urls = ref([])
let comments = ref([])
let showType = ref('')
let loading = ref(false)
let loadingtext = ref('pleas wait ...')


onMounted(() => {
    getUrls()
})

async function getUrls() {
    await $fetch('http://127.0.0.1:8002/api/v1/post/urls/')
        .then(res => {
            urls.value = res.posts
        })

}
async function getCommentUrl(posturl) {
    await $fetch('http://127.0.0.1:8002/api/v1/post/comments?url=' + posturl + '&utm_source=share&utm_medium=member_desktop')
        .then(res => {
            loading.value = false
            comments.value = res?.comments
            showType.value = 'comments'
        })

}
async function getCommentMinedUrl(posturl) {
    await $fetch('http://127.0.0.1:8002/api/v1/post/getcommentsMined?url=' + posturl + '&utm_source=share&utm_medium=member_desktop')
        .then(res => {
            loading.value = false
            comments.value = res?.comments
            showType.value = 'commentsMined'
        })
}
async function delCommentUrl(posturl) {
    await $fetch('http://127.0.0.1:8002/api/v1/post/delete?url=' + posturl)
        .then(res => {
            $fetch('http://127.0.0.1:8002/api/v1/post/urls/')
                .then(res => {
                    urls.value = res.posts
                    getUrls()
                    showType.value = ''
                })
        })


}
</script>


<template>
    <div class="py-10 px-6 bground h-screen">
        <h1 class="mb-6 text-2xl text-center text-white capitalize">get comments by url</h1>
        <NuxtLink to="/" class="nuxtlink py-4 px-6 bg-teal-500 text-white rounded-xl">back</NuxtLink>
        <div v-if="loading" class="flex gap-2 justify-center mt-10">
            <img src="../assets/img/icons8-rhombus-loader.gif" />
            <p>{{ loadingtext }}</p>
        </div>
        <table class="border my-10 w-full shadow-md">
            <thead>
                <tr>
                    <th class="th-head">
                        row
                    </th>
                    <th class="th-head">
                        username
                    </th>
                    <th class="th-head">
                        password
                    </th>
                    <th class="th-head">
                        url
                    </th>
                    <th class="th-head">
                        action
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(url, index) in urls" :key="index">
                    <td class="px-6 py-4 ">
                        {{ index + 1 }}
                    </td>
                    <td class="px-6 py-4 ">
                        {{ url?.email }}
                    </td>
                    <td class="px-6 py-4 ">
                        {{ url?.password }}
                    </td>
                    <td class="px-6 py-4 text-sm ">
                        <a :href="url.url" target="_blank">{{ url?.url }}</a>
                    </td>
                    <td class="px-6 py-4 flex gap-2 ">
                        <button @click="getCommentUrl(url?.url)" class="py-2 px-4">comments</button>
                        <button @click="getCommentMinedUrl(url?.url)" class="py-2 px-4">commentsMined</button>
                        <button @click="delCommentUrl(url?.url)" class="py-2 px-4 rose">delete</button>
                    </td>
                </tr>
            </tbody>
        </table>


        <table class="border my-10 w-full shadow-md" v-if="showType == 'comments'">
            <thead>
                <tr>
                    <th class="th-head">
                        row
                    </th>
                    <th class="th-head">
                        Title
                    </th>
                    <th class="th-head">
                        Comment
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(comment, index) in comments" :key="index">
                    <td class="px-6 py-4 ">
                        <div class="text-sm text-gray-900">{{ index + 1 }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div class="text-sm text-gray-900">{{ comment?.author }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div class="text-sm text-gray-900">{{ comment?.comment }}</div>
                    </td>
                </tr>

            </tbody>
        </table>


        <table class="border my-10 w-full shadow-md " v-if="showType == 'commentsMined'">
            <thead>
                <tr>
                    <th class="th-head">
                        row
                    </th>
                    <th class="th-head">
                        Title
                    </th>
                    <th class="th-head">
                        Comment
                    </th>
                    <th class="th-head">
                        VADER negative
                    </th>
                    <th class="th-head">
                        VADER neutral
                    </th>
                    <th class="th-head">
                        VADER positive
                    </th>
                    <th class="th-head">
                        VADER COMPOUND
                    </th>
                    <th class="th-head">
                        ROBERTA negative
                    </th>
                    <th class="th-head">
                        ROBERTA neutral
                    </th>
                    <th class="th-head">
                        ROBERTA positive
                    </th>
                </tr>

            </thead>
            <tbody>
                <tr v-for="(comment, index) in comments" :key="index">
                    <td class="px-6 py-4 ">
                        <div>{{ index + 1 }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.author }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.comment }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.veder_neg }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.vader_neu }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.vader_pos }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div
                            :class="comment?.vader_compound > 0 ? 'text-green-700' : comment?.vader_compound < 0 ? 'text-rose-500' : 'text-black'">
                            {{ comment?.vader_compound }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_neg).toFixed(2) }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_neu).toFixed(2) }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_pos).toFixed(2) }}</div>
                    </td>

                </tr>

            </tbody>
        </table>
    </div>
</template>

<style scoped>
.bground {
    background: linear-gradient(-45deg, #ee7752, #765b8d, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 10s ease infinite;
    min-height: 100vh;
    height: 100%;
}

table {
    border-radius: 0.375rem;
    overflow: hidden;
    background: rgba(216, 216, 216, 0.347);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: rgb(0, 0, 0)
}

.th-head {
    padding: 18px;
    font-size: 16px;
    color: rgb(255, 255, 255);
}

tbody tr {
    transition: 0.2s;
}

thead {
    background-color: #097853;

}

tbody tr:hover {
    background: #efeeee4d;
}

button:focus,
.nuxtlink:focus {
    outline: none;
}

input:focus {
    outline: none;
    background: linear-gradient(white, white) padding-box,
        linear-gradient(to right, rgb(0, 139, 23), darkorchid) border-box;
    border: 1px solid transparent;
}

input {
    border: 1px solid white;
    transition: .3s;
    box-shadow: 0 4px 7px 0 rgba(10, 208, 53, 0.2);
}

input::placeholder {
    color: black;
    opacity: .5;
}

button,
.nuxtlink {
    background-color: #097853;
    border-radius: 8px;
    box-shadow: 0 4px 7px 0 rgba(19, 21, 19, 0.2);
    color: white;

}

.rose{
    background-color: #b60606b8;

}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}
</style>    